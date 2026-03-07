#!/bin/bash
# Quick Start Script for Multi-Agent Platform
# Usage: ./quickstart.sh

set -e

echo "🚀 Multi-Agent Platform Quick Start"
echo "===================================="
echo ""

# Check if Nullclaw is installed
if ! command -v nullclaw &> /dev/null; then
    echo "⚠️  Nullclaw not found. Installing..."
    curl -L https://github.com/nullclaw/nullclaw/releases/latest/download/nullclaw-linux-x86_64.bin -o nullclaw
    chmod +x nullclaw
    sudo mv nullclaw /usr/local/bin/
    echo "✅ Nullclaw installed"
else
    echo "✅ Nullclaw already installed"
fi

echo ""
echo "📋 Step 1: Create Your First Customer"
echo "--------------------------------------"
echo ""

# Get customer name
read -p "Customer/Company Name: " CUSTOMER_NAME
read -p "Plan (free/starter/pro/enterprise) [starter]: " PLAN
PLAN=${PLAN:-starter}

# Create tenant
python3 tenant_manager.py create "$CUSTOMER_NAME" "$PLAN"

TENANT_ID="tenant_000"

echo ""
echo "📋 Step 2: Configure Nullclaw for Customer"
echo "-------------------------------------------"
echo ""

# Get OpenRouter API key
read -p "Enter OpenRouter API Key (or press Enter to skip): " API_KEY

if [ -n "$API_KEY" ]; then
    nullclaw onboard --api-key "$API_KEY" --provider openrouter
    echo "✅ Nullclaw configured"
else
    echo "⚠️  Skipping Nullclaw configuration (add API key later)"
fi

echo ""
echo "📋 Step 3: Add Telegram Bot (Optional)"
echo "---------------------------------------"
echo ""
echo "To add Telegram:"
echo "1. Message @BotFather on Telegram"
echo "2. Send: /newbot"
echo "3. Follow prompts to create bot"
echo "4. Copy the bot token"
echo "5. Update customer config:"
echo "   python3 tenant_manager.py update $TENANT_ID telegram_bot_token YOUR_TOKEN"
echo ""

read -p "Press Enter to continue..."

echo ""
echo "📋 Step 4: Test the Platform"
echo "-----------------------------"
echo ""

# Test agent routing
echo "🧪 Testing agent routing..."
python3 agents_platform.py route $TENANT_ID "Search for latest AI news"

echo ""
echo "🧪 Testing usage tracking..."
python3 usage_tracker.py record $TENANT_ID 100 "test-model" "test-agent"
python3 usage_tracker.py monthly $TENANT_ID

echo ""
echo "✅ Setup Complete!"
echo "=================="
echo ""
echo "Next Steps:"
echo "1. Add your OpenRouter API key to ~/.nullclaw/config.json"
echo "2. Add Telegram bot token: python3 tenant_manager.py update $TENANT_ID telegram_bot_token YOUR_TOKEN"
echo "3. Start Telegram bot: nullclaw channel start telegram"
echo "4. Test with: python3 agents_platform.py route $TENANT_ID 'Your task here'"
echo ""
echo "Documentation:"
echo "- README.md - Full documentation"
echo "- CONFIG_GUIDE.md - Detailed configuration"
echo "- SIMPLE_COMMANDS.md - Simple commands guide"
echo ""
