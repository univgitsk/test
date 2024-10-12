import unittest
from unittest.mock import patch
import pandas as pd
from football_data import get_api_response, extract_team_standings, process_season_data  # Replace `your_module_name` with the actual name of your Python file (without .py)

class FootballDataTests(unittest.TestCase):

    @patch('requests.get')
    def test_get_api_response_success(self, mock_get):
        # Mock response data
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "standings": [
                {
                    "table": [
                        {
                            "team": {"name": "Team A"},
                            "playedGames": 10,
                            "won": 6,
                            "draw": 2,
                            "lost": 2,
                            "goalsFor": 20,
                            "goalsAgainst": 10,
                            "goalDifference": 10,
                            "points": 20
                        }
                    ]
                }
            ]
        }

        # Call the function with the mock data
        data = get_api_response("competitions/PL/standings", {"season": 2020})
        self.assertIsNotNone(data)
        self.assertIn('standings', data)

    @patch('requests.get')
    def test_get_api_response_failure(self, mock_get):
        mock_get.return_value.status_code = 404
        
        # Call the function
        result = get_api_response("competitions/PL/standings", {"season": 2020})
        
        # Assertions
        self.assertIsNone(result)

    def test_extract_team_standings(self):
        # Mock the data for extraction
        mock_data = {
            "standings": [
                {
                    "table": [
                        {
                            "team": {"name": "Team B"},
                            "playedGames": 12,
                            "won": 7,
                            "draw": 3,
                            "lost": 2,
                            "goalsFor": 25,
                            "goalsAgainst": 15,
                            "goalDifference": 10,
                            "points": 24
                        }
                    ]
                }
            ]
        }

        df = extract_team_standings(mock_data, 2020)

        self.assertIsNotNone(df)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["Team"], "Team B")

    def test_extract_team_standings_no_data(self):
        # Mock the response with no standings
        mock_data = {}

        df = extract_team_standings(mock_data, 2020)

        self.assertTrue(df.empty)

if __name__ == '__main__':
    unittest.main()
