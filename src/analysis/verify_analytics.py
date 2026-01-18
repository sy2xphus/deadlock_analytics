import sys
import os
import pandas as pd

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.analysis.analytics import DeadlockAnalyzer

def verify():
    print("Verifying Analytics Module...")
    analyzer = DeadlockAnalyzer()
    
    print("\n--- Hypothesis 1: Winrate by Duration ---")
    df1 = analyzer.get_winrate_by_duration()
    print(df1.head())
    if df1.empty:
        print("FAIL: DataFrame is empty")
    else:
        print(f"SUCCESS: Retrieved {len(df1)} rows")

    print("\n--- Hypothesis 2: Net Worth Correlation ---")
    df2 = analyzer.get_net_worth_correlation()
    print(df2.head())
    if df2.empty:
        print("FAIL: DataFrame is empty")
    else:
         print(f"SUCCESS: Retrieved {len(df2)} rows")

    print("\n--- Hypothesis 3: Meta Rating ---")
    df3 = analyzer.get_meta_rating()
    print(df3.head())
    if df3.empty:
        print("FAIL: DataFrame is empty")
    else:
         print(f"SUCCESS: Retrieved {len(df3)} rows")

if __name__ == "__main__":
    verify()
