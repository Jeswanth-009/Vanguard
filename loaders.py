"""
Data Loaders for GRID Esports API
Handles fetching data from GRID Stats Feed API and Mock Generators
"""
from typing import Dict, List, Any, Optional
import requests
import mock_data
import datetime
import random

# GRID API Endpoints (Open Access)
GRID_CENTRAL_DATA_URL = "https://api-op.grid.gg/central-data/graphql"  # Static data: teams, tournaments
GRID_STATS_FEED_URL = "https://api-op.grid.gg/statistics-feed/graphql"  # Aggregated statistics


class GridDataLoader:
    """
    Main data loader for esports match data
    Supports both League of Legends and VALORANT
    Uses GRID Stats Feed API for real aggregated statistics + simulated match details
    """
    
    def __init__(self, api_key: Optional[str] = None, use_mock: bool = True):
        """
        Initialize the data loader
        
        Args:
            api_key: GRID API key (not used in mock mode)
            use_mock: Whether to use mock data or live API calls
        """
        self.api_key = api_key
        self.use_mock = use_mock
        
        if not use_mock and not api_key:
            raise ValueError("API key required when not using mock data")
    
    def load_lol_matches(self, team_name: str = "Cloud9", num_matches: int = 10) -> List[Dict[str, Any]]:
        """Load League of Legends match data"""
        if self.use_mock:
            return mock_data.get_lol_mock_data(team_name, num_matches)
        else:
            return self._fetch_from_grid_api(team_name, num_matches, "lol")
    
    def load_valorant_matches(self, team_name: str = "Cloud9", num_matches: int = 10) -> List[Dict[str, Any]]:
        """Load VALORANT match data"""
        if self.use_mock:
            return mock_data.get_valorant_mock_data(team_name, num_matches)
        else:
            return self._fetch_from_grid_api(team_name, num_matches, "valorant")
    
    def _fetch_from_grid_api(self, team_name: str, num_matches: int, game_type: str) -> List[Dict]:
        """
        Fetch data from GRID Stats Feed API
        
        For now, requires direct team ID input (format: "TeamID:83")
        Team name search is disabled due to Central Data API schema complexity
        """
        if not self.api_key:
            raise ValueError("API Key missing.")

        print(f"🔄 Fetching {game_type.upper()} statistics from GRID Stats Feed API...")
        
        # Extract team ID from input
        if team_name.startswith("TeamID:"):
            team_id = team_name.replace("TeamID:", "")
            print(f"✅ Using Team ID: {team_id}")
        else:
            # Team name search disabled - require team ID
            print(f"❌ Team name search not available - please use Team ID")
            print(f"💡 Tip: Check 'Use Team ID instead of name' and enter team ID (e.g., 83)")
            print("⚠️  Falling back to mock data...")
            return mock_data.get_lol_mock_data(team_name, num_matches) if game_type == "lol" else mock_data.get_valorant_mock_data(team_name, num_matches)
        
        # Fetch aggregated statistics from Stats Feed
        stats_data = self._fetch_team_statistics(team_id, game_type)
        if not stats_data:
            print("⚠️  No statistics available. Falling back to mock data...")
            return mock_data.get_lol_mock_data(team_name, num_matches) if game_type == "lol" else mock_data.get_valorant_mock_data(team_name, num_matches)
        
        # Transform to matches - use a clean team name
        display_name = f"Team {team_id}" if team_name.startswith("TeamID:") else team_name
        matches = self._transform_stats_to_matches(stats_data, display_name, num_matches, game_type)
        return matches
    
    def _get_team_id(self, team_name: str, game_type: str) -> Optional[str]:
        """Search for team in Central Data Feed and return ID"""
        title_ids = {"lol": 22, "valorant": 29}
        
        # Use correct GRID schema: teams (not allTeams)
        query = """
        query SearchTeam($titleId: Int!) {
          teams(titleId: $titleId, first: 100) {
            id
            name
          }
        }
        """
        
        try:
            response = requests.post(
                GRID_CENTRAL_DATA_URL,
                json={"query": query, "variables": {"titleId": title_ids[game_type]}},
                headers={"x-api-key": self.api_key, "Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                print(f"❌ Central Data API Error: {data['errors']}")
                return None
            
            # Search for team in results
            teams = data.get("data", {}).get("teams", [])
            for team in teams:
                if team_name.lower() in team["name"].lower():
                    print(f"✅ Found team: {team['name']} (ID: {team['id']})")
                    return team["id"]
            
            print(f"⚠️  Team '{team_name}' not found in {len(teams)} available teams")
        except Exception as e:
            print(f"❌ Error searching for team: {e}")
        
        return None
    
    def _fetch_team_statistics(self, team_id: str, game_type: str) -> Optional[Dict]:
        """Fetch aggregated statistics from Stats Feed API"""
        
        # Use exact GRID Stats Feed query format
        query = """
        query TeamStatisticsForLastThreeMonths($teamId: ID!) {
          teamStatistics(teamId: $teamId, filter: { timeWindow: LAST_3_MONTHS }) {
            id
            aggregationSeriesIds
            series {
              count
              kills {
                sum
                min
                max
                avg
              }
            }
            game {
              count
              kills {
                sum
                min
                max
                avg
              }
              deaths {
                sum
                avg
              }
              wins {
                value
                count
                percentage
                streak {
                  min
                  max
                  current
                }
              }
            }
            segment {
              type
              count
              deaths {
                sum
                min
                max
                avg
              }
            }
          }
        }
        """
        
        try:
            print(f"📊 Fetching statistics from Stats Feed (Team ID: {team_id})...")
            response = requests.post(
                GRID_STATS_FEED_URL,
                json={"query": query, "variables": {"teamId": team_id}},
                headers={"x-api-key": self.api_key, "Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                print(f"❌ Stats Feed API Error: {data['errors']}")
                return None
            
            stats = data.get("data", {}).get("teamStatistics")
            if stats and stats["game"]["count"] > 0:
                wins_data = stats["game"]["wins"]
                win_pct = next((w["percentage"] for w in wins_data if w["value"] == True), 50.0)
                print(f"✅ Stats: {stats['series']['count']} series, {stats['game']['count']} games, {win_pct:.1f}% win rate")
                return stats
                
        except Exception as e:
            print(f"❌ Error fetching statistics: {e}")
        
        return None
    
    def _transform_stats_to_matches(self, stats_data: Dict, team_name: str, num_matches: int, game_type: str) -> List[Dict]:
        """
        Transform GRID Stats into match format
        Uses real win rates + generates realistic match details
        """
        print("🔄 Generating matches with real GRID statistics...")
        
        # Extract real statistics
        game_stats = stats_data["game"]
        wins_data = game_stats["wins"]
        real_win_pct = next((w["percentage"] for w in wins_data if w["value"] == True), 50.0)
        
        print(f"📈 Using real win rate: {real_win_pct:.1f}%")
        
        # Generate matches with real win distribution
        from mock_data import MockDataGenerator
        mock_gen = MockDataGenerator()
        
        # Generate all matches at once with the correct function signature
        if game_type == "lol":
            matches = mock_gen.generate_lol_match_data(team_name, num_matches)
        else:
            matches = mock_gen.generate_valorant_match_data(team_name, num_matches)
        
        # Now apply real win rate distribution
        num_wins_expected = int(len(matches) * (real_win_pct / 100.0))
        num_wins_applied = 0
        
        for match in matches:
            if num_wins_applied < num_wins_expected:
                match["won"] = True
                num_wins_applied += 1
            else:
                match["won"] = False
        
        # Shuffle to randomize win distribution
        import random
        random.shuffle(matches)
        
        print(f"✅ Generated {len(matches)} matches with real {real_win_pct:.1f}% win rate")
        return matches
