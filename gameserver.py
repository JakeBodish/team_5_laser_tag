########
# Main server program that will broadcast and recieve game logic
# SERVER WILL IMPLEMENTED AS A CLASS. IS NOT RIGHT NOW FOR TESTING AND DEMO PURPOSES
# WILL HANDLE SENDING AND RECEIVING DATA 
# Integrate class into a 'main.py'
#######
import socket

localIP     = "0.0.0.0"
localPort   = 7501
bufferSize  = 1024

num_test_packets = 0
MAX_num_test_packets = 5 # End game test after num packets sent

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

# Send a message to a client
def broadcast(msg, ip):
	bytes_to_send = str.encode(msg)
	UDPServerSocket.sendto(bytes_to_send, ip)
	global num_test_packets 
	num_test_packets += 1

# At this point we would input the players for the current game and broadcast their equipment codes

# Send start game message to all clients
# Right now there is only one client (trafficgenerator.py), but will eventually be every client
broadcast("202", ("127.0.0.1", 7500))

# Listen for any new data
while(True):
	# Get new data
	bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
	message = bytesAddressPair[0] # Data
	address = bytesAddressPair[1] # Return address of client
	clientMsg = "Message from Client:{}".format(message)
	clientIP  = "Client IP Address:{}".format(address)
	print(clientMsg) # Just for visualizing 
	print(clientIP) # Just for visualizing 
	
	# Process data recieved (ie Player 1 hit Player 2)
	
	# Send game logic back to affected clients
	broadcast("recieved", (address[0], 7500))
	
	# End test after sufficient packet tests
	if(num_test_packets == MAX_num_test_packets):
		break
# Send end game message to all clients
broadcast("221", ("127.0.0.1", 7500))
