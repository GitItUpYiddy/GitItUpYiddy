# Quick Start Guide - AI Trading Agents

## 🚀 5-Minute Setup

### 1. Clone & Setup

```bash
# Clone the repository
git clone https://github.com/GitItUpYiddy/GitItUpYiddy.git
cd GitItUpYiddy

# Checkout the branch
git checkout claude/clone-moon-dev-repo-011CUKTa7DHN59AQ48ZnjtJ6

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
# Copy environment template
cp .env_example .env

# Edit with your keys
nano .env
```

**Minimum required (choose one AI provider):**
- `ANTHROPIC_KEY` - For Claude models
- `OPENAI_KEY` - For GPT models
- `GROQ_API_KEY` - For Groq (fast & free tier)

### 3. Run Your First Agent

```bash
# Test with a simple agent
python src/agents/sentiment_agent.py
```

---

## 📋 Common Commands

### Main Orchestrator
```bash
# Run all active agents in a loop
python src/main.py
```

### Individual Agents

**Trading:**
```bash
python src/agents/trading_agent.py      # Trade analysis
python src/agents/risk_agent.py         # Risk monitoring
python src/agents/strategy_agent.py     # Run strategies
```

**Analysis:**
```bash
python src/agents/sentiment_agent.py    # Twitter sentiment
python src/agents/whale_agent.py        # Whale tracking
python src/agents/chartanalysis_agent.py # Chart analysis
```

**Strategy Development:**
```bash
python src/agents/rbi_agent.py          # Create backtests from videos
python src/agents/research_agent.py     # Generate ideas
```

**Content Creation:**
```bash
python src/agents/tweet_agent.py        # Generate tweets
python src/agents/chat_agent.py         # YouTube chat monitor
python src/agents/video_agent.py        # Create videos
```

---

## 🎯 Your First 30 Minutes

### Minute 0-5: Setup
```bash
git clone [repo]
cd GitItUpYiddy
pip install -r requirements.txt
cp .env_example .env
```

### Minute 5-10: Configure
- Add at least one AI API key to `.env`
- Optional: Add trading API keys (for live data)

### Minute 10-15: Test Basic Agent
```bash
# Run a simple, safe agent
python src/agents/research_agent.py
```

### Minute 15-20: Create a Backtest
```bash
# Run RBI agent with a YouTube video
python src/agents/rbi_agent.py
# Enter a trading strategy video URL when prompted
```

### Minute 20-25: Explore Agents
```bash
# List all available agents
ls src/agents/*.py

# Check agent documentation
cat src/agents/README.md
```

### Minute 25-30: Customize
```bash
# Edit configuration
nano src/config.py

# Create your own strategy
nano src/strategies/my_first_strategy.py
```

---

## ⚡ Quick Reference Card

| What You Want | Command |
|---------------|---------|
| Run everything | `python src/main.py` |
| Check risk | `python src/agents/risk_agent.py` |
| Analyze sentiment | `python src/agents/sentiment_agent.py` |
| Create backtest | `python src/agents/rbi_agent.py` |
| Generate tweet | `python src/agents/tweet_agent.py` |
| Monitor whales | `python src/agents/whale_agent.py` |
| Check funding | `python src/agents/funding_agent.py` |
| View outputs | `ls src/data/` |

---

## 🔑 Essential Files

| File | Purpose |
|------|---------|
| `.env` | Your API keys (create from `.env_example`) |
| `src/config.py` | Trading settings & risk limits |
| `src/main.py` | Main orchestrator |
| `src/agents/` | All 45+ AI agents |
| `src/models/` | LLM provider integrations |
| `src/strategies/` | Your trading strategies |
| `src/data/` | Agent outputs & results |

---

## 🎓 Learning Path

1. **Beginner:**
   - Run `sentiment_agent.py`
   - Run `research_agent.py`
   - Understand agent outputs

2. **Intermediate:**
   - Run `rbi_agent.py` to create backtests
   - Modify `config.py` settings
   - Create a custom strategy

3. **Advanced:**
   - Run `main.py` orchestrator
   - Integrate live trading APIs
   - Deploy multiple agents

---

## ⚠️ Safety First

✅ **Do This:**
- Start with research/analysis agents
- Test with paper trading
- Review all code before running
- Keep API keys secure

❌ **Don't Do This:**
- Never commit `.env` file
- Don't trade real money immediately
- Don't share API keys
- Don't trust blindly - review strategies

---

## 🆘 Quick Troubleshooting

**"Module not found"**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**"API key not found"**
```bash
# Check .env exists and has keys
cat .env | grep KEY
```

**"No trades executing"**
- This is normal! Review `config.py` first
- System is designed for safety
- Test in paper trading mode

---

## 📚 Full Documentation

For detailed information, see:
- `SETUP_GUIDE.md` - Complete setup & usage guide
- `README.md` - Project overview
- `CLAUDE.md` - Development guidelines

---

## 🔗 Resources

- **Discord:** [moondev.com](http://moondev.com)
- **YouTube:** [Moon Dev Channel](https://www.youtube.com/@moondevonyt)
- **Original Repo:** [moon-dev-ai-agents](https://github.com/moondevonyt/moon-dev-ai-agents)

---

**Ready to build the future of AI-powered trading? Let's go! 🚀**
