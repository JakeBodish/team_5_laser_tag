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
        self.play_screen = False
        self.start_time = pygame.time.get_ticks()
        #loads splash screen image
        self.img = pygame.image.load("splash_screen.jpg")
        self.img = pygame.transform.scale(self.img, Screen.SCREEN_SIZE)
        #entry data storage
        self.red_players = [{"player_id": "", "equipment_id": ""} for _ in range(20)]
        self.green_players = [{"player_id": "", "equipment_id": ""} for _ in range(20)]
        self.entry_screen_options = []
        #current selection
        self.team = "RED"
        self.current_entry = ""
        self.last_entry = ""
        self.row = 0
        self.col = 0
        self.font = pygame.font.SysFont(None, 24)

        #Initilize text
        self.init_entry_options()

    #draw screen
    def update(self):
        self.screen.fill((0, 0, 0))

        #splash screen for first 3 seconds
        if not self.entry_screen and not self.play_screen:
            self.screen.blit(self.img, (0, 0))
            if pygame.time.get_ticks() - self.start_time > 3000:
                self.entry_screen = True
            pygame.display.flip()
            return

        elif self.entry_screen and not self.play_screen:
            #draw entry screen
            self.draw_entries()
            self.draw_potential_actions()

        elif not self.entry_screen and self.play_screen:
            #Draw play_screen
            self.draw_action_screen()

    def draw_entries(self):
        y = 100
        player_id_col = self.font.render("Player ID:", True, (255,255,255))
        name_id_col = self.font.render("Codename:", True, (255,255,255))
        self.screen.blit(player_id_col, (100,84))
        self.screen.blit(player_id_col, (500,84))
        self.screen.blit(name_id_col, (180,84))
        self.screen.blit(name_id_col, (580,84))
        
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
                player_id, name = player
                name = self.font.render(str(name), True, (255, 255, 255))
                playerID = self.font.render(str(player_id), True, (255, 255, 255))
                
                self.screen.blit(playerID, (115, y))
                self.screen.blit(name, (190, y)) 
                y += 25

        if(len(self.model.green_team) != 0):
            y = 105
            for key, player in self.model.green_team.items():
                player_id, name = player
                name = self.font.render(str(name), True, (255, 255, 255))
                playerID = self.font.render(str(player_id), True, (255, 255, 255))
                
                self.screen.blit(playerID, (515, y))
                self.screen.blit(name, (590, y)) 
                y += 25
        
        # Current entry
        entry = self.font.render(str(self.current_entry), True, (255,255,255))
        if self.col == 0:
            entry_x = 115
        else:
            entry_x = 515
        entry_y =105 + self.row*25
        pygame.draw.rect(self.screen, (255, 255, 0), (entry_x-15, entry_y-5, 75, 25), 2)
        self.screen.blit(entry, (entry_x, entry_y ))

    # Initalizes the text on entry screen and stores into an array to be printed
    def init_entry_options(self):
        add_player = self.font.render("1. Enter playerID then hit TAB to enter equipment ID", True, (255,255,255))
        config_network = self.font.render("2. Press F2 to configure server IP", True, (255,255,255))
        wipe_players = self.font.render("3. Press F12 to clear all entries", True, (255,255,255))
        action_screen = self.font.render("4. Press COMMA for action screen and game start", True, (255,255,255))
        exit_game = self.font.render("5. Press ESC to exit the program", True, (255,255,255))
        
        self.entry_screen_options.append(add_player)
        self.entry_screen_options.append(config_network)
        self.entry_screen_options.append(wipe_players)
        self.entry_screen_options.append(action_screen)
        self.entry_screen_options.append(exit_game)
    
    # Prints the text for action on player entry screen
    def draw_potential_actions(self):
        y = 625
        for option in self.entry_screen_options:
            self.screen.blit(option,(15, y))
            y += 15

    def draw_prompt(self, prompt: str, usr_input: str):
        y = 35
        pygame.draw.rect(self.screen, (100, 100, 100), (150, y, 550, 45), 4)
        prompt_ren = self.font.render(prompt, True, (255,255,255))
        usr_input_ren = self.font.render(usr_input, True, (255,255,255))
        self.screen.blit(prompt_ren, (160,y+5))
        self.screen.blit(usr_input_ren, (165,y+26))

    #Draws action screen
    def draw_action_screen(self):
        # RED and GREEN title at top of screen
        red_title = self.font.render("RED TEAM", True, (255,255,255))
        green_title = self.font.render("GREEN TEAM", True, (255,255,255))
        self.screen.blit(red_title, (100, 10))
        self.screen.blit(green_title, (600, 10))

        #Draw Rectangles
        pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, 800, 395), 4)
        pygame.draw.rect(self.screen, (255, 255, 255), (0, 405, 800, 350), 4)

        #Draw Rectangle Titles
        score_title = self.font.render("Current Scores", True, (255,255,255))
        action_title = self.font.render("Current Game Action", True, (255,255,255))
        self.screen.blit(score_title, (335, 10))
        self.screen.blit(action_title, (325, 415))

         # Draw the currently entered players for each team on the action screen.
        red_y = 45
        for player_id, name in self.model.red_team.values():
            red_text = self.font.render(str(name), True, (255,0,0))
            self.screen.blit(red_text, (100, red_y))
            red_y += 20

        green_y = 45
        for player_id, name in self.model.green_team.values():
            green_text = self.font.render(str(name), True, (0,255,0))
            self.screen.blit(green_text, (600, green_y))
            green_y += 20


        #calculate time left in game
        time_left = self.model.get_time_left()
        time_text = ("Time Remaining: " + str(time_left))
        time_title = self.font.render(time_text, True, (255,255,255))
        self.screen.blit(time_title, (550, 760))

        pygame.display.flip()
