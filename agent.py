"""
LLM-Powered Agentic Scout
Generates ruthless coaching insights and win condition strategies
"""
import os
from typing import Dict, Any, Optional
import json


def generate_scouting_report(stats_dict: Dict[str, Any], game_type: str, llm_provider: str = "openai") -> str:
    """
    Generate an AI-powered scouting report using an LLM agent
    
    Args:
        stats_dict: Statistical analysis from the analyzer
        game_type: "lol" or "valorant"
        llm_provider: "openai", "gemini", "openrouter", or "mock" for testing
        
    Returns:
        Formatted scouting report with win condition strategy
    """
    
    # Construct the prompt
    prompt = _build_scout_prompt(stats_dict, game_type)
    
    # Call the appropriate LLM
    if llm_provider == "mock" or not os.getenv("OPENAI_API_KEY"):
        return _generate_mock_report(stats_dict, game_type)
    elif llm_provider == "openai":
        return _call_openai(prompt)
    elif llm_provider == "gemini":
        return _call_gemini(prompt)
    elif llm_provider == "openrouter":
        return _call_openrouter(prompt)
    else:
        raise ValueError(f"Unknown LLM provider: {llm_provider}")


def _build_scout_prompt(stats_dict: Dict[str, Any], game_type: str) -> str:
    """
    Build the LLM prompt with statistical context
    
    Args:
        stats_dict: Statistical analysis dictionary
        game_type: "lol" or "valorant"
        
    Returns:
        Formatted prompt string
    """
    
    # Convert stats to formatted JSON for the prompt
    stats_json = json.dumps(stats_dict, indent=2)
    
    if game_type == "lol":
        prompt = f"""You are a RUTHLESS League of Legends Esports Coach analyzing enemy team data.

Your job is to find EXPLOITABLE WEAKNESSES and craft a precise win condition.

TEAM STATISTICS:
{stats_json}

ANALYSIS REQUIREMENTS:

1. PATTERN RECOGNITION
   - Identify the 3 most CRITICAL patterns in their playstyle
   - Highlight both strengths AND weaknesses (focus on weaknesses)
   
2. JUNGLE ANALYSIS
   - Where does their jungler neglect? (Top/Mid/Bot)
   - Can we exploit their jungle pathing?
   
3. OBJECTIVE CONTROL
   - Are they vulnerable to early dragon steals?
   - Do they give up heralds/barons easily?
   
4. GOLD SCALING
   - Do they fall behind in the mid-game?
   - Can we punish their early game?

5. **THE WIN CONDITION** (MOST IMPORTANT SECTION)
   Based on the data, provide:
   - Their BIGGEST WEAKNESS (be specific)
   - Our COUNTER-STRATEGY (actionable steps)
   - The exact TIMING WINDOW to exploit (e.g., "Between 10-15 minutes")
   - The KEY PLAYERS to target or lanes to pressure

FORMAT YOUR RESPONSE AS:
---
## 🎯 SCOUTING REPORT: [Team Name]

### 📊 Key Patterns
[Your analysis here]

### 🌲 Jungle Pressure Map
[Analysis of jungle proximity]

### 🐉 Objective Control Assessment
[Analysis of dragon/baron control]

### 💰 Economic Trends
[Analysis of gold efficiency]

### 🚨 THE WIN CONDITION
**Their Fatal Flaw:** [Specific weakness]
**Our Counter-Strategy:** [Detailed action plan]
**Timing Window:** [Exact time frame]
**Target Priority:** [Who/what to focus]
---

Be DIRECT. Be RUTHLESS. Be ACTIONABLE."""

    else:  # VALORANT
        prompt = f"""You are a RUTHLESS VALORANT Esports Coach analyzing enemy team data.

Your job is to find EXPLOITABLE WEAKNESSES and craft a precise win condition.

TEAM STATISTICS:
{stats_json}

ANALYSIS REQUIREMENTS:

1. PATTERN RECOGNITION
   - Identify the 3 most CRITICAL patterns in their playstyle
   - Highlight both strengths AND weaknesses (focus on weaknesses)
   
2. OPENING DUELS
   - Are they weak in early fights?
   - Do they lose when they DON'T get first blood?
   
3. SITE BIAS
   - Which site do they over-commit to?
   - Can we bait them into their comfort zone and counter?
   
4. ECONOMY DISCIPLINE
   - Are they predictable on eco rounds?
   - Do they force-buy recklessly?

5. **THE WIN CONDITION** (MOST IMPORTANT SECTION)
   Based on the data, provide:
   - Their BIGGEST WEAKNESS (be specific)
   - Our COUNTER-STRATEGY (actionable steps)
   - The MAP AREAS to exploit (e.g., "A-Main control")
   - The ROUND TYPES where they're vulnerable (Eco/Force/Full)

FORMAT YOUR RESPONSE AS:
---
## 🎯 SCOUTING REPORT: [Team Name]

### 📊 Key Patterns
[Your analysis here]

### ⚔️ Opening Engagement Analysis
[Analysis of first blood stats]

### 🗺️ Site Attack Tendencies
[Analysis of site bias]

### 💳 Economic Discipline
[Analysis of eco/force buy patterns]

### 🚨 THE WIN CONDITION
**Their Fatal Flaw:** [Specific weakness]
**Our Counter-Strategy:** [Detailed action plan]
**Map Control Focus:** [Which areas to dominate]
**Round Type Exploit:** [When they're weakest]
---

Be DIRECT. Be RUTHLESS. Be ACTIONABLE."""

    return prompt


