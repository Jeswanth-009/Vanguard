"""
Analysis Engines for League of Legends and VALORANT
Provides "Moneyball-style" statistical insights
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
from collections import Counter


class LolAnalyzer:
    """
    League of Legends Analysis Engine
    Calculates jungle proximity, objective control, and gold efficiency
    """
    
    def __init__(self, matches: List[Dict[str, Any]]):
        """
        Initialize analyzer with match data
        
        Args:
            matches: List of LoL match dictionaries
        """
        self.matches = matches
        self.team_name = matches[0]["team"] if matches else "Unknown"
    
    def calculate_jungle_proximity(self) -> Dict[str, Any]:
        """
        Calculate where the jungler spends the most time (Top/Mid/Bot)
        
        Returns:
            Dictionary with lane percentages and heatmap data
        """
        all_positions = []
        
        for match in self.matches:
            all_positions.extend(match.get("jungle_positions", []))
        
        if not all_positions:
            return {
                "top_lane_percent": 0,
                "mid_lane_percent": 0,
                "bot_lane_percent": 0,
                "positions": []
            }
        
        # Count lane presence
        lane_counter = Counter(pos["lane"] for pos in all_positions)
        total = len(all_positions)
        
        # Calculate percentages
        top_percent = (lane_counter.get("Top", 0) / total) * 100
        mid_percent = (lane_counter.get("Mid", 0) / total) * 100
        bot_percent = (lane_counter.get("Bot", 0) / total) * 100
        
        # Prepare heatmap data
        heatmap_data = {
            "x": [pos["x"] for pos in all_positions],
            "y": [pos["y"] for pos in all_positions],
            "lane": [pos["lane"] for pos in all_positions]
        }
        
        return {
            "top_lane_percent": round(top_percent, 1),
            "mid_lane_percent": round(mid_percent, 1),
            "bot_lane_percent": round(bot_percent, 1),
            "total_samples": total,
            "heatmap_data": heatmap_data,
            "insight": f"Jungler focuses {max(top_percent, mid_percent, bot_percent):.1f}% on {max(lane_counter, key=lane_counter.get)} lane"
        }
    
    def calculate_objective_control(self) -> Dict[str, Any]:
        """
        Calculate % of First Dragons and Rift Heralds taken
        
        Returns:
            Dictionary with objective control statistics
        """
        first_dragons = 0
        first_dragons_taken = 0
        
        total_dragons = 0
        team_dragons = 0
        
        total_heralds = 0
        team_heralds = 0
        
        for match in self.matches:
            # First Dragon analysis
            dragons = match.get("dragons", [])
            if dragons:
                first_dragons += 1
                if dragons[0]["team"] == self.team_name:
                    first_dragons_taken += 1
            
            # All dragons
            for dragon in dragons:
                total_dragons += 1
                if dragon["team"] == self.team_name:
                    team_dragons += 1
            
            # Heralds
            heralds = match.get("heralds", [])
            for herald in heralds:
                total_heralds += 1
                if herald["team"] == self.team_name:
                    team_heralds += 1
        
        first_dragon_rate = (first_dragons_taken / first_dragons * 100) if first_dragons > 0 else 0
        overall_dragon_rate = (team_dragons / total_dragons * 100) if total_dragons > 0 else 0
        herald_rate = (team_heralds / total_heralds * 100) if total_heralds > 0 else 0
        
        # Baron analysis
        total_barons = 0
        team_barons = 0
        
        for match in self.matches:
            barons = match.get("barons", [])
            for baron in barons:
                total_barons += 1
                if baron["team"] == self.team_name:
                    team_barons += 1
        
        baron_rate = (team_barons / total_barons * 100) if total_barons > 0 else 0
        
        return {
            "first_dragon_rate": round(first_dragon_rate, 1),
            "overall_dragon_rate": round(overall_dragon_rate, 1),
            "herald_control_rate": round(herald_rate, 1),
            "baron_control_rate": round(baron_rate, 1),
            "total_dragons": total_dragons,
            "team_dragons": team_dragons,
            "total_heralds": total_heralds,
            "team_heralds": team_heralds,
            "total_barons": total_barons,
            "team_barons": team_barons,
            "insight": f"{'DOMINATES' if first_dragon_rate > 70 else 'STRUGGLES WITH'} early objective control ({first_dragon_rate:.0f}% first dragon rate)"
        }
    
    def calculate_gold_efficiency(self) -> Dict[str, Any]:
        """
        Calculate team gold difference at key timings (10, 15, 20 minutes)
        
        Returns:
            Dictionary with gold efficiency metrics
        """
        gold_at_10 = []
        gold_at_15 = []
        gold_at_20 = []
        
        for match in self.matches:
            gold_updates = match.get("gold_updates", [])
            
            # Find closest gold update to each timing
            for update in gold_updates:
                timestamp = update["timestamp"]
                gold_diff = update["gold_difference"]
                
                if 9 * 60 <= timestamp <= 11 * 60:
                    gold_at_10.append(gold_diff)
                elif 14 * 60 <= timestamp <= 16 * 60:
                    gold_at_15.append(gold_diff)
                elif 19 * 60 <= timestamp <= 21 * 60:
                    gold_at_20.append(gold_diff)
        
        avg_gold_10 = np.mean(gold_at_10) if gold_at_10 else 0
        avg_gold_15 = np.mean(gold_at_15) if gold_at_15 else 0
        avg_gold_20 = np.mean(gold_at_20) if gold_at_20 else 0
        
        # Calculate gold growth rate
        growth_rate = 0
        if avg_gold_10 != 0 and avg_gold_15 != 0:
            growth_rate = ((avg_gold_15 - avg_gold_10) / 5) * 60  # Gold per minute
        
        return {
            "gold_diff_at_10min": round(avg_gold_10, 0),
            "gold_diff_at_15min": round(avg_gold_15, 0),
            "gold_diff_at_20min": round(avg_gold_20, 0),
            "gold_growth_rate": round(growth_rate, 0),
            "samples_at_10": len(gold_at_10),
            "samples_at_15": len(gold_at_15),
            "samples_at_20": len(gold_at_20),
            "insight": f"{'Strong' if avg_gold_15 > 0 else 'Weak'} mid-game scaling ({int(avg_gold_15):+d}g @ 15min)"
        }
    
    def get_complete_analysis(self) -> Dict[str, Any]:
        """
        Get comprehensive analysis combining all metrics
        
        Returns:
            Complete statistical report
        """
        wins = sum(1 for match in self.matches if match["won"])
        total_matches = len(self.matches)
        win_rate = (wins / total_matches * 100) if total_matches > 0 else 0
        
        avg_game_duration = np.mean([match["duration"] for match in self.matches]) if self.matches else 0
        
        return {
            "team_name": self.team_name,
            "matches_analyzed": total_matches,
            "win_rate": round(win_rate, 1),
            "avg_game_duration_minutes": round(avg_game_duration / 60, 1),
            "jungle_proximity": self.calculate_jungle_proximity(),
            "objective_control": self.calculate_objective_control(),
            "gold_efficiency": self.calculate_gold_efficiency()
        }


class ValorantAnalyzer:
    """
    VALORANT Analysis Engine
    Calculates opening duel win%, site bias, and eco conversion rate
    """
    
    def __init__(self, matches: List[Dict[str, Any]]):
        """
        Initialize analyzer with match data
        
        Args:
            matches: List of VALORANT match dictionaries
        """
        self.matches = matches
        self.team_name = matches[0]["team"] if matches else "Unknown"
    
    def calculate_opening_duel_winrate(self) -> Dict[str, Any]:
        """
        Calculate how often the team gets the first kill (5v4 advantage)
        
        Returns:
            Dictionary with first blood statistics
        """
        total_rounds = 0
        team_first_bloods = 0
        rounds_won_with_fb = 0
        rounds_won_without_fb = 0
        
        for match in self.matches:
            for round_data in match.get("rounds", []):
                total_rounds += 1
                
                got_first_blood = round_data["first_blood_team"] == self.team_name
                won_round = round_data["winner"] == self.team_name
                
                if got_first_blood:
                    team_first_bloods += 1
                    if won_round:
                        rounds_won_with_fb += 1
                else:
                    if won_round:
                        rounds_won_without_fb += 1
        
        fb_rate = (team_first_bloods / total_rounds * 100) if total_rounds > 0 else 0
        fb_conversion = (rounds_won_with_fb / team_first_bloods * 100) if team_first_bloods > 0 else 0
        
        return {
            "first_blood_rate": round(fb_rate, 1),
            "first_blood_conversion": round(fb_conversion, 1),
            "rounds_with_first_blood": team_first_bloods,
            "rounds_won_with_fb": rounds_won_with_fb,
            "rounds_won_without_fb": rounds_won_without_fb,
            "total_rounds": total_rounds,
            "insight": f"{'ELITE' if fb_rate > 55 else 'AVERAGE'} opening duelist ({fb_rate:.1f}% FB rate, {fb_conversion:.1f}% conversion)"
        }
    
    def calculate_site_bias(self) -> Dict[str, Any]:
        """
        Calculate % of times they attack A-Site vs. B-Site vs. C-Site
        
        Returns:
            Dictionary with site attack preferences
        """
        site_attacks = Counter()
        site_wins = Counter()
        
        for match in self.matches:
            for round_data in match.get("rounds", []):
                spike_site = round_data.get("spike_site")
                
                if spike_site:
                    site_attacks[spike_site] += 1
                    
                    if round_data["winner"] == self.team_name:
                        site_wins[spike_site] += 1
        
        total_attacks = sum(site_attacks.values())
        
        site_percentages = {}
        site_win_rates = {}
        
        for site in ["A", "B", "C"]:
            attacks = site_attacks.get(site, 0)
            wins = site_wins.get(site, 0)
            
            site_percentages[f"site_{site}_percent"] = round((attacks / total_attacks * 100), 1) if total_attacks > 0 else 0
            site_win_rates[f"site_{site}_winrate"] = round((wins / attacks * 100), 1) if attacks > 0 else 0
        
        # Find favorite site
        favorite_site = max(site_attacks, key=site_attacks.get) if site_attacks else "Unknown"
        
        return {
            **site_percentages,
            **site_win_rates,
            "total_spike_plants": total_attacks,
            "favorite_site": favorite_site,
            "favorite_site_attacks": site_attacks.get(favorite_site, 0),
            "site_attack_distribution": dict(site_attacks),
            "insight": f"HEAVILY favors {favorite_site}-Site ({site_percentages[f'site_{favorite_site}_percent']:.0f}% of attacks)"
        }
    
    def calculate_eco_conversion(self) -> Dict[str, Any]:
        """
        Calculate % of rounds won when spending < 2000 credits (Eco rounds)
        
        Returns:
            Dictionary with economy statistics
        """
        eco_rounds = 0
        eco_wins = 0
        
        force_rounds = 0  # 2000-3500
        force_wins = 0
        
        full_buy_rounds = 0  # 3500+
        full_buy_wins = 0
        
        for match in self.matches:
            for round_data in match.get("rounds", []):
                team_loadout = round_data["team_loadout_value"]
                won_round = round_data["winner"] == self.team_name
                
                if team_loadout < 2000:
                    eco_rounds += 1
                    if won_round:
                        eco_wins += 1
                
                elif 2000 <= team_loadout < 3500:
                    force_rounds += 1
                    if won_round:
                        force_wins += 1
                
                else:  # Full buy
                    full_buy_rounds += 1
                    if won_round:
                        full_buy_wins += 1
        
        eco_conversion_rate = (eco_wins / eco_rounds * 100) if eco_rounds > 0 else 0
        force_winrate = (force_wins / force_rounds * 100) if force_rounds > 0 else 0
        full_buy_winrate = (full_buy_wins / full_buy_rounds * 100) if full_buy_rounds > 0 else 0
        
        return {
            "eco_conversion_rate": round(eco_conversion_rate, 1),
            "eco_rounds_played": eco_rounds,
            "eco_rounds_won": eco_wins,
            "force_buy_winrate": round(force_winrate, 1),
            "force_rounds_played": force_rounds,
            "full_buy_winrate": round(full_buy_winrate, 1),
            "full_buy_rounds_played": full_buy_rounds,
            "insight": f"{'DANGEROUS' if eco_conversion_rate > 20 else 'PREDICTABLE'} on eco rounds ({eco_conversion_rate:.1f}% win rate)"
        }
    
    def get_complete_analysis(self) -> Dict[str, Any]:
        """
        Get comprehensive analysis combining all metrics
        
        Returns:
            Complete statistical report
        """
        total_matches = len(self.matches)
        wins = sum(1 for match in self.matches if match["won"])
        win_rate = (wins / total_matches * 100) if total_matches > 0 else 0
        
        total_rounds = sum(len(match["rounds"]) for match in self.matches)
        team_rounds_won = sum(
            sum(1 for r in match["rounds"] if r["winner"] == self.team_name)
            for match in self.matches
        )
        round_win_rate = (team_rounds_won / total_rounds * 100) if total_rounds > 0 else 0
        
        return {
            "team_name": self.team_name,
            "matches_analyzed": total_matches,
            "match_win_rate": round(win_rate, 1),
            "round_win_rate": round(round_win_rate, 1),
            "total_rounds_played": total_rounds,
            "opening_duel_stats": self.calculate_opening_duel_winrate(),
            "site_bias_stats": self.calculate_site_bias(),
            "economy_stats": self.calculate_eco_conversion()
        }


def analyze_lol_team(matches: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Convenience function for LoL analysis"""
    analyzer = LolAnalyzer(matches)
    return analyzer.get_complete_analysis()


def analyze_valorant_team(matches: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Convenience function for VALORANT analysis"""
    analyzer = ValorantAnalyzer(matches)
    return analyzer.get_complete_analysis()
