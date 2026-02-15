import pygame
from pygame.locals import *

class Screen:
    SCREEN_SIZE = (800, 800)

    def __init__(self):
        self.screen = pygame.display.set_mode(Screen.SCREEN_SIZE)
        #starts splash screen timer
        self.entry_screen = False
        self.start_time = pygame.time.get_ticks()
        #loads splash screen image
        self.img = pygame.image.load("splash_screen.jpg")
        self.img = pygame.transform.scale(self.img, Screen.SCREEN_SIZE)
        #entry data storage
        self.red_players = [{"id": "", "name": ""} for _ in range(20)]
        self.green_players = [{"id": "", "name": ""} for _ in range(20)]
        #current selection
        self.team = "RED"
        self.row = 0
        self.col = 0
        self.font = pygame.font.SysFont(None, 24)

    #draw screen
    def update(self):
        self.screen.fill((0, 0, 0))

        #splash screen for first 3 seconds
        if not self.entry_screen:
            self.screen.blit(self.img, (0, 0))
            if pygame.time.get_ticks() - self.start_time > 3000:
                self.entry_screen = True
            pygame.display.flip()
            return

        #sraw entry screen
        self.draw_entries()
        pygame.display.flip()

    def draw_entries(self):
        y = 100

        for i in range(20):
            #red side
            pygame.draw.rect(self.screen, (255, 0, 0), (100, y, 75, 25), 2)
            pygame.draw.rect(self.screen, (255, 0, 0), (175, y, 125, 25), 2)

            #green side
            pygame.draw.rect(self.screen, (0, 255, 0), (500, y, 75, 25), 2)
            pygame.draw.rect(self.screen, (0, 255, 0), (575, y, 125, 25), 2)

            y += 25
