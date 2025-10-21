#!/bin/bash
# Enhancement Script 2: Add RBI Agent (Strategy Generator from YouTube Videos)

echo "🔧 Enhancement Step 2: Adding RBI Agent..."
echo ""

# Copy RBI agents
echo "📦 Copying RBI Agent (Strategy Generator)..."
cp /home/user/GitItUpYiddy/src/agents/rbi_agent.py /home/user/GitItUpYiddy/ai-agents-2025/src/agents/
cp /home/user/GitItUpYiddy/src/agents/rbi_agent_v2.py /home/user/GitItUpYiddy/ai-agents-2025/src/agents/
cp /home/user/GitItUpYiddy/src/agents/backtest_runner.py /home/user/GitItUpYiddy/ai-agents-2025/src/agents/

# Update requirements
echo "📦 Adding RBI dependencies..."
cat >> /home/user/GitItUpYiddy/ai-agents-2025/requirements.txt << 'EOF'

# RBI Agent Dependencies (Strategy Generator)
youtube-transcript-api>=0.6.0
backtesting>=0.3.3
talib-binary>=0.4.24
EOF

echo ""
echo "✅ RBI Agent added successfully!"
echo ""
echo "📝 Usage:"
echo "   python ai-agents-2025/src/agents/rbi_agent.py"
echo ""
echo "   When prompted, enter a YouTube URL of any trading strategy video"
echo "   The agent will:"
echo "      1. Download & transcribe the video"
echo "      2. Extract the trading strategy"
echo "      3. Generate backtesting code"
echo "      4. Run the backtest"
echo "      5. Return performance metrics"
echo ""
echo "💰 Cost: ~\$0.027 per backtest (6 minutes)"
echo ""
