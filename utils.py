"""
Utility functions for visualization and data processing
"""
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List
import pandas as pd
import numpy as np


def create_jungle_heatmap(heatmap_data: Dict[str, List]) -> go.Figure:
    """
    Create an interactive heatmap of jungle proximity
    
    Args:
        heatmap_data: Dictionary with 'x', 'y', and 'lane' lists
        
    Returns:
        Plotly figure object
    """
    x_coords = heatmap_data.get("x", [])
    y_coords = heatmap_data.get("y", [])
    lanes = heatmap_data.get("lane", [])
    
    if not x_coords:
        # Return empty figure
        fig = go.Figure()
        fig.add_annotation(
            text="No jungle position data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=20)
        )
        return fig
    
    # Create density heatmap
    fig = go.Figure(data=go.Histogram2d(
        x=x_coords,
        y=y_coords,
        colorscale='Hot',
        reversescale=True,
        nbinsx=30,
        nbinsy=30
    ))
    
    fig.update_layout(
        title="Jungle Proximity Heatmap (Darker = More Time Spent)",
        xaxis_title="Map X Coordinate",
        yaxis_title="Map Y Coordinate",
        height=600,
        plot_bgcolor='#0f1419',
        paper_bgcolor='#1a1d23',
        font=dict(color='white')
    )
    
    return fig


def create_objective_timeline(matches: List[Dict[str, Any]], team_name: str) -> go.Figure:
    """
    Create timeline visualization of objective captures
    
    Args:
        matches: List of match dictionaries
        team_name: Name of the team being analyzed
        
    Returns:
        Plotly figure object
    """
    all_objectives = []
    
    for match_idx, match in enumerate(matches):
        match_label = f"Match {match_idx + 1}"
        
        # Dragons
        for dragon in match.get("dragons", []):
            all_objectives.append({
                "match": match_label,
                "timestamp": dragon["timestamp"] / 60,  # Convert to minutes
                "type": "Dragon",
                "team": "Captured" if dragon["team"] == team_name else "Lost",
                "specific": dragon.get("dragon_type", "Dragon")
            })
        
        # Heralds
        for herald in match.get("heralds", []):
            all_objectives.append({
                "match": match_label,
                "timestamp": herald["timestamp"] / 60,
                "type": "Herald",
                "team": "Captured" if herald["team"] == team_name else "Lost",
                "specific": "Rift Herald"
            })
        
        # Barons
        for baron in match.get("barons", []):
            all_objectives.append({
                "match": match_label,
                "timestamp": baron["timestamp"] / 60,
                "type": "Baron",
                "team": "Captured" if baron["team"] == team_name else "Lost",
                "specific": "Baron Nashor"
            })
    
    if not all_objectives:
        fig = go.Figure()
        fig.add_annotation(
            text="No objective data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=20)
        )
        return fig
    
    df = pd.DataFrame(all_objectives)
    
    # Create scatter plot with color coding
    fig = px.scatter(
        df,
        x="timestamp",
        y="match",
        color="team",
        symbol="type",
        hover_data=["specific"],
        title="Objective Control Timeline",
        color_discrete_map={"Captured": "#00ff00", "Lost": "#ff0000"}
    )
    
    fig.update_layout(
        xaxis_title="Game Time (minutes)",
        yaxis_title="Match",
        height=400,
        plot_bgcolor='#0f1419',
        paper_bgcolor='#1a1d23',
        font=dict(color='white')
    )
    
    return fig


