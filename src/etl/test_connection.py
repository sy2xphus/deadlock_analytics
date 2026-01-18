import requests
import json
import os
from datetime import datetime

# Configuration
API_BASE_URL = "https://api.deadlock-api.com"
RAW_DATA_PATH = os.path.join("data", "raw")

def fetch_active_matches():
    """Fetches currently active matches."""
    url = f"{API_BASE_URL}/v1/matches/active"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_to_raw(data, filename):
    """Saves data to a JSON file in the raw directory."""
    os.makedirs(RAW_DATA_PATH, exist_ok=True)
    filepath = os.path.join(RAW_DATA_PATH, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filepath}")

def main():
    print("Fetching active matches...")
    matches = fetch_active_matches()
    
    if matches:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"active_matches_{timestamp}.json"
        save_to_raw(matches, filename)
        print(f"Successfully fetched {len(matches)} matches.")
    else:
        print("Failed to fetch matches.")

if __name__ == "__main__":
    main()
