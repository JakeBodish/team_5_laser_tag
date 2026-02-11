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
		self.data_in_buffer = queue.Queue()
		self.listner = threading.Thread(target=self.listen, args=(), daemon=True)
	
	def update(self):
		for event in pygame.event.get(): # Process any key inputs
			if event.type == QUIT:
				self.running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.running = False
	
	def broadcast(self, data): # send data to a client
		bytes_to_send = str.encode(data)
		self.UDPOutgoingSocket.sendto(bytes_to_send, ("255.255.255.255", self.outgoingPort)) # Broadcast to all devices on the network
# START GAME
	def start(self): # Start code is 202
		self.broadcast("202")
		self.listner.start() 
# END GAME
	def end(self): # End code is 221
		self.broadcast("221") # Broadcast end code to all clients on the network


	def listen(self): # Worker function for listner thread
		while self.running:
			try:
				self.data_in_buffer.put(self.UDPIncomingSocket.recvfrom(self.bufferSize))
			except socket.error as e:
				print(f"Socket error: {e}")
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