def _call_openai(prompt: str) -> str:
    """
    Call OpenAI API for report generation
    
    Args:
        prompt: The constructed prompt
        
    Returns:
        LLM-generated scouting report
    """
    try:
        from openai import OpenAI
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "⚠️ ERROR: OPENAI_API_KEY not found in environment variables. Using mock report."
        
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except ImportError:
        return "⚠️ ERROR: openai package not installed. Run: pip install openai"
    except Exception as e:
        return f"⚠️ ERROR calling OpenAI: {str(e)}\n\nUsing mock report instead."


def _call_gemini(prompt: str) -> str:
    """
    Call Google Gemini API for report generation
    
    Args:
        prompt: The constructed prompt
        
    Returns:
        LLM-generated scouting report
    """
    try:
        import google.generativeai as genai
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "⚠️ ERROR: GOOGLE_API_KEY not found in environment variables. Using mock report."
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        response = model.generate_content(prompt)
        return response.text
    
    except ImportError:
        return "⚠️ ERROR: google-generativeai not installed. Run: pip install google-generativeai"
    except Exception as e:
        return f"⚠️ ERROR calling Gemini: {str(e)}\n\nUsing mock report instead."


def _call_openrouter(prompt: str) -> str:
    """
    Call OpenRouter API (Google Gemma 3 27B free tier)
    
    Args:
        prompt: The constructed prompt
        
    Returns:
        LLM-generated scouting report
    """
    try:
        import requests
        
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return "⚠️ ERROR: OPENROUTER_API_KEY not found in environment variables. Using mock report."
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "google/gemma-3-27b-it:free",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        return data["choices"][0]["message"]["content"]
    
    except ImportError:
        return "⚠️ ERROR: requests not installed. Run: pip install requests"
    except Exception as e:
        return f"⚠️ ERROR calling OpenRouter: {str(e)}\n\nUsing mock report instead."


