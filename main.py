######
# Main program loop
######
import pygame
from pygame.locals import*
from time import sleep
from controller import Controller
from View import Screen

if __name__=="__main__":
	pygame.init()
	view = Screen()
	controller = Controller()

	while controller.running:
		view.update()
		controller.update()
		sleep(0.04)
