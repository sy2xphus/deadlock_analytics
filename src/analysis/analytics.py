import sqlite3
import pandas as pd
import os
import sys

# Ensure proper path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.db.database import DB_NAME

class DeadlockAnalyzer:
    def __init__(self, db_path=None):
        self.db_path = db_path if db_path else DB_NAME

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_winrate_by_duration(self):
        """
        Hypothesis 1: Late Game Heroes.
        Groups matches by duration buckets and calculates winrate for each hero.
        """
        query = """
        SELECT 
            ps.hero_id,
            CASE 
                WHEN m.duration_s < 900 THEN '0-15m'
                WHEN m.duration_s BETWEEN 900 AND 1500 THEN '15-25m'
                WHEN m.duration_s BETWEEN 1501 AND 2400 THEN '25-40m'
                ELSE '40m+' 
            END as duration_bucket,
            COUNT(*) as matches_played,
            SUM(CASE WHEN ps.team = m.winning_team THEN 1 ELSE 0 END) as wins
        FROM player_stats ps
        JOIN matches m ON ps.match_id = m.match_id
        GROUP BY ps.hero_id, duration_bucket
        """
        with self.get_connection() as conn:
            df = pd.read_sql_query(query, conn)
            
        df['winrate'] = df['wins'] / df['matches_played']
        return df

    def get_net_worth_correlation(self):
        """
        Hypothesis 2: Snowball Effect.
        Analyzes correlation between final Net Worth and Victory.
        """
        query = """
        SELECT 
            m.match_id,
            ps.team,
            CASE WHEN ps.team = m.winning_team THEN 1 ELSE 0 END as is_winner,
            AVG(ps.net_worth) as avg_team_net_worth
        FROM player_stats ps
        JOIN matches m ON ps.match_id = m.match_id
        GROUP BY m.match_id, ps.team
        """
        with self.get_connection() as conn:
            df = pd.read_sql_query(query, conn)
            
        return df

    def get_meta_rating(self):
        """
        Hypothesis 3: Meta Tier List.
        Calculates weighted rating: Pick Rate * Win Rate.
        """
        query = """
        SELECT 
            ps.hero_id,
            COUNT(DISTINCT m.match_id) as matches_appeared,
            SUM(CASE WHEN ps.team = m.winning_team THEN 1 ELSE 0 END) as total_wins,
            COUNT(*) as total_picks
        FROM player_stats ps
        JOIN matches m ON ps.match_id = m.match_id
        GROUP BY ps.hero_id
        """
        with self.get_connection() as conn:
            df = pd.read_sql_query(query, conn)
        
        # Get total matches count for pick rate
        with self.get_connection() as conn:
            total_matches = pd.read_sql_query("SELECT COUNT(*) FROM matches", conn).iloc[0, 0]

        df['pick_rate'] = df['matches_appeared'] / total_matches
        df['win_rate'] = df['total_wins'] / df['total_picks']
        df['meta_score'] = df['pick_rate'] * df['win_rate'] * 100 # Scale to 0-100
        
        return df.sort_values('meta_score', ascending=False)