def _generate_mock_report(stats_dict: Dict[str, Any], game_type: str) -> str:
    """
    Generate a mock scouting report for testing without LLM API
    
    Args:
        stats_dict: Statistical analysis dictionary
        game_type: "lol" or "valorant"
        
    Returns:
        Mock scouting report
    """
    
    team_name = stats_dict.get("team_name", "Unknown Team")
    
    if game_type == "lol":
        jungle_data = stats_dict.get("jungle_proximity", {})
        objective_data = stats_dict.get("objective_control", {})
        gold_data = stats_dict.get("gold_efficiency", {})
        
        weakest_lane = min(
            [("Top", jungle_data.get("top_lane_percent", 0)),
             ("Mid", jungle_data.get("mid_lane_percent", 0)),
             ("Bot", jungle_data.get("bot_lane_percent", 0))],
            key=lambda x: x[1]
        )[0]
        
        first_dragon_rate = objective_data.get("first_dragon_rate", 0)
        gold_at_15 = gold_data.get("gold_diff_at_15min", 0)
        
        return f"""---
## 🎯 SCOUTING REPORT: {team_name}

### 📊 Key Patterns

**Win Rate:** {stats_dict.get("win_rate", 0):.1f}% ({stats_dict.get("matches_analyzed", 0)} matches analyzed)

1. **Jungle Pathing is PREDICTABLE** - Heavy focus on certain lanes leaves others vulnerable
2. **Early Objective Control is {'ELITE' if first_dragon_rate > 70 else 'INCONSISTENT'}** - {first_dragon_rate:.0f}% first dragon rate
3. **Mid-Game Scaling Shows {'STRENGTH' if gold_at_15 > 0 else 'WEAKNESS'}** - {int(gold_at_15):+d} gold @ 15min

### 🌲 Jungle Pressure Map

**Lane Distribution:**
- Top Lane: {jungle_data.get("top_lane_percent", 0):.1f}%
- Mid Lane: {jungle_data.get("mid_lane_percent", 0):.1f}%
- Bot Lane: {jungle_data.get("bot_lane_percent", 0):.1f}%

**⚠️ CRITICAL INSIGHT:** {weakest_lane} lane receives the LEAST jungle attention ({min(jungle_data.get("top_lane_percent", 0), jungle_data.get("mid_lane_percent", 0), jungle_data.get("bot_lane_percent", 0)):.1f}%). This is an exploitable weakness.

### 🐉 Objective Control Assessment

**First Dragon Control:** {first_dragon_rate:.1f}%
**Overall Dragon Control:** {objective_data.get("overall_dragon_rate", 0):.1f}%
**Rift Herald Control:** {objective_data.get("herald_control_rate", 0):.1f}%
**Baron Control:** {objective_data.get("baron_control_rate", 0):.1f}%

{'🚨 They STRUGGLE to secure early objectives - contest every dragon spawn!' if first_dragon_rate < 50 else '✅ Strong early objective control - must deny vision and contest aggressively.'}

### 💰 Economic Trends

**Gold @ 10min:** {int(gold_data.get("gold_diff_at_10min", 0)):+d}
**Gold @ 15min:** {int(gold_data.get("gold_diff_at_15min", 0)):+d}
**Gold @ 20min:** {int(gold_data.get("gold_diff_at_20min", 0)):+d}

{'🚨 They bleed gold in the mid-game - extend games and scale!' if gold_at_15 < 0 else '⚠️ They accelerate leads - must survive early game and prevent snowball.'}

### 🚨 THE WIN CONDITION

**Their Fatal Flaw:** {weakest_lane} lane is ABANDONED by their jungler ({min(jungle_data.get("top_lane_percent", 0), jungle_data.get("mid_lane_percent", 0), jungle_data.get("bot_lane_percent", 0)):.1f}% presence). {'Early objective control is weak.' if first_dragon_rate < 50 else 'They over-commit to objectives - can be baited.'}

**Our Counter-Strategy:**
1. **Camp {weakest_lane} Lane** - Set up repeated ganks in the 8-15 minute window
2. **Contest Every Drake** - Their {first_dragon_rate:.0f}% first dragon rate means we can steal early momentum
3. {'**Survive to 15 Minutes** - They lose gold leads, we scale better' if gold_at_15 < 0 else '**Punish Their Early Aggression** - Force skirmishes before they establish vision control'}

**Timing Window:** **Minutes 8-15** - Their jungler is predictable, and their macro is weakest here.

**Target Priority:**
1. {weakest_lane} laner (most isolated)
2. Contest dragon at 5:00, 10:00, 15:00 spawns
3. Deny vision around Baron pit after 20:00

---
*Generated by Vanguard AI Scout | "Moneyball for Esports"*
"""

    else:  # VALORANT
        opening_data = stats_dict.get("opening_duel_stats", {})
        site_data = stats_dict.get("site_bias_stats", {})
        eco_data = stats_dict.get("economy_stats", {})
        
        fb_rate = opening_data.get("first_blood_rate", 0)
        favorite_site = site_data.get("favorite_site", "A")
        eco_conversion = eco_data.get("eco_conversion_rate", 0)
        
        return f"""---
## 🎯 SCOUTING REPORT: {team_name}

### 📊 Key Patterns

**Match Win Rate:** {stats_dict.get("match_win_rate", 0):.1f}% | **Round Win Rate:** {stats_dict.get("round_win_rate", 0):.1f}%
**Matches Analyzed:** {stats_dict.get("matches_analyzed", 0)} | **Total Rounds:** {stats_dict.get("total_rounds_played", 0)}

1. **Opening Duels are {'ELITE' if fb_rate > 55 else 'INCONSISTENT'}** - {fb_rate:.1f}% first blood rate
2. **HEAVILY PREDICTABLE Site Bias** - {favorite_site}-Site is attacked {site_data.get(f"site_{favorite_site}_percent", 0):.0f}% of the time
3. **Eco Rounds are {'DANGEROUS' if eco_conversion > 20 else 'PREDICTABLE'}** - {eco_conversion:.1f}% win rate on saves

### ⚔️ Opening Engagement Analysis

**First Blood Rate:** {fb_rate:.1f}%
**First Blood Conversion:** {opening_data.get("first_blood_conversion", 0):.1f}%

**Rounds Won WITH First Blood:** {opening_data.get("rounds_won_with_fb", 0)}
**Rounds Won WITHOUT First Blood:** {opening_data.get("rounds_won_without_fb", 0)}

{'🚨 They CRUMBLE when losing the opening duel - aggressive early peaks will tilt them!' if fb_rate < 50 else '⚠️ Strong early fraggers - must trade carefully and play post-plant.'}

### 🗺️ Site Attack Tendencies

**Site A Attacks:** {site_data.get("site_A_percent", 0):.1f}% (Win Rate: {site_data.get("site_A_winrate", 0):.1f}%)
**Site B Attacks:** {site_data.get("site_B_percent", 0):.1f}% (Win Rate: {site_data.get("site_B_winrate", 0):.1f}%)
**Site C Attacks:** {site_data.get("site_C_percent", 0):.1f}% (Win Rate: {site_data.get("site_C_winrate", 0):.1f}%)

**⚠️ EXPLOITABLE BIAS:** They attack **{favorite_site}-Site {site_data.get(f"site_{favorite_site}_percent", 0):.0f}%** of the time. Stack {favorite_site} and force rotations.

### 💳 Economic Discipline

**Eco Round Conversion:** {eco_conversion:.1f}%
**Force Buy Win Rate:** {eco_data.get("force_buy_winrate", 0):.1f}%
**Full Buy Win Rate:** {eco_data.get("full_buy_winrate", 0):.1f}%

{'🚨 They throw away eco rounds - sheriffs and spectres shut them down!' if eco_conversion < 15 else '⚠️ Dangerous on eco - must respect their aim and positioning.'}

### 🚨 THE WIN CONDITION

**Their Fatal Flaw:** OVER-COMMITMENT to **{favorite_site}-Site** ({site_data.get(f"site_{favorite_site}_percent", 0):.0f}% of attacks). {'They cannot win without first blood.' if fb_rate < 50 else 'Predictable eco-round strats.'}

**Our Counter-Strategy:**
1. **Stack {favorite_site}-Site Early** - Put 3 players on {favorite_site} by default, they'll walk into the trap
2. **Challenge Opening Duels Aggressively** - {('Take first blood and they fall apart' if fb_rate < 50 else 'Trade 1-for-1 and deny their entry fragger')}
3. **{'Punish Eco Rounds Relentlessly' if eco_conversion < 15 else 'Respect Their Aim on Ecos'}** - {('Sheriff headshots are free - push aggressively' if eco_conversion < 15 else 'Play default and avoid risky peeks')}

**Map Control Focus:** 
- **Primary:** {favorite_site}-Site default setup (they WILL come here)
- **Secondary:** Mid control to fast-rotate when they finally hit other sites

**Round Type Exploit:**
- **Eco Rounds:** {'Push aggressively, they have no answer' if eco_conversion < 15 else 'Play disciplined, they CAN upset'}
- **Full Buy Rounds:** {('Deny their entry fragger and they crumble' if fb_rate < 50 else 'Trade carefully and play post-plant')}

---
*Generated by Vanguard AI Scout | "Moneyball for Esports"*
"""

    return "Error generating report."


# Convenience function for direct use
def scout_team(stats: Dict[str, Any], game: str) -> str:
    """Quick function to generate a scouting report"""
    return generate_scouting_report(stats, game, llm_provider="mock")
