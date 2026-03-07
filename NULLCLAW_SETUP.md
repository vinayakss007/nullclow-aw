# Nullclaw Telegram Search Agent - Setup Complete! 

## What's Configured

Your Nullclaw agent is now set up with:
- **Telegram Bot** - Connected and ready
- **Internet Search** - Browser and HTTP request tools enabled
- **AI Provider** - OpenRouter (supports multiple free models)

## Important: Update Your API Key

You need to add a **real OpenRouter API key** for the AI to work:

1. Go to https://openrouter.ai/keys
2. Create a free API key
3. Run this command:
   ```bash
   nullclaw onboard --api-key YOUR_REAL_KEY --provider openrouter
   ```

## Test Your Bot

1. **Open Telegram**
2. **Find your bot** (search for the name you gave it)
3. **Send a message:**
   ```
   /start
   ```
4. **Try a search query:**
   ```
   Search for latest AI news
   ```

## Current Configuration

| Setting | Value |
|---------|-------|
| Bot Token | Configured ⚠️ (revoke and get new one!) |
| AI Provider | OpenRouter |
| Model | Claude Sonnet 4.6 |
| Search Tools | Enabled |
| Telegram | Configured |

## Commands

```bash
# Check status
nullclaw status

# Start agent
nullclaw agent

# Start gateway (for webhooks)
nullclaw gateway

# View logs
nullclaw logs
```

## Security Note

⚠️ **Your current bot token was shared publicly.** Consider:
1. Going to @BotFather in Telegram
2. Sending `/revoke` 
3. Getting a new token
4. Updating config: Edit `~/.nullclaw/config.json`

## Troubleshooting

**Bot doesn't respond:**
- Check if API key is valid: `nullclaw status`
- Check logs: `nullclaw logs`
- Run diagnostics: `nullclaw doctor`

**Search not working:**
- Browser tool is enabled in config
- HTTP request tool is enabled
- Make sure agent is running: `nullclaw agent`
