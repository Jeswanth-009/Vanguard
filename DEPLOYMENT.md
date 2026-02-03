# Deployment Guide

## 🚀 Deploy to Streamlit Cloud

### Step 1: Remove Exposed API Keys from GitHub

**IMPORTANT:** Your API keys were pushed to GitHub! Follow these steps:

1. **Rotate your API keys immediately:**
   - GRID API: Get new key at https://developer.grid.gg/
   - OpenRouter: Get new key at https://openrouter.ai/keys

2. **Remove from Git history:**
```bash
# Install BFG Repo Cleaner or use git filter-branch
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch main.py" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (WARNING: This rewrites history)
git push origin --force --all
```

**OR** simply delete the repo and recreate it (easier option).

### Step 2: Deploy to Streamlit Cloud

1. **Go to:** https://share.streamlit.io/

2. **Click:** "New app"

3. **Connect your GitHub repo:**
   - Repository: `Jeswanth-009/Vanguard`
   - Branch: `main`
   - Main file: `main.py`

4. **Add Secrets:**
   - Click "Advanced settings"
   - Go to "Secrets" section
   - Copy and paste this format:

```toml
# GRID Esports API
GRID_API_KEY = "p6A54Yf7qoOOCpBkI2rbwxgcq5PmqyMmErumj4AN"

# OpenRouter API (Free Gemma 3 27B)
OPENROUTER_API_KEY = "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"

# Optional: Add other LLM providers
# OPENAI_API_KEY = "your-openai-key"
# GOOGLE_API_KEY = "your-google-key"
```

5. **Click:** "Deploy!"

### Step 3: Verify Deployment

Your app will be live at: `https://[your-app-name].streamlit.app`

The API keys will be securely stored and NOT visible in the UI or code.

## 🔒 Security Best Practices

### Local Development

1. **Create `.streamlit/secrets.toml`** (local only):
```bash
mkdir .streamlit
# Copy secrets.toml.example to secrets.toml
# Add your real API keys to secrets.toml
```

2. **Verify `.gitignore` includes:**
```
.streamlit/secrets.toml
.env
```

3. **Use environment variables OR secrets:**
```python
# The code now checks:
# 1. Streamlit secrets (for deployed apps)
# 2. Environment variables (for local dev)
# 3. Manual input (fallback)
```

### GitHub Repository

- ✅ **DO commit:** `secrets.toml.example`, `.env.example`
- ❌ **DON'T commit:** `secrets.toml`, `.env`, actual API keys

## 🧪 Testing Deployment

### Test Locally First:
```bash
# Create secrets file
mkdir .streamlit
echo 'GRID_API_KEY = "your-key"' > .streamlit/secrets.toml

# Run app
streamlit run main.py
```

### Test on Streamlit Cloud:
1. Deploy app
2. Check "Manage app" → "Logs" for errors
3. Test with Team ID 83 (known working team)

## 🐛 Troubleshooting

### "API key not found" error:
- Check Streamlit Cloud secrets are properly formatted (no quotes around keys)
- Verify secrets section doesn't have extra spaces

### GRID API 400 errors:
- Ensure Team ID is numeric only
- Check Title ID: LoL=22, VALORANT=29

### App crashes on startup:
- Check requirements.txt includes all dependencies
- View logs in Streamlit Cloud dashboard

## ✅ Final Checklist

- [ ] Rotated exposed API keys
- [ ] Removed keys from git history OR deleted/recreated repo
- [ ] Added secrets to Streamlit Cloud
- [ ] Verified `.gitignore` includes secrets files
- [ ] Tested deployment with mock mode
- [ ] Tested deployment with GRID API mode
- [ ] Tested all LLM providers

## 🎯 Your Deployment URL

After deployment: `https://vanguard-esports-scout.streamlit.app`

(Customize the URL in Streamlit Cloud settings)
