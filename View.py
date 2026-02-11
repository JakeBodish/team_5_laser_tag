import pygame
from pygame.locals import*
from time import sleep

class Screen():
    SCREEN_SIZE = (800,800)
    def __init__(self):
        self.screen = pygame.display.set_mode(Screen.SCREEN_SIZE,)
        self.entry_screen = False
        self.red_team_entry = []
        self.green_team_entry = []
        self.entry_text = []
        self.entry_rows = 20
        self.entry_col = 2
        self.entry_box_height = 25
        self.init_entry_arrays()
        self.init_entry_text()
        self.img = pygame.image.load('splash_screen.jpg')
        self.scaled_img = pygame.transform.scale(self.img, (800, 800))

    def init_entry_arrays(self): # initalizes the red and green team entry screen arrays
         for i in range(self.entry_rows):
            for j in range(self.entry_col):
                if(j == 0): #First box for player ID
                    red_rect = pygame.Rect(100, 100 + self.entry_box_height * i, 75, self.entry_box_height)
                    green_rect = pygame.Rect(500, 100 + self.entry_box_height * i, 75, self.entry_box_height)
                if(j == 1): #Second box for player Name
                    red_rect = pygame.Rect(175, 100 + self.entry_box_height * i, 125, self.entry_box_height)
                    green_rect = pygame.Rect(575, 100 + self.entry_box_height * i, 125, self.entry_box_height)
                
                self.red_team_entry.append(red_rect)
                self.green_team_entry.append(green_rect)

    def init_entry_text(self):
        # "Player Entry Screen" 
        font = pygame.font.SysFont(None, 36)
        text_surface = font.render("Player Entry Screen", True, (255, 255, 255))
        text = (text_surface, (280, 25))
        self.entry_text.append(text)

        # "Red Team"
        font = pygame.font.SysFont(None, 20)
        text_surface = font.render("Red Team", True, (255, 0, 0))
        text = (text_surface, (150, 75))
        self.entry_text.append(text)

        # "Green Team"
        font = pygame.font.SysFont(None, 20)
        text_surface = font.render("Green Team", True, (0, 255, 0))
        text = (text_surface, (550, 75))
        self.entry_text.append(text)


    def update(self):
        self.screen.fill((0, 0, 0))
        if(self.entry_screen):
            for rect in self.red_team_entry: # Draw red team entry table
                pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)
            for rect in self.green_team_entry: # Draw green team entry table
                pygame.draw.rect(self.screen, (0, 255, 0), rect, 2)

            #Print words to the screen
            for text in self.entry_text:
                self.screen.blit(text[0], text[1])
        else: 
            #Prints scaled Splash Screen image, waits 3s and updates entry_screen
            self.screen.blit(self.scaled_img, (0, 0))
            sleep(3)
            self.entry_screen = True

        pygame.display.flip()
