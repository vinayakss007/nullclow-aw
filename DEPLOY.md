# Deploy Nullclaw Telegram Agent

## Option 1: Deploy as Background Service (Linux Server)

### Install on Server
```bash
# Download Nullclaw
curl -L https://github.com/nullclaw/nullclaw/releases/latest/download/nullclaw-linux-x86_64.bin -o nullclaw
chmod +x nullclaw
sudo mv nullclaw /usr/local/bin/

# Verify
nullclaw version
```

### Configure
```bash
# Run interactive setup
nullclaw onboard --interactive

# Or with API key directly
nullclaw onboard --api-key sk-or-YOUR_KEY --provider openrouter
```

### Add Telegram to Config
```bash
# Edit config
nano ~/.nullclaw/config.json

# Add under "channels":
"telegram": {
  "accounts": {
    "main": {
      "bot_token": "YOUR_BOT_TOKEN",
      "allow_from": ["all"],
      "reply_in_private": true
    }
  }
}
```

### Enable Browser/Search
```bash
# Edit config and set:
"browser": {"enabled": true},
"http_request": {"enabled": true}
```

### Install as Service
```bash
# Install systemd service
nullclaw service install

# Start service
nullclaw service start

# Check status
nullclaw service status
```

### Auto-start on Boot
```bash
# Enable systemd service
systemctl --user enable nullclaw.service
systemctl --user start nullclaw.service
```

---

## Option 2: Docker Deployment

### Create Dockerfile
```dockerfile
FROM nullclaw/nullclaw:latest

COPY config.json /root/.nullclaw/config.json

EXPOSE 3000

CMD ["nullclaw", "gateway"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  nullclaw:
    image: nullclaw/nullclaw:latest
    container_name: telegram-bot
    restart: unless-stopped
    volumes:
      - ./config.json:/root/.nullclaw/config.json
      - ./workspace:/root/.nullclaw/workspace
      - nullclaw-memory:/root/.nullclaw/memory
    ports:
      - "3000:3000"
    environment:
      - OPENROUTER_API_KEY=sk-or-YOUR_KEY
    networks:
      - bot-network

volumes:
  nullclaw-memory:

networks:
  bot-network:
```

### Deploy
```bash
docker-compose up -d
```

---

## Option 3: Cloud Deployment (VPS)

### Deploy to DigitalOcean/AWS/Linode

1. **Create Ubuntu 22.04 VPS** (minimum $5/month)

2. **SSH into server:**
   ```bash
   ssh root@your-server-ip
   ```

3. **Install Nullclaw:**
   ```bash
   curl -L https://github.com/nullclaw/nullclaw/releases/latest/download/nullclaw-linux-x86_64.bin -o nullclaw
   chmod +x nullclaw
   sudo mv nullclaw /usr/local/bin/
   ```

4. **Configure:**
   ```bash
   nullclaw onboard --api-key sk-or-YOUR_KEY --provider openrouter
   ```

5. **Add Telegram config** (edit `~/.nullclaw/config.json`)

6. **Start as service:**
   ```bash
   nullclaw service install
   nullclaw service start
   ```

7. **Enable auto-start:**
   ```bash
   systemctl --user enable nullclaw.service
   ```

---

## Option 4: Run Continuously (Simple)

### Using tmux (keeps running after disconnect)
```bash
# Install tmux
sudo apt install tmux

# Create session
tmux new -s nullclaw

# Run agent
nullclaw agent

# Detach (keeps running): Ctrl+B, then D
```

### Using nohup
```bash
nohup nullclaw agent > nullclaw.log 2>&1 &
```

### Using screen
```bash
screen -S nullclaw
nullclaw agent
# Detach: Ctrl+A, then D
```

---

## Verify Deployment

```bash
# Check service status
nullclaw service status

# Check channels
nullclaw channel status

# View logs
nullclaw logs

# Test bot
# Send message on Telegram: "Hello"
```

---

## Quick Deploy Script

Save as `deploy.sh`:
```bash
#!/bin/bash

echo "Installing Nullclaw..."
curl -L https://github.com/nullclaw/nullclaw/releases/latest/download/nullclaw-linux-x86_64.bin -o nullclaw
chmod +x nullclaw
sudo mv nullclaw /usr/local/bin/

echo "Configuring..."
read -p "Enter OpenRouter API Key: " API_KEY
nullclaw onboard --api-key $API_KEY --provider openrouter

echo "Adding Telegram..."
read -p "Enter Telegram Bot Token: " BOT_TOKEN
jq --arg token "$BOT_TOKEN" '.channels.telegram = {"accounts": {"main": {"bot_token": $token, "allow_from": ["all"], "reply_in_private": true}}}' ~/.nullclaw/config.json > /tmp/config.json && mv /tmp/config.json ~/.nullclaw/config.json

echo "Enabling search..."
jq '.browser.enabled = true | .http_request.enabled = true' ~/.nullclaw/config.json > /tmp/config.json && mv /tmp/config.json ~/.nullclaw/config.json

echo "Installing service..."
nullclaw service install
nullclaw service start

echo "Done! Test your bot on Telegram."
```

Run:
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## Monitoring

```bash
# Real-time logs
nullclaw logs --follow

# Status check
nullclaw status

# Channel health
nullclaw channel status

# Memory usage
nullclaw memory stats
```

---

## Troubleshooting

**Service won't start:**
```bash
nullclaw doctor
nullclaw logs
```

**Bot offline:**
```bash
nullclaw service restart
nullclaw channel start telegram
```

**Update Nullclaw:**
```bash
nullclaw update
```
