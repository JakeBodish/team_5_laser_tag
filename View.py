import pygame
from pygame.locals import *

class Screen:
    SCREEN_SIZE = (800, 800)

class Screen(): #testing commiting from terminal
    SCREEN_SIZE = (800,800)
    def __init__(self, m):
        self.model = m
        self.screen = pygame.display.set_mode(Screen.SCREEN_SIZE)
        #starts splash screen timer
        self.entry_screen = False
        self.start_time = pygame.time.get_ticks()
        #loads splash screen image
        self.img = pygame.image.load("splash_screen.jpg")
        self.img = pygame.transform.scale(self.img, Screen.SCREEN_SIZE)
        #entry data storage
        self.red_players = [{"player_id": "", "equipment_id": ""} for _ in range(20)]
        self.green_players = [{"player_id": "", "equipment_id": ""} for _ in range(20)]
        #current selection
        self.team = "RED"
        self.current_entry = ""
        self.last_entry = ""
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

        #draw entry screen
        self.draw_entries()
        

    def draw_entries(self):
        y = 100
        font = pygame.font.SysFont("Arial", 16)
        player_id_col = font.render("Player ID:", True, (255,255,255))
        equip_id_col = font.render("Equipment ID:", True, (255,255,255))
        self.screen.blit(player_id_col, (100,84))
        self.screen.blit(player_id_col, (500,84))
        self.screen.blit(equip_id_col, (175,84))
        self.screen.blit(equip_id_col, (575,84))
        
        # boxes
        for i in range(20):
            #red side
            pygame.draw.rect(self.screen, (255, 0, 0), (100, y, 75, 25), 2)
            pygame.draw.rect(self.screen, (255, 0, 0), (175, y, 125, 25), 2)
            

            #green side
            pygame.draw.rect(self.screen, (0, 255, 0), (500, y, 75, 25), 2)
            pygame.draw.rect(self.screen, (0, 255, 0), (575, y, 125, 25), 2)

            y += 25
        
        #draw the player info on entry screen
        if(len(self.model.red_team) != 0):
            y = 105
            for key, player in self.model.red_team.items():
                player_id, _ = player
                hardware = font.render(str(key), True, (255, 255, 255))
                playerID = font.render(str(player_id), True, (255, 255, 255))
                
                self.screen.blit(playerID, (115, y))
                self.screen.blit(hardware, (190, y)) 
                y += 25

        if(len(self.model.green_team) != 0):
            y = 105
            for key, player in self.model.green_team.items():
                player_id, _ = player
                hardware = font.render(str(key), True, (255, 255, 255))
                playerID = font.render(str(player_id), True, (255, 255, 255))
                
                self.screen.blit(playerID, (515, y))
                self.screen.blit(hardware, (590, y)) 
                y += 25
        
        # Current entry
        entry = font.render(str(self.current_entry), True, (255,255,255))
        last_entry = font.render(str(self.last_entry), True, (255,255,255))
        if self.col == 0:
            entry_x = 115
        elif self.col == 1:
            entry_x = 190
        elif self.col == 2:
            entry_x = 515
        elif self.col == 3:
            entry_x = 590
        entry_y =105 + self.row*25
        pygame.draw.rect(self.screen, (255, 255, 0), (entry_x-15, entry_y-5, 75, 25), 2)
        self.screen.blit(entry, (entry_x, entry_y ))
        if self.col % 2 == 1:
            self.screen.blit(last_entry, (entry_x-75, entry_y))
        
    def draw_prompt(self, prompt: str, usr_input: str):
        y = 35
        font = pygame.font.SysFont("Arial", 16)
        pygame.draw.rect(self.screen, (100, 100, 100), (150, y, 550, 45), 4)
        prompt_ren = font.render(prompt, True, (255,255,255))
        usr_input_ren = font.render(usr_input, True, (255,255,255))
        self.screen.blit(prompt_ren, (160,y+5))
        self.screen.blit(usr_input_ren, (165,y+26))
