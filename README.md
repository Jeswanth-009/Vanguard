# ⚔️ Vanguard - AI-Powered Esports Scouting Report Generator

> **God-Tier Automated Esports Intelligence Platform**  
> Built for Sky is the limit Hackathon | Powered by GRID Esports API + AI

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![GRID API](https://img.shields.io/badge/GRID-API%20Integrated-orange.svg)

## 🎯 Overview

Vanguard is an automated esports scouting platform that generates comprehensive, AI-powered scouting reports for **League of Legends** and **VALORANT** teams. It combines real-time statistics from GRID Esports API with advanced AI analysis to provide actionable coaching insights.

### ✨ Key Features

- **🔴 Live GRID API Integration**: Real statistics from professional esports matches
- **🤖 Multi-LLM Support**: OpenAI GPT-4, Google Gemini, OpenRouter (free Gemma 3 27B)
- **📊 Advanced Analytics**: Win rates, K/D ratios, objective control, performance trends
- **🎮 Dual Game Support**: League of Legends & VALORANT
- **📈 Interactive Visualizations**: Performance charts, match timelines, heatmaps
- **💡 AI Coaching Insights**: Win conditions, exploit strategies, tactical recommendations
- **🎭 Hybrid Architecture**: Real GRID stats + simulated match details for reliability

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- GRID Esports API Key ([Get one here](https://developer.grid.gg/))
- LLM API Key (OpenAI, Google, or OpenRouter)

### Installation

```bash
# Clone the repository
git clone https://github.com/Jeswanth-009/Vanguard.git
cd Vanguard

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (optional)
cp .env.example .env
# Edit .env with your API keys
```

### Running the Application

```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

## 🎮 Usage

### Mock Mode (Demo)
1. Uncheck "Use Live GRID API"
2. Select game: League of Legends or VALORANT
3. Enter team name (e.g., "Cloud9")
4. Choose LLM provider and enter API key
5. Click "Generate Scouting Report"

### Live GRID API Mode
1. Check "Use Live GRID API"
2. Enter your GRID API Key
3. Enter Team ID (e.g., `83`)
4. Select game (Title ID: LoL=22, VALORANT=29)
5. Choose LLM provider
6. Generate report with real statistics!

### LLM Providers

| Provider | Model | Cost | Context |
|----------|-------|------|---------|
| **OpenAI** | GPT-4 | Paid | 128K tokens |
| **Google** | Gemini Pro | Free tier | 32K tokens |
| **OpenRouter** | Gemma 3 27B | FREE ✨ | 131K tokens |

**Recommended**: OpenRouter (Gemma 3 27B) - completely free, high quality!

## 📦 Project Structure

```
Vanguard/
├── main.py              # Streamlit dashboard UI
├── loaders.py           # GRID API integration & data loading
├── analyzers.py         # Statistical analysis engine
├── agent.py             # LLM-powered report generation
├── mock_data.py         # Mock data generators
├── utils.py             # Visualization utilities
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔧 Core Components

### 1. Data Loading (`loaders.py`)
- **GRID Stats Feed API**: Fetches real aggregated statistics
- **Team Statistics**: Win rates, K/D, objectives, series history
- **Hybrid Approach**: Real stats + simulated match details
- **Error Handling**: Automatic fallback to mock data

### 2. Analysis Engine (`analyzers.py`)
- **Performance Metrics**: Win rate trends, consistency scores
- **Game-Specific Stats**: 
  - LoL: Gold per minute, CS, vision score, dragon/baron control
  - VALORANT: ACS, first bloods, clutch rate, site control
- **Strengths/Weaknesses**: Automated pattern recognition

### 3. AI Agent (`agent.py`)
- **Multi-Provider**: OpenAI, Google, OpenRouter support
- **Coaching Insights**: Win conditions, exploit strategies
- **Contextual Analysis**: Game state, meta adaptation

### 4. Mock Data (`mock_data.py`)
- **Game-Accurate**: Realistic champion pools, agent comps
- **Match Details**: Round-by-round data, heatmaps, timelines
- **Demo Reliability**: Consistent test data for presentations

## 🌐 GRID API Integration

### Architecture
Vanguard uses **GRID Stats Feed API** for real statistics:

- **Endpoint**: `https://api-op.grid.gg/statistics-feed/graphql`
- **Data**: Aggregated win rates, kills, deaths, series history
- **Title IDs**: 
  - League of Legends: `22`
  - VALORANT: `29`

### Example Query
```graphql
query TeamStatistics($teamId: Int!, $titleId: Int!) {
  aggregations(
    filter: {
      dimensionFilters: [
        { dimension: "team_id", value: [$teamId] }
        { dimension: "title_id", value: [$titleId] }
      ]
    }
  ) {
    data {
      totalSeries: sum(dimension: "series_count")
      totalGames: sum(dimension: "games_count")
      wins: valueCountByDimension(
        dimension: "won"
        sumBy: "games_count"
      ) {
        value
        percentage
      }
    }
  }
}
```

## 🎨 Features Showcase

### 📊 Comprehensive Analytics
- **Performance Trends**: 10-match rolling average
- **Consistency Score**: Statistical variance analysis
- **Match Visualizations**: Interactive charts and heatmaps

### 🤖 AI-Powered Insights
- **Win Conditions**: How the team wins (early aggression, scaling, teamfights)
- **Exploit Strategies**: Opponent weaknesses and how to abuse them
- **Coaching Recommendations**: Actionable tactical advice

### 🎯 Game-Specific Analysis

**League of Legends**:
- Gold economy trends
- Objective control (dragons, barons, towers)
- Vision dominance
- Champion pool analysis

**VALORANT**:
- Round win patterns
- Site control statistics  
- Economy management
- Agent composition meta

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.8+ |
| **Data Processing** | Pandas, NumPy |
| **Frontend** | Streamlit |
| **Visualizations** | Plotly |
| **AI Agent** | OpenAI GPT-4, Google Gemini, OpenRouter |
| **API** | GRID Esports Stats Feed API |



## 🐛 Troubleshooting

### Common Issues

**White Screen / App Crashes**
- Check terminal for error messages
- Verify API keys are valid
- Try mock mode first to isolate API issues

**GRID API 400 Errors**
- Verify team ID is correct (numeric only)
- Check title ID matches game (LoL=22, VALORANT=29)
- Ensure API key has correct permissions

**No AI Report Generated**
- Verify LLM API key is valid
- Check API provider status
- Try different provider (OpenRouter is most reliable)

**Import Errors**
- Run `pip install -r requirements.txt`
- Verify Python version 3.8+

## 📝 Dependencies

```
streamlit>=1.28.0
requests>=2.31.0
plotly>=5.17.0
pandas>=2.1.0
numpy>=1.24.0
openai>=1.3.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
```

## 🎓 How It Works

1. **Data Collection**: Fetch statistics from GRID API or generate mock data
2. **Analysis**: Calculate performance metrics, trends, strengths/weaknesses
3. **Visualization**: Create interactive charts and heatmaps
4. **AI Generation**: Send context to LLM for strategic insights
5. **Report Assembly**: Combine all components into comprehensive report

## 🏆 Built For

**Cloud9 Hackathon** - Esports Intelligence Track

This project demonstrates:
- Real-time esports data integration
- AI-powered analysis and insights
- Production-ready hybrid architecture
- Multi-game support
- Professional UI/UX

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- **GRID Esports** - For comprehensive esports data API
- **OpenRouter** - For free access to Gemma 3 27B
- **Streamlit** - For rapid dashboard development
- **Cloud9** - For hosting the hackathon

## 📧 Contact

**Developer**: Jeswanth  
**GitHub**: [@Jeswanth-009](https://github.com/Jeswanth-009)  
**Repository**: [Vanguard](https://github.com/Jeswanth-009/Vanguard)

---

⚔️ **Built with passion for esports analytics** | Powered by GRID + AI | Cloud9 Hackathon 2026

**Current (Mock Mode):**
```python
loader = GridDataLoader(use_mock=True)
```

**Production (Live API):**
```python
loader = GridDataLoader(api_key="your-grid-api-key", use_mock=False)
```

### Implement the `_fetch_from_grid_api()` method:
```python
def _fetch_from_grid_api(self, game_type: str, team_name: str, num_matches: int):
    import requests
    
    headers = {"Authorization": f"Bearer {self.api_key}"}
    
    if game_type == "lol":
        url = f"https://api-v2.grid.gg/central-data/v1/lol/matches?team={team_name}&limit={num_matches}"
    else:
        url = f"https://api-v2.grid.gg/central-data/v1/valorant/matches?team={team_name}&limit={num_matches}"
    
    response = requests.get(url, headers=headers)
    return response.json()
```

---

## 🧪 Testing the Mock Data

You can test the mock data generators directly:

```bash
python mock_data.py
```

This will generate sample matches and print statistics to verify the data structure.

---

## 📈 Example Use Cases

### For Coaches:
- **Pre-Match Preparation**: Analyze opponent's recent games before a match
- **Weakness Identification**: Find specific areas to exploit (e.g., "They ignore top lane")
- **Strategy Development**: Use AI-generated win conditions to craft game plans

### For Analysts:
- **Pattern Recognition**: Identify long-term trends in team playstyles
- **Performance Tracking**: Monitor improvements over time
- **Comparative Analysis**: Compare multiple teams side-by-side

### For Players:
- **Self-Scouting**: Analyze your own team's weaknesses
- **Counter-Strategy Development**: Understand how opponents might exploit you
- **Meta Adaptation**: See how strategies evolve across matches

---

## 🎨 Customization

### Adding New Metrics
1. Extend the analyzer classes in `analyzers.py`
2. Add visualization functions in `utils.py`
3. Update the Streamlit dashboard in `main.py`

### Adding New Games
1. Create a new analyzer class (e.g., `CsgoAnalyzer`)
2. Add mock data generator in `mock_data.py`
3. Update the loader and main dashboard

---

## 🐛 Troubleshooting

### Issue: "Module not found"
**Solution:** Ensure all dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: "API key not working"
**Solution:** Verify your environment variables
```python
import os
print(os.getenv("OPENAI_API_KEY"))  # Should print your key
```

### Issue: Visualizations not showing
**Solution:** Check browser console, try refreshing, or use a different browser

---

## 🚀 Next Steps for Production

1. **GRID API Integration**: Replace mock data with live API calls
2. **Database Storage**: Cache match data in PostgreSQL or MongoDB
3. **User Authentication**: Add login system for teams
4. **Historical Tracking**: Store analysis results over time
5. **Comparative Reports**: Analyze multiple teams simultaneously
6. **Real-time Updates**: WebSocket integration for live match data
7. **Export Options**: PDF reports, PowerPoint presentations

---

## 📝 License

This project is built for the Cloud9 Hackathon 2026.

---

## 🙏 Acknowledgments

- **GRID Esports API** - For providing comprehensive esports data
- **Cloud9** - For hosting the hackathon
- **OpenAI / Google** - For LLM capabilities
- **Streamlit Community** - For the incredible framework

---

## 📧 Contact

Built by a passionate esports data engineer for the Cloud9 Hackathon.

**"Moneyball changed baseball. Vanguard will change esports."** 🎯

---

## 🎯 Hackathon Submission Checklist

- ✅ Complete file structure
- ✅ Mock data for immediate testing
- ✅ League of Legends analysis engine
- ✅ VALORANT analysis engine
- ✅ LLM-powered scouting agent
- ✅ Interactive Streamlit dashboard
- ✅ Plotly visualizations
- ✅ Comprehensive documentation
- ✅ Production-ready architecture
- ✅ Easy GRID API integration path

**Status: Ready for Demo! 🚀**
