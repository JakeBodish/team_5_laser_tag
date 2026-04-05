# team_5_laser_tag
Team 5 repository for Software Engineering Laser Tag Project

Team Members:  
JakeBodish | Jake Bodishbaugh  
collinkierce | Collin Kierce  
alexhayek | Alex Hayek  
elimccrary | Eli McCrary  
micahlivingston | Micah Livingston  

### HOW TO SET-UP ###

1. In top-left corner click Devices -> Insert Guest Additions CD Image
2. A new icon will pop-up on the desktop, double click it
3. Inside folder, right-click and select Open in Terminal
4. run commands:
5. sudo apt update
6. sudo apt install build-essential dkms linux-headers-$(uname -r)
7. sudo sh VBoxLinuxAdditions.run
8. sudo reboot

### HOW TO RUN ###

Sprint4:
1. in terminal run command: sed -i 's/\r$//' install.sh
2. bash install.sh
3. python3 main.py
4. In top left click View -> Auto-resize Guest Display
5. On player entry screen input player ID and hit TAB 
6. If it is a new player, you will be prompted to enter a new codename 
7. Enter the equipment ID for the player 
8. Press F2 to configure server IP 
9. Press COMMA to enter action screen and begin game start countdown
10. Press F12 to clear entries from player entry screen

