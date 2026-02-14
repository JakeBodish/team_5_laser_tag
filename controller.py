######
# Class handles communication between hardware and server and keyboard inputs
######
import socket
from time import sleep
import queue
import pygame
from pygame.locals import*
import threading

class Controller():
	def __init__(self):
		self.running  = True
		self.in_progress = False
		
		# Network configuration
		self.serverIP = "0.0.0.0"
		self.incomingPort = 7501
		self.outgoingPort = 7500
		self.bufferSize  = 1024

		# Sockets
		self.UDPIncomingSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
		self.UDPIncomingSocket.bind((self.serverIP, self.incomingPort)) # Bind incoming socket to an IP
	
		self.UDPOutgoingSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
		self.UDPOutgoingSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Enable broadcast on outgoing socket
		
		# Thread to constantly listen to data and then store in data buffer.
		self.data_in_buffer = None # Initialized on game start
		self.listner = threading.Thread(target=self.listen, args=(), daemon=True)

# KEY INPUTS	
	def update(self):
		for event in pygame.event.get(): 
			if event.type == QUIT:
				self.running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.running = False
			elif event.type == pygame.MOUSEBUTTONUP: # Mouse clicked
				continue; 
			elif event.type == pygame.KEYUP: # Key released; put hotkeys here
				match event.key:
					
					case pygame.K_F1: # Return to Entry screen
						# TODO: Signal switch back to Entry screen
						# TODO: Signal to 
						continue;
						
					case pygame.K_F2: # Configure network during Entry 
						newIP = None #TODO: Prompt user for new server IP
						self.change_serverIP(newIP)
						
					case pygame.K_F3: # Start Game from Entry Screen
						if not self.in_progress:
							self.start()
						# TODO: Send start signal to view to switch screens
	
					case pygame.K_F12: # Wipe players 
						if self.in_progress:
							self.end()
						else:
							# TODO: Signal model to wipe if on entry
							continue;
						
					case pygame.K_TAB: # Swtich current entry field
						if not self.in_progress:
							# TODO: Switch field
						continue;
						
					case pygame.K_DELETE: # Delete selected player from Entry Screen
						if not self.in_progress:
							# TODO: Delete selected player
						# TODO: Signal model to delete player
						continue;
			
	def broadcast(self, data): # broadcast data to all clients
		bytes_to_send = str.encode(data)
		self.UDPOutgoingSocket.sendto(bytes_to_send, ("255.255.255.255", self.outgoingPort)) # Broadcast to all devices on the network
		
# START GAME
	def start(self): # Start code is 202
		self.broadcast("202")
		self.listner.start()
		self.in_progress = True
		self.data_in_buffer = Queue.queue()
# END GAME
	def end(self): # End code is 221
		self.broadcast("221") # Broadcast end code to all clients on the network
		self.in_progress = False
		self.data_in_buffer.shutdown()

###########################
#
# LISTENER THREAD STARTS AND ENDS WITH GAME START AND END
#
# TO RETRIEVE DATA, USE CONTROLLER.DATA_IN_BUFFER.GET()
#
##########################
	def listen(self): # Worker function for listner thread
		while self.in_progress:
			try:
				self.data_in_buffer.put(self.UDPIncomingSocket.recvfrom(self.bufferSize))
			except socket.error as e:
				print(f"Socket error: {e}")
			except queue.Shutdown as e:
				continue;
			sleep(0.04)


# Functions to update network parameters
	def change_serverIP(self, new_ip): # This is the one for Sprint 2. Others are extra
		self.serverIP = new_ip
		self.UDPIncomingSocket.bind((self.serverIP, self.incomingPort))
	def change_incomingPort(self, new_port):
		self.incomingPort= new_port
		self.UDPIncomingSocket.bind((self.serverIP, self.incomingPort))
	def change_outgoingPort(self, new_port):
		self.outgoingPort = new_port
