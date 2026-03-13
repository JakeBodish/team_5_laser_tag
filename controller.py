######
# Class handles communication between hardware and server and keyboard inputs
######
import socket
import queue
import pygame
from pygame.locals import*
import threading

class Controller():
    def __init__(self, v, m):
        self.running  = True
        self.request_start = False
        self.request_wipe = False
        self.view = v
        self.model = m
        #true when game running
        self.in_progress = False
        
        # Network configuration
        self.serverIP = "0.0.0.0"
        self.incomingPort = 7501
        self.outgoingPort = 7500
        self.bufferSize  = 1024

        # Sockets
        #incoming socket
        self.UDPIncomingSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPIncomingSocket.bind((self.serverIP, self.incomingPort)) # Bind incoming socket to an IP

        #outgoing socket
        self.UDPOutgoingSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPOutgoingSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Enable broadcast on outgoing socket

        # Thread to constantly listen to data and then store in data buffer.
        self.data_in_buffer = queue.Queue()
        self.stop_event = threading.Event()
        self.listener = threading.Thread(target=self.listen, daemon=True)

        #input flags
        self.new_name = False
        self.name = ""
        self.equip_id = False

        #IP change mode
        self.ip_mode = False
    	self.ip_text = ""
        
        # Input text buffer
        self.usr_txt = ""

        # player and equipment tracking
        self.player_id = ""
        self.equipment_id = ""
		
    #event processing	
    def process_events(self, events):
        for event in events:
            if event.type == QUIT:
                self.running = False
            if event.type == KEYDOWN:
                #esc quits program or cancels IP input
                if event.key == K_ESCAPE:
                    if self.ip_mode:
                        self.ip_mode = False
                        self.ip_text = ""
                    else:
                        self.running = False
					continue

                #if typing IP address
                if self.ip_mode:
                    if event.key == K_RETURN:
                        self.change_serverIP(self.ip_text)
                        self.ip_mode = False
                    elif event.key == K_BACKSPACE:
                        self.ip_text = self.ip_text[:-1]
                    else:
                        if event.unicode.isdigit() or event.unicode == ".":
                            self.ip_text += event.unicode
					continue
                            
                #if typing new codename
                elif self.new_name: # This is True only when a new player is detected by the controller itself. Do not set True another way.
                    if event.key == K_RETURN:
                        self.name = self.usr_txt
                        if self.name != "":
                        	self.model.add_player_to_database(self.player_id, self.name)
                       		self.usr_txt = ""
                        	self.new_name = False
							self.equip_id = True
                    elif event.key == K_BACKSPACE:
                        self.usr_txt = self.usr_txt[:-1]
                    else:
                        self.usr_txt += event.unicode
					continue
                #if typing equipment code
                elif self.equip_id:
                    if event.key == K_RETURN:
                        self.equipment_id = self.usr_txt
                        if self.equipment_id != "":
	                        self.usr_txt = ""
	                        self.equip_id = False
	                        self.model.add_player_to_game(self.player_id, self.equipment_id, self.view.team)
	                        self.broadcast(self.equipment_id)

							self.view.current_entry = self.usr_txt
                        if self.view.col+1>=2:
                            self.view.row = (self.view.row+1)%20
                        self.view.col = (self.view.col+1)%2
                        if self.view.col == 1:
	                        self.view.team = "GREEN"
                        else:
	                        self.view.team = "RED"
	    	            
                    elif event.key == K_BACKSPACE:
                        self.usr_txt = self.usr_txt[:-1]
                    else:
                        if event.unicode.isdigit():
                            self.usr_txt += event.unicode
					self.view.current_entry = self.usr_txt
					continue
                #if typing playerId, switching between fields in player entry   
                elif self.view.entry_screen: # player entry
                    if event.key == K_TAB: # Switch fields
						
                        self.player_id = self.usr_txt
                        if self.player_id != "":
                        	self.name = self.model.get_player_name(self.player_id)
							self.view.last_entry = self.player_id
							self.usr_txt = ""
                        	if self.name == None:
                            	self.new_name = True
							else:
								self.equip_id = True
                        	continue
               
                    elif event.key == K_BACKSPACE:
                        self.usr_txt = self.usr_txt[:-1]
                    else:
                        if event.unicode.isdigit():
                            self.usr_txt += ""+event.unicode
                    self.view.current_entry = self.usr_txt

            if event.type == KEYUP:
                if event.key == K_F2:
                    self.ip_mode = True
                    self.ip_text = ""
                
                if event.key == K_F5:
                    if(self.view.entry_screen):
                        self.view.entry_screen = False
                        self.view.play_screen = True
                        self.model.playing = False
                        self.model.start_30s_timer = True

                if event.key == K_F12:
                    if self.view.entry_screen:
                        self.model.wipe_all() # Wipe teams
                        self.view.row = 0 # Reset index for player entry screen
                        self.view.col = 0
                        self.view.team = "RED"
                        self.view.current_entry = ""
                        self.view.last_entry = ""
                        self.usr_txt = ""
                        self.new_name = False
                        self.equip_id = False

        if self.new_name:
            prompt = "New Player ID detected, input new codename. Press ENTER to save:"
            self.view.draw_prompt(prompt, self.usr_text)            
        elif self.equip_id:
            prompt = "Input the hardware ID for '" +  self.name +"'. Press ENTER when done:"
            self.view.draw_prompt(prompt, self.usr_txt)
        elif self.ip_mode:
            prompt = "Input a new IP. Press ENTER when done. ESCAPE to cancel:"
            self.view.draw_prompt(prompt, self.ip_text)
        
        #Broadcast start code once 30s start timer is done:
        if self.model.playing and not self.in_progress:
            self.start()
		
		#Broadcast end game
        elif not self.model.playing and self.in_progress:
            self.end()
    #udp functions
    def broadcast(self, msg):
        self.UDPOutgoingSocket.sendto(
            msg.encode(),
            ("255.255.255.255", self.outgoingPort),
        )

    def start(self):
        #broadcast game start code
        self.broadcast("202")
        self.in_progress = True

        self.stop_event.clear()
        if not self.listener.is_alive():
            self.listener = threading.Thread(target=self.listen, daemon=True)
            self.listener.start()

    def end(self):
        #broadcast game end code
        self.broadcast("221")
        self.in_progress = False
        self.stop_event.set()

    def listen(self):
        #thread listens for udp sockets
        while not self.stop_event.is_set():
            try:
                data, addr = self.UDPIncomingSocket.recvfrom(self.bufferSize)
                self.data_in_buffer.put((data, addr))
            except:
                break

    #network configuration
    def change_serverIP(self, new_ip):
        #allows user to change network binding address
        try:
            self.serverIP = new_ip
            self.UDPIncomingSocket.close()
            self.UDPIncomingSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.UDPIncomingSocket.bind((self.serverIP, self.incomingPort))
        except:
            pass

