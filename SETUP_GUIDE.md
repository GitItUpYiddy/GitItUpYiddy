# AI Agents for Trading - Complete Setup & Usage Guide

## Table of Contents
1. [Download & Installation](#download--installation)
2. [Environment Setup](#environment-setup)
3. [Configuration](#configuration)
4. [How to Use](#how-to-use)
5. [Agent Overview](#agent-overview)
6. [Examples & Walkthroughs](#examples--walkthroughs)
7. [Troubleshooting](#troubleshooting)

---

## Download & Installation

### Option 1: Clone from GitHub (Recommended)

```bash
# Clone the repository
git clone https://github.com/GitItUpYiddy/GitItUpYiddy.git

# Navigate into the directory
cd GitItUpYiddy

# Checkout the branch with all the agents
git checkout claude/clone-moon-dev-repo-011CUKTa7DHN59AQ48ZnjtJ6
```

### Option 2: Download ZIP

1. Go to your GitHub repository
2. Click the green "Code" button
3. Select "Download ZIP"
4. Extract the ZIP file to your desired location

---

## Environment Setup

### Prerequisites

- **Python 3.10.9** (recommended) or Python 3.8+
- **pip** (Python package manager)
- **Git** (for version control)

### Step 1: Create Virtual Environment (Optional but Recommended)

```bash
# Using conda (recommended by the original developer)
conda create -n tflow python=3.10.9
conda activate tflow

# OR using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**Note:** If you encounter any errors, install packages individually:
```bash
pip install anthropic openai pandas requests termcolor python-dotenv
```

---

## Configuration

### Step 1: Set Up Environment Variables

```bash
# Copy the example environment file
cp .env_example .env

# Edit the .env file with your API keys
nano .env  # or use any text editor
```

### Step 2: Required API Keys

Add these to your `.env` file:

```bash
# AI Model APIs (at least one required)
ANTHROPIC_KEY=your_anthropic_api_key_here
OPENAI_KEY=your_openai_api_key_here
DEEPSEEK_KEY=your_deepseek_api_key_here
GROQ_API_KEY=your_groq_api_key_here
GEMINI_KEY=your_gemini_api_key_here

# Trading APIs (for live trading features)
BIRDEYE_API_KEY=your_birdeye_api_key_here
MOONDEV_API_KEY=your_moondev_api_key_here
COINGECKO_API_KEY=your_coingecko_api_key_here

# Blockchain (for Solana trading)
SOLANA_PRIVATE_KEY=your_solana_private_key_here
RPC_ENDPOINT=your_rpc_endpoint_here

# Optional
HYPER_LIQUID_ETH_PRIVATE_KEY=your_hyperliquid_key_here
```

### Step 3: Configure Trading Settings

Edit `src/config.py` to customize:

```python
# Trading settings
MONITORED_TOKENS = ['SOL', 'BTC', 'ETH']  # Tokens to watch
EXCLUDED_TOKENS = ['SCAM', 'RUG']         # Tokens to avoid

# Risk management
MAX_LOSS_USD = 1000        # Maximum allowed loss
MAX_GAIN_USD = 5000        # Take profit threshold
MINIMUM_BALANCE_USD = 500  # Circuit breaker minimum

# AI settings
AI_MODEL = "claude-3-haiku-20240307"  # Fast & cheap
AI_MAX_TOKENS = 1000
AI_TEMPERATURE = 0.7

# Agent timing
SLEEP_BETWEEN_RUNS_MINUTES = 15  # How often agents run
```

---

## How to Use

### Quick Start - Run the Main Orchestrator

The **main orchestrator** runs multiple agents in a coordinated loop:

```bash
# Run the main system (coordinates all active agents)
python src/main.py
```

This will:
1. Run the Risk Agent first (checks portfolio health)
2. Execute active trading agents
3. Run analysis agents
4. Sleep for configured interval (default 15 minutes)
5. Repeat indefinitely

**Press Ctrl+C to stop gracefully**

### Run Individual Agents

Each agent can run independently:

```bash
# Trading agents
python src/agents/trading_agent.py      # Basic trading decisions
python src/agents/strategy_agent.py     # Strategy execution
python src/agents/risk_agent.py         # Risk monitoring

# Analysis agents
python src/agents/sentiment_agent.py    # Twitter sentiment analysis
python src/agents/whale_agent.py        # Whale wallet tracking
python src/agents/funding_agent.py      # Funding rate monitoring

# Strategy development
python src/agents/rbi_agent.py          # Create backtests from YouTube videos
python src/agents/research_agent.py     # Generate trading ideas

# Content creation
python src/agents/chat_agent.py         # Monitor YouTube chat
python src/agents/tweet_agent.py        # Generate tweets
python src/agents/video_agent.py        # Create videos
python src/agents/clips_agent.py        # Create video clips
```

---

## Agent Overview

### 🎯 Trading Agents (Core)

| Agent | Purpose | Command |
|-------|---------|---------|
| **Trading Agent** | Analyzes tokens and makes basic trade decisions | `python src/agents/trading_agent.py` |
| **Strategy Agent** | Executes strategies from `src/strategies/` | `python src/agents/strategy_agent.py` |
| **Risk Agent** | Monitors portfolio risk and PnL thresholds | `python src/agents/risk_agent.py` |
| **Copybot Agent** | Monitors copy trading signals | `python src/agents/copybot_agent.py` |

### 📊 Market Analysis Agents

| Agent | Purpose | Command |
|-------|---------|---------|
| **Sentiment Agent** | Analyzes crypto Twitter sentiment | `python src/agents/sentiment_agent.py` |
| **Whale Agent** | Tracks whale wallet activity | `python src/agents/whale_agent.py` |
| **Funding Agent** | Monitors perpetual funding rates | `python src/agents/funding_agent.py` |
| **Liquidation Agent** | Tracks liquidation events | `python src/agents/liquidation_agent.py` |
| **Chart Agent** | AI-powered chart analysis | `python src/agents/chartanalysis_agent.py` |

### 🧪 Strategy Development Agents

| Agent | Purpose | Command |
|-------|---------|---------|
| **RBI Agent** | Creates backtests from YouTube/PDFs | `python src/agents/rbi_agent.py` |
| **Research Agent** | Generates trading strategy ideas | `python src/agents/research_agent.py` |
| **Backtest Runner** | Runs and analyzes backtests | `python src/agents/backtest_runner.py` |

### 🎬 Content Creation Agents

| Agent | Purpose | Command |
|-------|---------|---------|
| **Chat Agent** | Monitors/responds to YouTube chat | `python src/agents/chat_agent.py` |
| **Tweet Agent** | Generates tweets using AI | `python src/agents/tweet_agent.py` |
| **Video Agent** | Creates videos from scripts | `python src/agents/video_agent.py` |
| **Clips Agent** | Creates short clips from long videos | `python src/agents/clips_agent.py` |
| **Phone Agent** | AI phone call handler | `python src/agents/phone_agent.py` |

### 🔍 Specialized Agents

| Agent | Purpose | Command |
|-------|---------|---------|
| **Sniper Agent** | Watches for new token launches | `python src/agents/sniper_agent.py` |
| **Solana Agent** | Analyzes Solana meme coins | `python src/agents/solana_agent.py` |
| **TX Agent** | Monitors wallet transactions | `python src/agents/tx_agent.py` |
| **TikTok Agent** | Scrapes TikTok for consumer data | `python src/agents/tiktok_agent.py` |
| **Compliance Agent** | Checks ad compliance | `python src/agents/compliance_agent.py` |

**Total: 45+ specialized AI agents**

---

## Examples & Walkthroughs

### Example 1: Create a Backtest from a YouTube Video

The **RBI Agent** can watch a YouTube video about trading and create a working backtest:

```bash
# Run the RBI agent
python src/agents/rbi_agent.py
```

When prompted:
1. Enter a YouTube URL (e.g., trading strategy video)
2. The agent will:
   - Download and transcribe the video
   - Extract the trading strategy
   - Generate backtesting code
   - Run the backtest
   - Return performance metrics

**Cost:** ~$0.027 per backtest (~6 minutes)

### Example 2: Run a Basic Trading Loop

```bash
# 1. Check your risk status
python src/agents/risk_agent.py

# 2. Run trading agent to analyze tokens
python src/agents/trading_agent.py

# 3. Check sentiment before trading
python src/agents/sentiment_agent.py
```

### Example 3: Create Your Own Strategy

1. Create a new strategy file:

```bash
# Create new strategy
nano src/strategies/my_strategy.py
```

2. Add strategy code:

```python
from src.strategies.base import BaseStrategy

class MyStrategy(BaseStrategy):
    name = "my_custom_strategy"
    description = "My custom trading logic"

    def generate_signals(self, token_address, market_data):
        # Your logic here
        action = "BUY"  # or "SELL" or "NOTHING"
        confidence = 75  # 0-100
        reasoning = "Strong bullish momentum"

        return {
            "action": action,
            "confidence": confidence,
            "reasoning": reasoning
        }
```

3. Run the strategy agent:

```bash
python src/agents/strategy_agent.py
```

### Example 4: Switch AI Models

Edit `src/config.py`:

```python
# Use fast, cheap model
AI_MODEL = "claude-3-haiku-20240307"

# Use more powerful model
# AI_MODEL = "claude-3-sonnet-20240229"

# Use most powerful model
# AI_MODEL = "claude-3-opus-20240229"
```

Or use different providers in individual agents:

```python
from src.models.model_factory import ModelFactory

# Use DeepSeek for reasoning tasks
model = ModelFactory.create_model('deepseek')

# Use Groq for fast inference
model = ModelFactory.create_model('groq')

# Use Claude (default)
model = ModelFactory.create_model('anthropic')
```

### Example 5: Monitor Live Trading

```bash
# Terminal 1: Run main orchestrator
python src/main.py

# Terminal 2: Monitor risk in real-time
watch -n 30 python src/agents/risk_agent.py

# Terminal 3: Watch for whale activity
python src/agents/whale_agent.py
```

---

## Troubleshooting

### Common Issues

#### Issue: "Module not found" errors

**Solution:**
```bash
# Make sure you're in the correct directory
cd /path/to/GitItUpYiddy

# Reinstall dependencies
pip install -r requirements.txt
```

#### Issue: "API key not found"

**Solution:**
```bash
# Check your .env file exists
ls -la .env

# Verify API keys are set
cat .env | grep ANTHROPIC_KEY

# Make sure .env is in the project root
```

#### Issue: "No module named 'src'"

**Solution:**
```bash
# Run from the project root directory
cd /path/to/GitItUpYiddy

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### Issue: Trading agents aren't executing trades

**Solution:**
- This is **expected behavior** - the system is designed for safety
- Review `src/config.py` trading settings
- Check `MONITORED_TOKENS` list
- Verify API keys for trading platforms
- Test in paper trading mode first

#### Issue: Out of API credits

**Solution:**
```bash
# Switch to a cheaper model in src/config.py
AI_MODEL = "claude-3-haiku-20240307"  # Most cost-effective

# Or use free alternatives
# Use Groq (free tier available)
# Use Ollama (local, completely free)
```

### Getting Help

1. **Check Documentation:**
   - `README.md` - Project overview
   - `CLAUDE.md` - Development guidelines
   - `src/agents/README.md` - Agent documentation
   - `src/models/README.md` - Model factory docs

2. **Join the Community:**
   - Discord: [moondev.com](http://moondev.com)
   - YouTube: [Moon Dev Channel](https://www.youtube.com/@moondevonyt)

3. **Original Repository:**
   - [github.com/moondevonyt/moon-dev-ai-agents](https://github.com/moondevonyt/moon-dev-ai-agents)

---

## Safety Reminders

⚠️ **CRITICAL DISCLAIMERS:**

1. This is an **experimental research project**, NOT a trading system
2. **NO guarantees of profitability** - trading involves substantial risk of loss
3. **Test thoroughly** before any live trading
4. Start with **small amounts** or paper trading
5. **Never commit** your `.env` file with API keys
6. There is **NO token** associated with this project (avoid scams)

---

## Advanced Usage

### Running Specific Agent Combinations

```bash
# Risk + Trading + Sentiment combo
python src/agents/risk_agent.py && \
python src/agents/sentiment_agent.py && \
python src/agents/trading_agent.py
```

### Customizing the Main Loop

Edit `src/main.py` to activate/deactivate agents:

```python
ACTIVE_AGENTS = {
    'risk': True,           # Always keep this on
    'trading': True,        # Main trading logic
    'sentiment': True,      # Twitter sentiment
    'whale': False,         # Disable whale tracking
    'funding': True,        # Funding rate monitoring
    # ... customize as needed
}
```

### Viewing Agent Output Data

All agents save their results:

```bash
# View agent outputs
ls -la src/data/

# Check recent trading decisions
cat src/data/agent_discussed_tokens.csv

# View backtest results
ls src/data/rbi/backtests/
```

---

## Next Steps

1. ✅ **Start Small:** Run individual agents to understand behavior
2. ✅ **Test Strategies:** Use RBI agent to backtest ideas
3. ✅ **Paper Trade:** Run without real money first
4. ✅ **Monitor:** Watch logs and agent outputs
5. ✅ **Customize:** Modify prompts and strategies for your needs
6. ✅ **Learn:** Join Discord, watch YouTube tutorials

---

**Built with ❤️ by Moon Dev - Pioneering AI-powered trading**

**Replicated & documented by Claude Code**

Last Updated: October 21, 2025