def create_gold_diff_chart(matches: List[Dict[str, Any]]) -> go.Figure:
    """
    Create line chart showing gold difference over time
    
    Args:
        matches: List of match dictionaries
        
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    for match_idx, match in enumerate(matches):
        gold_updates = match.get("gold_updates", [])
        
        if gold_updates:
            timestamps = [update["timestamp"] / 60 for update in gold_updates]
            gold_diffs = [update["gold_difference"] for update in gold_updates]
            
            match_label = f"Match {match_idx + 1}"
            line_color = '#00ff00' if match.get("won", False) else '#ff0000'
            
            fig.add_trace(go.Scatter(
                x=timestamps,
                y=gold_diffs,
                mode='lines+markers',
                name=match_label,
                line=dict(color=line_color, width=2),
                hovertemplate=f'{match_label}<br>Time: %{{x:.1f}}min<br>Gold Diff: %{{y:+d}}<extra></extra>'
            ))
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    fig.update_layout(
        title="Gold Difference Over Time (Green = Win, Red = Loss)",
        xaxis_title="Game Time (minutes)",
        yaxis_title="Gold Difference",
        height=500,
        plot_bgcolor='#0f1419',
        paper_bgcolor='#1a1d23',
        font=dict(color='white'),
        hovermode='x unified'
    )
    
    return fig


def create_site_bias_chart(site_data: Dict[str, Any]) -> go.Figure:
    """
    Create bar chart showing VALORANT site attack preferences
    
    Args:
        site_data: Site bias statistics dictionary
        
    Returns:
        Plotly figure object
    """
    sites = ["A", "B", "C"]
    percentages = [
        site_data.get("site_A_percent", 0),
        site_data.get("site_B_percent", 0),
        site_data.get("site_C_percent", 0)
    ]
    winrates = [
        site_data.get("site_A_winrate", 0),
        site_data.get("site_B_winrate", 0),
        site_data.get("site_C_winrate", 0)
    ]
    
    fig = go.Figure()
    
    # Add bars for attack frequency
    fig.add_trace(go.Bar(
        x=sites,
        y=percentages,
        name='Attack Frequency (%)',
        marker_color='#ff6b6b',
        text=[f"{p:.1f}%" for p in percentages],
        textposition='auto',
    ))
    
    # Add line for win rate
    fig.add_trace(go.Scatter(
        x=sites,
        y=winrates,
        name='Win Rate (%)',
        mode='lines+markers',
        line=dict(color='#51cf66', width=3),
        marker=dict(size=10),
        text=[f"{w:.1f}%" for w in winrates],
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Site Attack Preference vs Success Rate",
        xaxis_title="Site",
        yaxis_title="Attack Frequency (%)",
        yaxis2=dict(
            title="Win Rate (%)",
            overlaying='y',
            side='right'
        ),
        height=400,
        plot_bgcolor='#0f1419',
        paper_bgcolor='#1a1d23',
        font=dict(color='white'),
        legend=dict(x=0.01, y=0.99)
    )
    
    return fig


def create_economy_chart(eco_data: Dict[str, Any]) -> go.Figure:
    """
    Create visualization of economy round performance
    
    Args:
        eco_data: Economy statistics dictionary
        
    Returns:
        Plotly figure object
    """
    categories = ['Eco\n(<2000)', 'Force Buy\n(2000-3500)', 'Full Buy\n(3500+)']
    win_rates = [
        eco_data.get("eco_conversion_rate", 0),
        eco_data.get("force_buy_winrate", 0),
        eco_data.get("full_buy_winrate", 0)
    ]
    rounds_played = [
        eco_data.get("eco_rounds_played", 0),
        eco_data.get("force_rounds_played", 0),
        eco_data.get("full_buy_rounds_played", 0)
    ]
    
    # Color code: Red for eco, Orange for force, Green for full
    colors = ['#ff6b6b', '#ffa94d', '#51cf66']
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=categories,
        y=win_rates,
        text=[f"{wr:.1f}%<br>({rp} rounds)" for wr, rp in zip(win_rates, rounds_played)],
        textposition='auto',
        marker_color=colors,
        name='Win Rate'
    ))
    
    fig.update_layout(
        title="Win Rate by Economy Type",
        xaxis_title="Buy Type",
        yaxis_title="Win Rate (%)",
        height=400,
        plot_bgcolor='#0f1419',
        paper_bgcolor='#1a1d23',
        font=dict(color='white')
    )
    
    return fig


def format_stat_card(title: str, value: str, subtitle: str = "", color: str = "#ffffff") -> str:
    """
    Generate HTML for a styled stat card
    
    Args:
        title: Card title
        value: Main value to display
        subtitle: Optional subtitle
        color: Color for the value text
        
    Returns:
        HTML string
    """
    return f"""
    <div style="
        background: linear-gradient(135deg, #1a1d23 0%, #2d3139 100%);
        border-left: 4px solid {color};
        padding: 20px;
        border-radius: 8px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    ">
        <h3 style="margin:0; color:#8b8d98; font-size:14px; font-weight:400;">{title}</h3>
        <p style="margin:10px 0 5px 0; color:{color}; font-size:36px; font-weight:700;">{value}</p>
        {f'<p style="margin:0; color:#8b8d98; font-size:12px;">{subtitle}</p>' if subtitle else ''}
    </div>
    """


def get_color_by_performance(value: float, threshold_good: float, threshold_bad: float, 
                              higher_is_better: bool = True) -> str:
    """
    Get color based on performance metric
    
    Args:
        value: The metric value
        threshold_good: Threshold for good performance
        threshold_bad: Threshold for bad performance
        higher_is_better: Whether higher values are better
        
    Returns:
        Hex color code
    """
    if higher_is_better:
        if value >= threshold_good:
            return "#51cf66"  # Green
        elif value <= threshold_bad:
            return "#ff6b6b"  # Red
        else:
            return "#ffa94d"  # Orange
    else:
        if value <= threshold_good:
            return "#51cf66"
        elif value >= threshold_bad:
            return "#ff6b6b"
        else:
            return "#ffa94d"
