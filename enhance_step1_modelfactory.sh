#!/bin/bash
# Enhancement Script 1: Add Multi-LLM Support to NEW 2025 Repo

echo "🔧 Enhancement Step 1: Adding Multi-LLM Support..."
echo ""

# Copy ModelFactory
echo "📦 Copying ModelFactory from mature repo..."
cp -r /home/user/GitItUpYiddy/src/models /home/user/GitItUpYiddy/ai-agents-2025/src/

# Update requirements
echo "📦 Adding LLM provider dependencies..."
cat >> /home/user/GitItUpYiddy/ai-agents-2025/requirements.txt << 'EOF'

# Multi-LLM Support (Added by enhancement)
openai>=1.3.0
groq>=0.4.0
google-generativeai>=0.3.0
EOF

echo ""
echo "✅ ModelFactory added successfully!"
echo ""
echo "📝 Next Steps:"
echo "   1. cd ai-agents-2025"
echo "   2. pip install -r requirements.txt"
echo "   3. Update agents to use ModelFactory:"
echo ""
echo "      from src.models.model_factory import ModelFactory"
echo "      model = ModelFactory.create_model('anthropic')  # or 'groq', 'openai', etc."
echo ""
echo "🎯 You can now use:"
echo "   ✅ Anthropic Claude (all models)"
echo "   ✅ OpenAI GPT (all models)"
echo "   ✅ Groq (FREE tier!)"
echo "   ✅ DeepSeek (cheapest reasoning)"
echo "   ✅ Google Gemini"
echo "   ✅ Ollama (local, completely free)"
echo "   ✅ XAI Grok"
echo ""
