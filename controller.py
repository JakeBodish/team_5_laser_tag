######
# Class handles communication between hardware and server and keyboard inputs
######
import socket
import select
from time import sleep
import queue
import pygame
from pygame.locals import*
import threading
from sys import exit

class Controller():
	def __init__(self):
		self.running  = True
		self.localIP     = "0.0.0.0"
		self.localPort   = 7501
		self.remotePort = 7500
		self.bufferSize  = 1024
		self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
		self.UDPServerSocket.bind((self.localIP, self.localPort)) # Bind server socket to an IP
		
		# Thread to constantly listen to data and then store in data buffer.
		self.data_in_buffer = queue.Queue()
		self.databuffer_lock = threading.Lock()
		# self.listner = threading.Thread(target=self.listen(), args=(self), daemon=True)
		# self.listner.start()
		
	
	def update(self):
		self.listen()
		for event in pygame.event.get(): # Process any key inputs
			if event.type == QUIT:
				self.running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.running = False
	
	def send_data(self, data, clientIP): # send data to a client
		bytes_to_send = str.encode(data)
		self.UDPServerSocket.sendto(bytes_to_send, clientIP)
	
	def start(self): # Start code is 202
		''' 
		for player in player_database:
			self.send_data("202", (player.ip, self.remotePort))
		'''
		self.send_data("202", ("127.0.0.1", self.remotePort)) # coded for one client right now (trafficgenerator.py)
	
	def end(self): # End code is 221
		''' 
		for player in player_database:
			self.send_data("221", (player.ip, self.remotePort))
		'''
		self.send_data("221", ("127.0.0.1", self.remotePort)) # coded for one client right now (trafficgenerator.py)
		
	def listen(self): # Listen for new data
		ready_to_read, _, _ = select.select([self.UDPServerSocket], [], [], 1)
		if ready_to_read:
			try:
				self.data_in_buffer.put(self.UDPServerSocket.recvfrom(self.bufferSize))
			except socket.error as e:
				print(f"Socket error: {e}")
		sleep(0.04)
		# have an input and output buffer for sending and recieving data
		# have a thread running to see if it can read or write constantly. based on if there is data in buffers or not
		
	# Functions to update network parameters
	def change_localIP(self, new_ip):
		self.localIP = new_ip
		self.UDPServerSocket.bind((self.localIP, self.localPort))
	def change_localPort(self, new_port):
		self.localPort= new_port
		self.UDPServer((self.localIP, self.localPort))
	def change_remotePort(self, new_port):
		self.remotePort = new_port
