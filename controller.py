######
# Class handles communication between hardware and server
######
import socket

class controller():
	def __init__(self):
		self.localIP     = "0.0.0.0"
		self.localPort   = 7501
		self.remotePort = 7500
		self.bufferSize  = 1024
		self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
		self.UDPServerSocket.bind((self.localIP, self.localPort)) # Bind server socket to an IP
	
	def send_data(self, data, clientIP): # send data to a client
		bytes_to_send = str.encode(data)
		self.UDPServerSocket.sendto(bytes_to_send, clientIP)
	
	def start(self): # Start code is 202
		''' 
		for player in player_database:
			self.send_data("202", (player.ip, self.remotePort))
		'''
		self.send_data("202", ("127.0.0.1", self.remotePort)) # coded for one client right now (trafficgenerator.py)
	
	def end(self) # End code is 221
		''' 
		for player in player_database:
			self.send_data("221", (player.ip, self.remotePort))
		'''
		self.send_data("221", ("127.0.0.1", self.remotePort)) # coded for one client right now (trafficgenerator.py)
		
	def listen(self): # Listen for new data
		bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize) # Pauses until new data is recieved
			# if it needs to be actively listening, a thread might need to be used to constantly listen otherwise the main program loop could miss data while its processing stuff. maybe?
		data = bytesAddressPair[0] # Data
		address = bytesAddressPair[1] # Return address of client
		return data, address 
		
	# Functions to update network parameters
	def change_localIP(self, new_ip):
		self.localIP = new_ip
		self.UDPServerSocket.bind((self.localIP, self.localPort))
	def change_localPort(self, new_port):
		self.localPort= new_port
		self.UDPServer((self.localIP, self.localPort))
	def change_remotePort(self, new_port):
		self.remotePort = new_port
