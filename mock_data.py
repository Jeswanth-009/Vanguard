"""
Mock Data Generators for League of Legends and VALORANT
Generates realistic game data for testing the scouting system
"""
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any


class MockDataGenerator:
    """Generates realistic mock data for both LoL and VALORANT"""
    
    # LoL Map coordinates (Summoner's Rift is approximately 14820x14881 units)
    LOL_MAP_SIZE = 14820
    
    # VALORANT map coordinates (typical range)
    VALORANT_MAP_SIZE = 100
    
    @staticmethod
    def generate_lol_match_data(team_name: str = "Cloud9", num_matches: int = 10) -> List[Dict[str, Any]]:
        """
        Generate realistic League of Legends match data
        
        Returns:
            List of match dictionaries with timestamped events
        """
        matches = []
        
        for match_id in range(1, num_matches + 1):
            match_date = datetime.now() - timedelta(days=match_id * 3)
            
            # Generate match outcome (70% win rate for testing)
            won = random.random() < 0.7
            game_duration = random.randint(1500, 2400)  # 25-40 minutes in seconds
            
            # Generate kills (with coordinates)
            kills = []
            num_kills = random.randint(15, 35) if won else random.randint(8, 20)
            
            for k in range(num_kills):
                timestamp = random.randint(180, game_duration)  # Kills start after 3 min
                kills.append({
                    "timestamp": timestamp,
                    "killer": team_name,
                    "victim": "Enemy Team",
                    "x": random.randint(1000, MockDataGenerator.LOL_MAP_SIZE - 1000),
                    "y": random.randint(1000, MockDataGenerator.LOL_MAP_SIZE - 1000),
                    "is_first_blood": k == 0
                })
            
            # Generate Dragon kills (Dragons spawn every 5 minutes starting at 5:00)
            dragons = []
            dragon_spawn_times = [300, 600, 900, 1200, 1500, 1800, 2100, 2400]
            dragon_locations = [(9800, 4200)]  # Dragon pit location
            
            for spawn_time in dragon_spawn_times:
                if spawn_time < game_duration and random.random() < 0.8:
                    taken_by_team = random.random() < (0.75 if won else 0.35)
                    dragons.append({
                        "timestamp": spawn_time + random.randint(0, 120),
                        "team": team_name if taken_by_team else "Enemy Team",
                        "dragon_type": random.choice(["Cloud", "Infernal", "Ocean", "Mountain", "Elder"]),
                        "x": dragon_locations[0][0],
                        "y": dragon_locations[0][1]
                    })
            
            # Generate Baron kills (Baron spawns at 20:00)
            barons = []
            if game_duration > 1200:
                num_barons = random.randint(0, 2)
                baron_location = (5200, 10400)  # Baron pit location
                
                for b in range(num_barons):
                    timestamp = random.randint(1200, game_duration - 60)
                    taken_by_team = random.random() < (0.8 if won else 0.2)
                    barons.append({
                        "timestamp": timestamp,
                        "team": team_name if taken_by_team else "Enemy Team",
                        "x": baron_location[0],
                        "y": baron_location[1]
                    })
            
            # Generate Rift Herald kills (spawns at 8:00, despawns at 19:45)
            heralds = []
            if game_duration > 480:
                num_heralds = random.randint(0, 2)
                herald_location = (5200, 10400)
                
                for h in range(num_heralds):
                    timestamp = random.randint(480, min(1185, game_duration))
                    taken_by_team = random.random() < (0.7 if won else 0.3)
                    heralds.append({
                        "timestamp": timestamp,
                        "team": team_name if taken_by_team else "Enemy Team",
                        "x": herald_location[0],
                        "y": herald_location[1]
                    })
            
            # Generate gold updates (every 5 minutes)
            gold_updates = []
            base_gold_advantage = 500 if won else -500
            
            for minute in range(5, game_duration // 60 + 1, 5):
                variance = random.randint(-300, 300)
                gold_diff = base_gold_advantage + variance + (minute * 50)
                gold_updates.append({
                    "timestamp": minute * 60,
                    "team_gold": 15000 + (minute * 300) + gold_diff,
                    "enemy_gold": 15000 + (minute * 300),
                    "gold_difference": gold_diff
                })
            
            # Generate jungle proximity data (tracking jungler position)
            jungle_positions = []
            num_position_samples = random.randint(100, 200)
            
            for _ in range(num_position_samples):
                timestamp = random.randint(0, game_duration)
                # Divide map into lanes: Top (y > 10000), Mid (center), Bot (y < 5000)
                lane_bias = random.random()
                
                if lane_bias < 0.35:  # Top lane
                    x = random.randint(1000, 7000)
                    y = random.randint(10000, 14000)
                    lane = "Top"
                elif lane_bias < 0.70:  # Mid lane
                    x = random.randint(5000, 10000)
                    y = random.randint(5000, 10000)
                    lane = "Mid"
                else:  # Bot lane
                    x = random.randint(8000, 14000)
                    y = random.randint(1000, 5000)
                    lane = "Bot"
                
                jungle_positions.append({
                    "timestamp": timestamp,
                    "x": x,
                    "y": y,
                    "lane": lane
                })
            
            match_data = {
                "match_id": f"LOL_{match_id}",
                "date": match_date.isoformat(),
                "team": team_name,
                "opponent": f"Team_{match_id}",
                "won": won,
                "duration": game_duration,
                "kills": sorted(kills, key=lambda k: k["timestamp"]),
                "dragons": sorted(dragons, key=lambda d: d["timestamp"]),
                "barons": sorted(barons, key=lambda b: b["timestamp"]),
                "heralds": sorted(heralds, key=lambda h: h["timestamp"]),
                "gold_updates": sorted(gold_updates, key=lambda g: g["timestamp"]),
                "jungle_positions": sorted(jungle_positions, key=lambda j: j["timestamp"])
            }
            
            matches.append(match_data)
        
        return matches
    
    @staticmethod
    def generate_valorant_match_data(team_name: str = "Cloud9", num_matches: int = 10) -> List[Dict[str, Any]]:
        """
        Generate realistic VALORANT match data
        
        Returns:
            List of match dictionaries with round-by-round data
        """
        matches = []
        
        for match_id in range(1, num_matches + 1):
            match_date = datetime.now() - timedelta(days=match_id * 2)
            
            # VALORANT is first to 13 rounds
            team_rounds_won = random.randint(13, 15) if random.random() < 0.7 else random.randint(8, 12)
            enemy_rounds_won = 13 if team_rounds_won < 13 else random.randint(8, 12)
            total_rounds = team_rounds_won + enemy_rounds_won
            
            won = team_rounds_won > enemy_rounds_won
            
            # Generate round-by-round data
            rounds = []
            
            for round_num in range(1, total_rounds + 1):
                # Determine round winner
                round_won = random.random() < (team_rounds_won / total_rounds)
                
                # Economy system (Eco, Force Buy, Full Buy)
                if round_num == 1 or round_num == 13:  # Pistol rounds
                    team_loadout_value = 800
                    enemy_loadout_value = 800
                else:
                    # Simulate economy cycles
                    team_loadout_value = random.choice([
                        random.randint(800, 1500),    # Eco (20%)
                        random.randint(2000, 3000),   # Force Buy (30%)
                        random.randint(3500, 5000)    # Full Buy (50%)
                    ])
                    enemy_loadout_value = random.choice([
                        random.randint(800, 1500),
                        random.randint(2000, 3000),
                        random.randint(3500, 5000)
                    ])
                
                # Spike plant location (A, B, or C site - map dependent)
                sites = ["A", "B", "C"]
                spike_planted = random.random() < 0.85
                spike_site = random.choice(sites) if spike_planted else None
                
                # Spike plant coordinates (if planted)
                spike_coords = None
                if spike_planted:
                    if spike_site == "A":
                        spike_coords = {"x": random.randint(20, 35), "y": random.randint(40, 55)}
                    elif spike_site == "B":
                        spike_coords = {"x": random.randint(55, 70), "y": random.randint(20, 35)}
                    else:  # C site
                        spike_coords = {"x": random.randint(40, 55), "y": random.randint(60, 75)}
                
                # First blood
                first_blood_team = random.choice([team_name, "Enemy Team"])
                first_blood_location = {
                    "x": random.randint(10, 90),
                    "y": random.randint(10, 90)
                }
                
                # Determine if this was an eco round for either team
                is_team_eco = team_loadout_value < 2000
                is_enemy_eco = enemy_loadout_value < 2000
                
                round_data = {
                    "round_number": round_num,
                    "winner": team_name if round_won else "Enemy Team",
                    "team_loadout_value": team_loadout_value,
                    "enemy_loadout_value": enemy_loadout_value,
                    "is_team_eco": is_team_eco,
                    "is_enemy_eco": is_enemy_eco,
                    "spike_planted": spike_planted,
                    "spike_site": spike_site,
                    "spike_coords": spike_coords,
                    "first_blood_team": first_blood_team,
                    "first_blood_location": first_blood_location,
                    "round_duration": random.randint(30, 100)  # seconds
                }
                
                rounds.append(round_data)
            
            match_data = {
                "match_id": f"VAL_{match_id}",
                "date": match_date.isoformat(),
                "team": team_name,
                "opponent": f"Team_{match_id}",
                "team_score": team_rounds_won,
                "enemy_score": enemy_rounds_won,
                "won": won,
                "map": random.choice(["Ascent", "Bind", "Haven", "Split", "Icebox", "Breeze", "Fracture"]),
                "rounds": rounds
            }
            
            matches.append(match_data)
        
        return matches


# Convenience functions for quick access
def get_lol_mock_data(team_name: str = "Cloud9", num_matches: int = 10) -> List[Dict[str, Any]]:
    """Quick function to get LoL mock data"""
    return MockDataGenerator.generate_lol_match_data(team_name, num_matches)


def get_valorant_mock_data(team_name: str = "Cloud9", num_matches: int = 10) -> List[Dict[str, Any]]:
    """Quick function to get VALORANT mock data"""
    return MockDataGenerator.generate_valorant_match_data(team_name, num_matches)


if __name__ == "__main__":
    # Test data generation
    print("Generating League of Legends mock data...")
    lol_data = get_lol_mock_data(num_matches=3)
    print(f"Generated {len(lol_data)} LoL matches")
    print(f"Sample match: {lol_data[0]['match_id']}")
    print(f"  - Kills: {len(lol_data[0]['kills'])}")
    print(f"  - Dragons: {len(lol_data[0]['dragons'])}")
    print(f"  - Duration: {lol_data[0]['duration']}s")
    
    print("\nGenerating VALORANT mock data...")
    val_data = get_valorant_mock_data(num_matches=3)
    print(f"Generated {len(val_data)} VALORANT matches")
    print(f"Sample match: {val_data[0]['match_id']}")
    print(f"  - Score: {val_data[0]['team_score']}-{val_data[0]['enemy_score']}")
    print(f"  - Rounds: {len(val_data[0]['rounds'])}")
    print(f"  - Map: {val_data[0]['map']}")
