#hi
# model.py
import sqlite3
import pygame
import random
import psycopg2 as psycop
from psycopg2 import sql
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
        self.vm_db = self.try_connect_to_vm_db()
        if self.vm_db == True:
            self.connect_params = {
                "host" : "localhost",
                "database" : "photon",
                "user" : "student",
                "password" : "student",
                "port" : 5432
            }
        else:
            #If connection to VM db fails connect to players.db
            self.db_path = db_path
            #creates table if not there
            self._init_db()

        #Teams hardwareID:(playerID, codename)
        self.red_team = {}
        self.green_team = {}
        self.hit_base = []

        #Timer, Game, and Music settings
        self.start_30s_timer = True
        self.playing = True
        self.game_over = False
        self.start_time = 0
        self.time_left = 0
        self.music_playing = False

    #attempts to connect to vm db, return true or false
    def try_connect_to_vm_db(self):
        try:
            conn = psycop.connect(
                host="localhost",
                database="photon",
                user="student",
                password="student",
                port="5432"
            )
            print("connected to VM database sucessfully")
            conn.close()
            return True
        except Exception as e:
            print("failed to connnect to VM database: " + str(e))
            return False

    #Connection for testing DB
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
        if self.vm_db:
            return self.add_player_to_vm_db(player_id, name)
        else:
            return self.add_player_to_testing_db(player_id, name)


    def add_player_to_vm_db(self, player_id: int, name: str):
        if name == "":
            print("name can not be empty")
            return False, "Name cannot be empty"

        try:
            conn = psycop.connect(**self.connect_params)
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO players (id, codename) VALUES (%s, %s);",
                (player_id, name)
            )
            conn.commit()
            cur.close()
            conn.close()
            return True, "Player added"
        except Exception as e:
            return False


    def add_player_to_testing_db(self, player_id: int, name: str):
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
        if self.vm_db:
            return self.delete_player_from_vm_db(equipment_id)
        else:
            return self.delete_player_from_testing_db(equipment_id)

    def delete_player_from_vm_db(self, id: int) -> bool:
        try:
            conn = psycop.connect(**self.connect_params)
            cur = conn.cursor()

            cur.execute(
                "DELETE FROM players WHERE id = %s;",
                (id,)
            )
            conn.commit()
            rows = cur.rowcount > 0
            cur.close()
            conn.close()
            return rows
        except Exception as e:
            print(str(e))
            
    def delete_player_from_testing_db(self, equipment_id: int) -> bool:
        #delete player by ID
        with self._connect() as con:
            cur = con.cursor()
            cur.execute("delete from players where equipment_id =  ?", (equipment_id,))
            con.commit()
            return cur.rowcount > 0


    def get_player_name(self, player_id):
        if self.vm_db:
            return self.get_player_from_vm_db(player_id)
        else:
            return self.get_player_from_testing_db(player_id)

    def get_player_from_vm_db(self, player_id: int):
        try:
            conn = psycop.connect(**self.connect_params)
            cur = conn.cursor()
            cur.execute(
                "SELECT codename FROM players WHERE id = %s;",
                (player_id,)
            )

            result = cur.fetchone()
            cur.close()
            conn.close()
            if result:
                return result[0]
            else:
                return "None"
                
        except Exception as e:
            print(str(e))

    def get_player_from_testing_db(self, player_id: int):
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
        if self.game_over:
            return "00:00"

        current_time = pygame.time.get_ticks()
        time_remaining = max(0, int((self.time_left - (current_time - self.start_time)) / 1000))

        minutes = time_remaining // 60
        seconds = time_remaining % 60

        return f"{minutes:02}:{seconds:02}"
	
    def process_hit(self, player1, player2):
        redbase = '53'
        greenbase = '43'
        player1_team = 0 # red team = 0, green team = 1
        player2_team = 0

        if player1 in self.red_team.keys():
            player1_team = 0
        else:
            player1_team = 1

        if player2 == redbase:
            if player1_team == 1: #recieve 100 points
                self.scores[player1_team][player1] += 100
                self.hit_base.append(player1)
            #add symbol to their name on scoreboard
            return [redbase] #not sure what to return for base hit
        elif player2 == greenbase:
            if player1_team == 0:
                self.scores[player1_team][player1] += 100
                self.hit_base.append(player1)
            return [greenbase]
        elif player2 in self.red_team.keys():
            player2_team = 0
        else:
            player2_team = 1

        if player1_team == player2_team: #-10 each
            self.scores[player1_team][player1] -= 10
            self.scores[player2_team][player2] -= 10
            return [player1, player2]
        else: #+10/-10
            self.scores[player1_team][player1] += 10
            #self.scores[player2_team][player2] -= 10
            return [player2]
	
    def reset_scores(self):
        self.scores = [{player:0 for player in self.red_team.keys()},{player:0 for player in self.green_team.keys()}]
        self.hit_base = []
    
    def get_team_score(self, team):
        score = 0
        if team == 'RED':
            for _, player_score in self.scores[0].items():
                score += player_score
        else:
            for _, player_score in self.scores[1].items():
                score += player_score
        return score
        
    #update function
    def update(self):
        #Start 30 second timer before entering game
        if self.game_over:
            return

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
                self.playing = False
                self.game_over = True
                self.start_30s_timer = False
                return
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
        


        
        
