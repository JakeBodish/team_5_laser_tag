######
# Class handles communication between hardware and server and keyboard inputs
######
import socket
import queue
import pygame
from pygame.locals import*
import threading

class Controller():
	def __init__(self):
		self.running  = True
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
		self.request_start = False
		self.request_add = False
		self.request_delete = False
		self.request_wipe = False

		#IP change mode
		self.ip_mode = False
		self.ip_text = ""

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
                    else:
                        self.running = False

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

            if event.type == KEYUP:
                if event.key == K_F2:
                    self.ip_mode = True
                    self.ip_text = ""

                if event.key == K_F3:
                    self.request_start = True

                if event.key == K_F12:
                    self.request_wipe = True

                if event.key == K_a:
                    self.request_add = True

                if event.key == K_DELETE:
                    self.request_delete = True
		
	#udp functions
    def broadcast(self, msg):
        self.UDPOutgoingSocket.sendto(
            msg.encode(),
            ("255.255.255.255", self.outgoingPort),
        )

    def broadcast_equipment(self, equipment_id):
        #broadcast equipment code after adds player
        self.broadcast(f"EQ:{equipment_id}")

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

