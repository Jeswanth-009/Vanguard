"""
Vanguard - God-Tier Esports Scouting Report Generator
Cloud9 Hackathon Submission
"""
import streamlit as st
import pandas as pd
from loaders import GridDataLoader
from analyzers import LolAnalyzer, ValorantAnalyzer
from agent import generate_scouting_report
import utils

# Page configuration
st.set_page_config(
    page_title="Vanguard - Esports Scout AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    .main {
        background-color: #0f1419;
    }
    .stMetric {
        background-color: #1a1d23;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #00ff00;
    }
    h1, h2, h3 {
        color: #ffffff;
    }
    .reportview-container .markdown-text-container {
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("🎯 VANGUARD")
st.markdown("### *Moneyball for Esports* - AI-Powered Scouting Reports")
st.markdown("---")

# Sidebar configuration
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/1a1d23/00ff00?text=VANGUARD", use_container_width=True)
    
    st.header("⚙️ Configuration")
    
    # Game selector
    game_type = st.selectbox(
        "Select Game",
        ["League of Legends", "VALORANT"],
        help="Choose which game to analyze"
    )
    
    # Team input
    team_name = st.text_input(
        "Team Name",
        value="Cloud9",
        help="Enter the team name to analyze"
    )
    
    # Number of matches
    num_matches = st.slider(
        "Number of Matches",
        min_value=5,
        max_value=20,
        value=10,
        help="How many recent matches to analyze"
    )
    
    # Data source selection
    st.markdown("### 📡 Data Source")
    use_live_api = st.checkbox(
        "Use Live GRID API",
        value=False,
        help="Switch from mock data to live GRID API data"
    )
    
    # GRID API key input (if using live API)
    grid_api_key = None
    if use_live_api:
        st.info("📡 **GRID Stats Feed API Mode**")
        st.caption("⚠️ Requires GRID Team ID (team name search not available)")
        
        # Try to get GRID API key from Streamlit secrets first
        default_grid_key = ""
        try:
            default_grid_key = st.secrets.get("GRID_API_KEY", "")
        except:
            import os
            default_grid_key = os.getenv("GRID_API_KEY", "")
        
        grid_api_key = st.text_input(
            "GRID API Key",
            type="password",
            value=default_grid_key,
            help="Enter your GRID API key from https://grid.gg/developers"
        )
        
        st.checkbox("Use Team ID (Required)", value=True, disabled=True, help="Team ID is required for GRID API")
        
        team_id_input = st.text_input(
            "GRID Team ID", 
            value="83", 
            help="Enter GRID team ID (e.g., 83 for LoL teams). Find IDs in GRID documentation."
        )
        if team_id_input:
            team_name = f"TeamID:{team_id_input}"
        
        if grid_api_key:
            import os
            os.environ["GRID_API_KEY"] = grid_api_key
        else:
            st.warning("⚠️ Please enter your GRID API key to use live data")
    else:
        st.success("✅ **Mock Mode Active**")
        st.caption("• Fully functional with realistic data")
        st.caption("• Perfect for demos and presentations")
        st.caption("• No network dependencies")
    
    # LLM provider selection
    st.markdown("### 🤖 AI Scout Settings")
    llm_provider = st.selectbox(
        "LLM Provider",
        ["Mock (No API)", "OpenAI GPT-4", "Google Gemini", "OpenRouter (Gemma 3 27B - Free)"],
        help="Select AI provider for scouting report generation"
    )
    
    # API key input (if needed)
    if llm_provider != "Mock (No API)":
        # Try to get API key from Streamlit secrets first, then environment variables
        default_api_key = ""
        if llm_provider == "OpenRouter (Gemma 3 27B - Free)":
            try:
                default_api_key = st.secrets.get("OPENROUTER_API_KEY", "")
            except:
                import os
                default_api_key = os.getenv("OPENROUTER_API_KEY", "")
        
        if llm_provider == "OpenRouter (Gemma 3 27B - Free)":
            api_key = st.text_input(
                "OpenRouter API Key",
                type="password",
                value=default_api_key,
                help="OpenRouter API key (Gemma 3 27B is free!)"
            )
        else:
            api_key = st.text_input(
                "AI Provider API Key",
                type="password",
                help="Enter your OpenAI or Google API key"
            )
        
        if llm_provider == "OpenAI GPT-4":
            if api_key:
                import os
                os.environ["OPENAI_API_KEY"] = api_key
        elif llm_provider == "Google Gemini":
            if api_key:
                import os
                os.environ["GOOGLE_API_KEY"] = api_key
        elif llm_provider == "OpenRouter (Gemma 3 27B - Free)":
            if api_key:
                import os
                os.environ["OPENROUTER_API_KEY"] = api_key
    
    # Generate button
    generate_button = st.button("🚀 Generate Scouting Report", type="primary")
    
    st.markdown("---")
    st.markdown("**Data Source:** " + ("🔴 GRID API (Live)" if use_live_api else "🟢 Mock Data"))
    st.markdown("**Built for:** Sky Is The Limit Hackathon 2026")

# Main content area
if generate_button:
    try:
        # Clean team name for display
        display_team = team_name if not team_name.startswith("TeamID:") else f"Team {team_name.replace('TeamID:', '')}"
        
        with st.spinner(f"🔍 Analyzing {display_team}'s recent {num_matches} {game_type} matches..."):
            
            # Load data with appropriate mode
            if use_live_api and grid_api_key:
                st.info("🔄 Connecting to GRID Central Data Feed...")
                st.caption("📊 Fetching real tournament/team data + simulated in-game events")
                loader = GridDataLoader(api_key=grid_api_key, use_mock=False)
            else:
                st.info("🎮 Using Mock Data Mode")
                st.caption("📊 Generating realistic demo data")
                loader = GridDataLoader(use_mock=True)
            
            if game_type == "League of Legends":
                # Load LoL data
                matches = loader.load_lol_matches(team_name, num_matches)
                
                if not matches:
                    st.error("❌ No match data found!")
                    st.stop()
                
                # Analyze
                analyzer = LolAnalyzer(matches)
                stats = analyzer.get_complete_analysis()
                
                # Display header stats
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    win_color = utils.get_color_by_performance(stats["win_rate"], 60, 40)
                    st.markdown(utils.format_stat_card(
                        "Win Rate",
                        f"{stats['win_rate']:.1f}%",
                        f"{stats['matches_analyzed']} matches",
                        win_color
                    ), unsafe_allow_html=True)
                
                with col2:
                    jungle_data = stats["jungle_proximity"]
                    max_lane = max(
                        jungle_data["top_lane_percent"],
                        jungle_data["mid_lane_percent"],
                        jungle_data["bot_lane_percent"]
                    )
                    st.markdown(utils.format_stat_card(
                        "Jungle Focus",
                        f"{max_lane:.0f}%",
                        "Most prioritized lane",
                        "#ffa94d"
                    ), unsafe_allow_html=True)
                
                with col3:
                    obj_data = stats["objective_control"]
                    obj_color = utils.get_color_by_performance(obj_data["first_dragon_rate"], 60, 40)
                    st.markdown(utils.format_stat_card(
                        "First Dragon",
                        f"{obj_data['first_dragon_rate']:.0f}%",
                        "Control rate",
                        obj_color
                    ), unsafe_allow_html=True)
                
                with col4:
                    gold_data = stats["gold_efficiency"]
                    gold_15 = gold_data["gold_diff_at_15min"]
                    gold_color = utils.get_color_by_performance(gold_15, 500, -500)
                    st.markdown(utils.format_stat_card(
                        "Gold @ 15min",
                        f"{int(gold_15):+d}",
                        "Average difference",
                        gold_color
                    ), unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Visualizations
                st.header("📊 Statistical Analysis")
                
                # Jungle Heatmap
                st.subheader("🌲 Jungle Proximity Heatmap")
                heatmap_fig = utils.create_jungle_heatmap(stats["jungle_proximity"]["heatmap_data"])
                st.plotly_chart(heatmap_fig)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Top Lane", f"{jungle_data['top_lane_percent']:.1f}%")
                with col2:
                    st.metric("Mid Lane", f"{jungle_data['mid_lane_percent']:.1f}%")
                with col3:
                    st.metric("Bot Lane", f"{jungle_data['bot_lane_percent']:.1f}%")
                
                st.info(f"**Insight:** {jungle_data['insight']}")
                
                # Objective Timeline
                st.subheader("🐉 Objective Control Timeline")
                obj_timeline_fig = utils.create_objective_timeline(matches, team_name)
                st.plotly_chart(obj_timeline_fig)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Dragons", f"{obj_data['team_dragons']}/{obj_data['total_dragons']}")
                with col2:
                    st.metric("Heralds", f"{obj_data['team_heralds']}/{obj_data['total_heralds']}")
                with col3:
                    st.metric("Barons", f"{obj_data['team_barons']}/{obj_data['total_barons']}")
                
                st.info(f"**Insight:** {obj_data['insight']}")
                
                # Gold Difference Chart
                st.subheader("💰 Gold Efficiency Over Time")
                gold_fig = utils.create_gold_diff_chart(matches)
                st.plotly_chart(gold_fig)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("@ 10min", f"{int(gold_data['gold_diff_at_10min']):+d}g")
                with col2:
                    st.metric("@ 15min", f"{int(gold_data['gold_diff_at_15min']):+d}g")
                with col3:
                    st.metric("@ 20min", f"{int(gold_data['gold_diff_at_20min']):+d}g")
                
                st.info(f"**Insight:** {gold_data['insight']}")
                
                # Generate AI Report
                st.markdown("---")
                st.header("🤖 AI-Generated Scouting Report")
                
                with st.spinner("🧠 AI Scout is analyzing patterns and generating win conditions..."):
                    provider_map = {
                        "Mock (No API)": "mock",
                        "OpenAI GPT-4": "openai",
                        "Google Gemini": "gemini",
                        "OpenRouter (Gemma 3 27B - Free)": "openrouter"
                    }
                    report = generate_scouting_report(stats, "lol", provider_map[llm_provider])
                    
                    st.markdown(report)
                
                # Download button for report
                st.download_button(
                    label="📥 Download Scouting Report",
                    data=report,
                    file_name=f"scouting_report_{team_name}_LoL.md",
                    mime="text/markdown"
                )
            
            else:  # VALORANT
                # Load VALORANT data
                matches = loader.load_valorant_matches(team_name, num_matches)
                
                if not matches:
                    st.error("❌ No match data found!")
                    st.stop()
                
                # Analyze
                analyzer = ValorantAnalyzer(matches)
                stats = analyzer.get_complete_analysis()
                
                # Display header stats
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    win_color = utils.get_color_by_performance(stats["match_win_rate"], 60, 40)
                    st.markdown(utils.format_stat_card(
                        "Match Win Rate",
                        f"{stats['match_win_rate']:.1f}%",
                        f"{stats['matches_analyzed']} matches",
                        win_color
                    ), unsafe_allow_html=True)
                
                with col2:
                    round_color = utils.get_color_by_performance(stats["round_win_rate"], 55, 45)
                    st.markdown(utils.format_stat_card(
                        "Round Win Rate",
                        f"{stats['round_win_rate']:.1f}%",
                        f"{stats['total_rounds_played']} rounds",
                        round_color
                    ), unsafe_allow_html=True)
                
                with col3:
                    opening_data = stats["opening_duel_stats"]
                    fb_color = utils.get_color_by_performance(opening_data["first_blood_rate"], 55, 45)
                    st.markdown(utils.format_stat_card(
                        "First Blood Rate",
                        f"{opening_data['first_blood_rate']:.0f}%",
                        "Opening duel success",
                        fb_color
                    ), unsafe_allow_html=True)
                
                with col4:
                    eco_data = stats["economy_stats"]
                    eco_color = utils.get_color_by_performance(eco_data["eco_conversion_rate"], 20, 10)
                    st.markdown(utils.format_stat_card(
                        "Eco Conversion",
                        f"{eco_data['eco_conversion_rate']:.0f}%",
                        "Win rate on save rounds",
                        eco_color
                    ), unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Visualizations
                st.header("📊 Statistical Analysis")
                
                # Opening Duel Stats
                st.subheader("⚔️ Opening Engagement Performance")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        "First Blood Rate",
                        f"{opening_data['first_blood_rate']:.1f}%",
                        delta=f"Conversion: {opening_data['first_blood_conversion']:.1f}%"
                    )
                    st.metric(
                        "Rounds Won WITH First Blood",
                        f"{opening_data['rounds_won_with_fb']} / {opening_data['rounds_with_first_blood']}"
                    )
                
                with col2:
                    st.metric(
                        "Rounds Won WITHOUT First Blood",
                        f"{opening_data['rounds_won_without_fb']}"
                    )
                    st.metric(
                        "Total Rounds Analyzed",
                        f"{opening_data['total_rounds']}"
                    )
                
                st.info(f"**Insight:** {opening_data['insight']}")
                
                # Site Bias Analysis
                st.subheader("🗺️ Site Attack Preferences")
                site_data = stats["site_bias_stats"]
                site_fig = utils.create_site_bias_chart(site_data)
                st.plotly_chart(site_fig)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("A-Site", f"{site_data['site_A_percent']:.1f}%", 
                             delta=f"{site_data['site_A_winrate']:.1f}% WR")
                with col2:
                    st.metric("B-Site", f"{site_data['site_B_percent']:.1f}%",
                             delta=f"{site_data['site_B_winrate']:.1f}% WR")
                with col3:
                    st.metric("C-Site", f"{site_data['site_C_percent']:.1f}%",
                             delta=f"{site_data['site_C_winrate']:.1f}% WR")
                
                st.info(f"**Insight:** {site_data['insight']}")
                
                # Economy Analysis
                st.subheader("💳 Economy Round Performance")
                eco_fig = utils.create_economy_chart(eco_data)
                st.plotly_chart(eco_fig)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Eco Rounds", f"{eco_data['eco_rounds_played']}",
                             delta=f"{eco_data['eco_conversion_rate']:.1f}% WR")
                with col2:
                    st.metric("Force Buy Rounds", f"{eco_data['force_rounds_played']}",
                             delta=f"{eco_data['force_buy_winrate']:.1f}% WR")
                with col3:
                    st.metric("Full Buy Rounds", f"{eco_data['full_buy_rounds_played']}",
                             delta=f"{eco_data['full_buy_winrate']:.1f}% WR")
                
                st.info(f"**Insight:** {eco_data['insight']}")
                
                # Generate AI Report
                st.markdown("---")
                st.header("🤖 AI-Generated Scouting Report")
                
                with st.spinner("🧠 AI Scout is analyzing patterns and generating win conditions..."):
                    provider_map = {
                        "Mock (No API)": "mock",
                        "OpenAI GPT-4": "openai",
                        "Google Gemini": "gemini",
                        "OpenRouter (Gemma 3 27B - Free)": "openrouter"
                    }
                    report = generate_scouting_report(stats, "valorant", provider_map[llm_provider])
                    
                    st.markdown(report)
                
                # Download button for report
                st.download_button(
                    label="📥 Download Scouting Report",
                    data=report,
                    file_name=f"scouting_report_{team_name}_VALORANT.md",
                    mime="text/markdown"
                )
    
    except Exception as e:
        st.error("❌ An error occurred while generating the report")
        st.error(f"**Error details:** {str(e)}")
        
        # Show helpful message based on the error
        if "GRID" in str(e) or "API" in str(e):
            st.warning("""
            **GRID API Connection Issue**
            
            Possible causes:
            - Invalid API key
            - GRID API endpoint is unavailable
            - Network connectivity issues
            
            **Solution:** Uncheck "Use Live GRID API" to use mock data instead.
            """)
        else:
            st.info("💡 **Tip:** Try using mock data mode (uncheck 'Use Live GRID API') to test the system.")
        
        # Show traceback in expander for debugging
        with st.expander("🔧 Technical Details (for debugging)"):
            import traceback
            st.code(traceback.format_exc())

else:
    # Landing page
    st.markdown("""
    ## 👋 Welcome to Vanguard
    
    **Vanguard** is a God-Tier automated esports scouting system that provides "Moneyball-style" 
    statistical analysis for competitive gaming teams.
    
    ### 🎮 Supported Games
    - **League of Legends**: Jungle proximity heatmaps, objective control rates, gold efficiency
    - **VALORANT**: Opening duel statistics, site bias analysis, economy conversion rates
    
    ### 🤖 AI-Powered Insights
    Our LLM-based "Agentic Scout" analyzes your statistical data and generates:
    - **Pattern Recognition**: Identifies exploitable weaknesses
    - **Win Condition Strategy**: Specific, actionable counter-strategies
    - **Timing Windows**: Exact timeframes to execute your game plan
    - **Target Priorities**: Who and what to focus on
    
    ### 🚀 Getting Started
    1. Select your game (LoL or VALORANT) in the sidebar
    2. Enter the team name you want to analyze
    3. Choose how many recent matches to include
    4. Click **"Generate Scouting Report"**
    
    ### 📊 What You'll Get
    - Interactive heatmaps and charts
    - Comprehensive statistical breakdowns
    - AI-generated coaching insights
    - Downloadable markdown reports
    
    ---
    
    **Ready to dominate?** Configure your settings in the sidebar and click the generate button! 🎯
    """)
    
    # Sample visualizations (placeholder)
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**League of Legends Analysis**\n\n- Jungle Proximity Heatmaps\n- Objective Control Timelines\n- Gold Efficiency Charts")
    
    with col2:
        st.info("**VALORANT Analysis**\n\n- Opening Duel Statistics\n- Site Attack Preferences\n- Economy Win Rates")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #8b8d98;'>
    <p><strong>Vanguard</strong> - Moneyball for Esports</p>
    <p>Built for Sky Is The Limit Hackathon 2026 | Powered by GRID Esports API & AI</p>
</div>
""", unsafe_allow_html=True)
