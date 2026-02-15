#hi
# model.py
import sqlite3
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
                    equipment_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    team TEXT NOT NULL CHECK(team IN ('RED','GREEN'))
                )
            """)
            con.commit()
    #database operations
    def add_player(self, equipment_id: int, name: str, team: str) -> Tuple[bool, str]:
        #add player
        team = team.upper().strip()
        if team not in ("RED", "GREEN"):
            return False, "Team must be RED or GREEN"
        if equipment_id <= 0:
            return False, "Equipment ID must be a positive integer"
        if name == "":
            return False, "Name cannot be empty"

        try:
            with self._connect() as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO players (equipment_id, name, team) VALUES (?,?,?)",
                    (equipment_id, name, team),
                )
                con.commit()
            return True, "Player added"
        except sqlite3.IntegrityError:
            return False, f"Equipment ID already exists"
            
    def delete_player(self, equipment_id: int) -> bool:
        #delete player by ID
        with self._connect() as con:
            cur = con.cursor()
            cur.execute("delete from players where equipment_id = ?", (equipment_id,))
            con.commit()
            return cur.rowcount > 0

    def get_players(self, team: Optional[str] = None) -> List[Player]:
        #gets list of players
        with self._connect() as con:
            cur = con.cursor()
            if team:
                team = team.upper().strip()
                cur.execute("SELECT equipment_id, name, team from players where team = ? order by equipment_id", (team,))
            else:
                cur.execute("select equipment_id, name, team from players order by team, equipment_id")
            rows = cur.fetchall()
        return [Player(*r) for r in rows]

    def wipe_all(self):
        #removes all players from database
        with self._connect() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM players")
            con.commit()
