# Simple Telegram Search Agent with Nullclaw

## Prerequisites

### 1. Install Nullclaw
```bash
# Option A: Using Homebrew (macOS/Linux)
brew install nullclaw

# Option B: Build from source
git clone https://github.com/nullclaw/nullclaw.git
cd nullclaw
zig build -Doptimize=ReleaseSmall
sudo cp zig-out/bin/nullclaw /usr/local/bin/
```

### 2. Get Telegram Bot Token
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 3. Get Your Telegram Username
- Your username is what appears after @ in your Telegram profile
- Example: if your profile is @john_doe, your username is `john_doe`

### 4. Get Free AI API Key (OpenRouter)
1. Go to https://openrouter.ai
2. Sign up for free
3. Create an API key
4. Copy the key (starts with `sk-or-`)

---

## Setup Steps

### Step 1: Configure Nullclaw
```bash
# Run interactive setup
nullclaw onboard --interactive
```

Or manually edit the config:
```bash
# Config location
~/.nullclaw/config.json
```

### Step 2: Update Configuration
Edit `nullclaw-config.json` with your credentials:
- Replace `YOUR_TELEGRAM_BOT_TOKEN` with your bot token
- Replace `your_telegram_username` with your Telegram username
- Replace `YOUR_OPENROUTER_API_KEY` with your API key

Then copy to Nullclaw config directory:
```bash
cp nullclaw-config.json ~/.nullclaw/config.json
```

### Step 3: Start the Agent
```bash
# Start Telegram channel
nullclaw channel start telegram

# Or start the gateway (for webhook mode)
nullclaw gateway
```

### Step 4: Test Your Bot
1. Open Telegram
2. Search for your bot by name
3. Send `/start`
4. Send a message like: "Search for latest AI news"

---

## Commands Reference

```bash
# Check status
nullclaw status
nullclaw channel status

# Start/stop channels
nullclaw channel start telegram
nullclaw channel stop telegram

# Run agent directly
nullclaw agent -m "Hello!"

# Interactive chat
nullclaw agent

# View logs
nullclaw logs
```

---

## Example Messages to Test

```
Search for today's top tech news
What's the weather like today?
Find information about Node.js tutorials
Search for cryptocurrency prices
```

---

## Troubleshooting

### Bot doesn't respond
1. Check if Telegram channel is running: `nullclaw channel status`
2. Verify your username is in `allow_from` list
3. Check logs: `nullclaw logs`

### API errors
1. Verify API keys are correct
2. Check internet connection
3. Try: `nullclaw doctor`

### Config issues
```bash
# Validate config
nullclaw config validate
```

---

## Learning Resources

- Nullclaw Docs: https://nullclaw.io
- GitHub: https://github.com/nullclaw/nullclaw
- Community: Check the GitHub discussions
