import sqlite3
import os
from contextlib import contextmanager

DB_NAME = os.path.abspath("deadlock.db")
print(f"DEBUG: Using database at {DB_NAME}")

@contextmanager
def get_db_connection():
    """Context manager for database connection."""
    conn = sqlite3.connect(DB_NAME)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initializes the database with necessary tables."""
    create_matches_table = """
    CREATE TABLE IF NOT EXISTS matches (
        match_id INTEGER PRIMARY KEY,
        start_time INTEGER,
        duration_s INTEGER,
        winning_team INTEGER, -- 0 or 1
        game_mode TEXT,
        region_mode TEXT
    );
    """

    create_player_stats_table = """
    CREATE TABLE IF NOT EXISTS player_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        account_id INTEGER,
        hero_id INTEGER,
        team INTEGER, -- 0 or 1
        net_worth INTEGER,
        kills INTEGER,
        deaths INTEGER,
        assists INTEGER,
        damage_dealt INTEGER,
        healing_done INTEGER,
        FOREIGN KEY (match_id) REFERENCES matches (match_id)
    );
    """
    
    # Index for fast lookups
    create_index_matches_time = "CREATE INDEX IF NOT EXISTS idx_matches_time ON matches(start_time);"
    create_index_player_match = "CREATE INDEX IF NOT EXISTS idx_player_match ON player_stats(match_id);"
    create_index_player_hero = "CREATE INDEX IF NOT EXISTS idx_player_hero ON player_stats(hero_id);"

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(create_matches_table)
        cursor.execute(create_player_stats_table)
        cursor.execute(create_index_matches_time)
        cursor.execute(create_index_player_match)
        cursor.execute(create_index_player_hero)
        conn.commit()
    
    print(f"Database {DB_NAME} initialized successfully.")

if __name__ == "__main__":
    init_db()
