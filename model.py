#hi
# model.py
import sqlite3
import pygame
import random
from dataclasses import dataclass
from typing import List, Optional, Tuple

@dataclass
class Player:
    #player record
    equipment_id: int
    name: str
    #red or green
    team: str

class Model:
    #database linked to application
    def __init__(self, db_path: str = "players.db"):
        #database file name
        self.db_path = db_path
        #creates table if not there
        self._init_db()

        #Teams hardwareID:(playerID, codename)
        self.red_team = {}
        self.green_team = {}

        #Timer, Game, and Music settings
        self.start_30s_timer = True
        self.playing = True
        self.start_time = 0
        self.time_left = 0
        self.music_playing = False

    def _connect(self):
        #connection to database
        return sqlite3.connect(self.db_path)
    def _init_db(self):
        #creates players table if not there
        with self._connect() as con:
            cur = con.cursor()
            #creates table structure
            cur.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    player_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                )
            """)
            con.commit()

    def check_if_player_already_exists(self, player_id: int, equipment_id: int):
        for equip_id in self.red_team:
            p_id = self.red_team[equip_id][0]
            if player_id == p_id:
                print("player already on red team!")
                return False
            if equip_id == equipment_id:
                print("equipment number is already taken!")
                return False

        for equip_id in self.green_team:
            p_id = self.green_team[equip_id][0]
            if player_id == p_id:
                print("player already on green team!")
                return False
            if equip_id == equipment_id:
                print("equipment number is already taken!")
                return False

        return True

            
    #database operations
    def add_player_to_game(self, player_id: int, equipment_id: int, team: str):
		#add player to game memory
        name = self.get_player_name(player_id)
        if team == "RED":
            if(self.check_if_player_already_exists(player_id, equipment_id)):
                self.red_team[equipment_id] = (player_id,name)
                return True
            else:
                return False
        else:
            if(self.check_if_player_already_exists(player_id, equipment_id)):
                self.green_team[equipment_id] = (player_id,name)
                return True
            else:
                return False

    def add_player_to_database(self, player_id: int, name: str):
        #add player_id and codename to database for future use
        if name == "":
            print("name can not be empty")
            return False, "Name cannot be empty"

        # Add player to database
        try:
            with self._connect() as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO players (player_id, name) VALUES (?,?)",
                    (player_id, name),
                )
                con.commit()
            return True, "Player added"
        except sqlite3.IntegrityError:
            return False, f"PLayer ID already exists"
            
    def delete_player(self, equipment_id: int) -> bool:
        #delete player by ID
        with self._connect() as con:
            cur = con.cursor()
            cur.execute("delete from players where equipment_id =  ?", (equipment_id,))
            con.commit()
            return cur.rowcount > 0

    def get_player_name(self, player_id):
        #gets list of players
        with self._connect() as con:
            cur = con.cursor()
            try:
                cur.execute("SELECT name from players where player_id =  ?", (player_id,))
            except Exception as e:
                print(e)
            name = str(cur.fetchone())
        return name.strip("()'',")

    def wipe_all(self):
        self.red_team = {}
        self.green_team = {}
    
    # A function so the View can grab the amount of time left in the game
    def get_time_left(self):
        if(self.playing and self.start_30s_timer):
            return "00:00"
        current_time = pygame.time.get_ticks()
        time_remaining = int((self.time_left - (current_time - self.start_time)) / 1000)
        minutes = int((time_remaining) / 60)
        seconds = time_remaining % 60
        if seconds < 10:
            return (str(minutes) + ":0" + str(seconds))
        else: 
            return (str(minutes) + ":" + str(seconds))
        
    #A function to clear all player entries on player entry screen -> f12
    def clear_player_entries(self):
        self.red_team.clear()
        self.green_team.clear()
        print("Players cleared")


    #update function
    def update(self):
        #Start 30 second timer before entering game
        if(self.start_30s_timer and not self.playing):
            self.start_time = pygame.time.get_ticks()
            self.time_left = 30000 #30 seconds
            self.start_30s_timer = False
            print("Set 30 second timer")
            return

        #Calculate difference between current time and start time to see how much time has passed
        current_time = pygame.time.get_ticks()
        if(current_time - self.start_time > self.time_left):
            if(not self.start_30s_timer and not self.playing):
                print("30 seconds is up")
                self.playing = True
                self.start_time = pygame.time.get_ticks()
                self.time_left = 360000
            elif(not self.start_30s_timer and self.playing):
                print("game is over")
                self.playing = True
                self.start_30s_timer = True
        elif(current_time - self.start_time >= 12000 and not self.music_playing):
            self.play_music()

    def play_music(self):
        track_num = random.randint(1,8)
        track_name = "Track0" + str(track_num) + ".mp3"

        try:
            pygame.mixer.music.load("photon_tracks/" + track_name)
            pygame.mixer.music.play()
            self.music_playing = True
        except:
            print("something went wrong in the music selection")
            return 66
        


        
        
