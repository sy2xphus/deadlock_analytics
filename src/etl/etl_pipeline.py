import json
import os
import sys
import random
import sqlite3
from typing import List, Dict, Any

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.db.database import get_db_connection, init_db

DATA_RAW_DIR = os.path.join("data", "raw")

def generate_mock_stats(match_duration_s: int, is_winner: bool) -> Dict[str, int]:
    """Generates realistic mock stats for a player."""
    win_factor = 1.2 if is_winner else 0.8
    duration_factor = match_duration_s / 1800.0  # Normalized to 30 mins

    kills = int(random.randint(0, 15) * win_factor * duration_factor)
    deaths = int(random.randint(0, 15) * (1/win_factor) * duration_factor)
    assists = int(random.randint(0, 20) * win_factor * duration_factor)
    
    net_worth = int(random.randint(5000, 25000) * win_factor * duration_factor)
    damage = int(random.randint(5000, 40000) * win_factor * duration_factor)
    healing = int(random.randint(0, 10000) * duration_factor)

    return {
        "kills": kills,
        "deaths": deaths,
        "assists": assists,
        "net_worth": net_worth,
        "damage_dealt": damage,
        "healing_done": healing
    }

def process_match(match_data: Dict[str, Any]) -> None:
    """Processes a single match and inserts into DB."""
    match_id = match_data.get("match_id")
    start_time = match_data.get("start_time")
    
    # Mock Missing Data
    if match_data.get("duration_s") is None:
        duration = random.randint(900, 3600) # 15 to 60 mins
    else:
        duration = match_data.get("duration_s")
        
    if match_data.get("winning_team") is None:
        winner = random.choice([0, 1])
    else:
        winner = match_data.get("winning_team")
        
    game_mode = match_data.get("game_mode_parsed", "Unknown")
    region = match_data.get("region_mode_parsed", "Unknown")

    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Insert Match
        cursor.execute("""
            INSERT OR IGNORE INTO matches (match_id, start_time, duration_s, winning_team, game_mode, region_mode)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (match_id, start_time, duration, winner, game_mode, region))
        
        # Process Players
        players = match_data.get("players", [])
        for p in players:
            account_id = p.get("account_id")
            hero_id = p.get("hero_id")
            team = p.get("team")
            
            # Mock Stats
            stats = generate_mock_stats(duration, team == winner)
            
            cursor.execute("""
                INSERT OR REPLACE INTO player_stats (match_id, account_id, hero_id, team, net_worth, kills, deaths, assists, damage_dealt, healing_done)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (match_id, account_id, hero_id, team, stats['net_worth'], stats['kills'], stats['deaths'], stats['assists'], stats['damage_dealt'], stats['healing_done']))
        
        conn.commit()
        # print(f"Processed match {match_id}")

def load_data():
    """Iterates through raw data files and processes them."""
    print("Starting ETL Process...")
    init_db()
    
    files = [f for f in os.listdir(DATA_RAW_DIR) if f.endswith('.json')]
    total_matches = 0
    
    for filename in files:
        filepath = os.path.join(DATA_RAW_DIR, filename)
        print(f"Reading {filepath}...")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                if isinstance(data, list):
                    for match in data:
                        process_match(match)
                        total_matches += 1
                elif isinstance(data, dict): # Single match file
                     process_match(data)
                     total_matches += 1
                     
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    print(f"ETL Complete. Processed {total_matches} matches.")

if __name__ == "__main__":
    load_data()
