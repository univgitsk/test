import requests
import pandas as pd

# Constants
API_BASE_URL = "https://api.football-data.org/v4/"
API_TOKEN = "12abfbaacdab48bc8948ed6061925e1f"
HEADERS = {"X-Auth-Token": API_TOKEN}

def get_api_response(endpoint, params=None):
    # Fetch the data from the API endpoint
    response = requests.get(f"{API_BASE_URL}{endpoint}", headers=HEADERS, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch data (Status code: {response.status_code})")
        return None

def extract_team_standings(data, season):
    # Extract the team standing and the fetch the KPIs
    if not data or 'standings' not in data:
        return pd.DataFrame()
    
    teams = [{
        "Team": entry['team']['name'],
        "PlayedGames": entry['playedGames'],
        "Won": entry['won'],
        "Drawn": entry['draw'],
        "Lost": entry['lost'],
        "GoalsFor": entry['goalsFor'],
        "GoalsAgainst": entry['goalsAgainst'],
        "GoalDifference": entry['goalDifference'],
        "Points": entry['points'],
        "Year": season
    } for entry in data['standings'][0]['table']]
    
    return pd.DataFrame(teams)

def save_to_csv(df, season):
    # Export the data to csv files
    file_name = f'premier_league_standings_{season}.csv'
    df.to_csv(file_name, index=False)
    print(f"Data for {season} saved to {file_name}")

def process_season_data(season):
    # Process the data after fetching it and store the transformed data in csv file
    endpoint = "competitions/PL/standings"
    params = {"season": season}
    data = get_api_response(endpoint, params)
    df = extract_team_standings(data, season)
    if not df.empty:
        save_to_csv(df, season)

if __name__ == "__main__":
    for season in range(2020, 2024):
        process_season_data(season)
