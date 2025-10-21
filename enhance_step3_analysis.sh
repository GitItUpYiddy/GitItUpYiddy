#!/bin/bash
# Enhancement Script 3: Add Advanced Analysis Agents

echo "🔧 Enhancement Step 3: Adding Advanced Analysis Agents..."
echo ""

# Copy analysis agents
echo "📦 Copying Whale Agent..."
cp /home/user/GitItUpYiddy/src/agents/whale_agent.py /home/user/GitItUpYiddy/ai-agents-2025/src/agents/

echo "📦 Copying Funding Agent..."
cp /home/user/GitItUpYiddy/src/agents/funding_agent.py /home/user/GitItUpYiddy/ai-agents-2025/src/agents/

echo "📦 Copying Liquidation Agent..."
cp /home/user/GitItUpYiddy/src/agents/liquidation_agent.py /home/user/GitItUpYiddy/ai-agents-2025/src/agents/

echo "📦 Copying Chart Analysis Agent..."
cp /home/user/GitItUpYiddy/src/agents/chartanalysis_agent.py /home/user/GitItUpYiddy/ai-agents-2025/src/agents/

echo ""
echo "✅ Analysis agents added successfully!"
echo ""
echo "📝 Available agents:"
echo "   • whale_agent.py - Track large wallet movements and whale activity"
echo "   • funding_agent.py - Monitor perpetual funding rates across exchanges"
echo "   • liquidation_agent.py - Track liquidation cascades (15min/1hr/4hr)"
echo "   • chartanalysis_agent.py - AI-powered chart pattern analysis"
echo ""
echo "🎯 Usage examples:"
echo "   python ai-agents-2025/src/agents/whale_agent.py"
echo "   python ai-agents-2025/src/agents/funding_agent.py"
echo "   python ai-agents-2025/src/agents/liquidation_agent.py"
echo "   python ai-agents-2025/src/agents/chartanalysis_agent.py"
echo ""
