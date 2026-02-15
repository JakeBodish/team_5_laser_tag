#hi
# model.py
import sqlite3
from dataclasses import dataclass
from typing import List, Optional, Tuple

@dataclass
class Player:
    equipment_id: int
    name: str
  # "RED" or "GREEN"
    team: str

class Model:
    def __init__(self, db_path: str = "players.db"):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as con:
            cur = con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    equipment_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    team TEXT NOT NULL CHECK(team IN ('RED','GREEN'))
                )
            """)
            con.commit()

    def add_player(self, equipment_id: int, name: str, team: str) -> Tuple[bool, str]:
        team = team.upper().strip()
        if team not in ("RED", "GREEN"):
            return False, "Team must be RED or GREEN"
        if equipment_id <= 0:
            return False, "Equipment ID must be a positive integer"
        name = name.strip()
        if not name:
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
            return False, f"Equipment ID {equipment_id} already exists"

    def delete_player(self, equipment_id: int) -> bool:
        with self._connect() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM players WHERE equipment_id = ?", (equipment_id,))
            con.commit()
            return cur.rowcount > 0

    def get_players(self, team: Optional[str] = None) -> List[Player]:
        with self._connect() as con:
            cur = con.cursor()
            if team:
                team = team.upper().strip()
                cur.execute("SELECT equipment_id, name, team FROM players WHERE team = ? ORDER BY equipment_id", (team,))
            else:
                cur.execute("SELECT equipment_id, name, team FROM players ORDER BY team, equipment_id")
            rows = cur.fetchall()
        return [Player(*r) for r in rows]

    def wipe_all(self):
        with self._connect() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM players")
            con.commit()
