# AI Agents Platform (Nullclaw-based)

🤖 **Multi-tenant AI Agents Platform for businesses** - Built on [Nullclaw](https://github.com/nullclaw/nullclaw)

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/coding4vinayak/nullclow-aw.git
cd nullclow-aw

# Install Nullclaw (Linux)
curl -L https://github.com/nullclaw/nullclaw/releases/latest/download/nullclaw-linux-x86_64.bin -o nullclaw
chmod +x nullclaw && sudo mv nullclaw /usr/local/bin/

# Configure
nullclaw onboard --api-key YOUR_OPENROUTER_KEY --provider openrouter

# Start Telegram bot
nullclaw channel start telegram
```

---

## 📦 Features

### Pre-built Agents
- ✅ **Sales Lead Agent** - Score and qualify leads automatically
- ✅ **HR Screening Agent** - Screen resumes and rank candidates
- ✅ **Support Agent** - Handle customer support tickets
- ✅ **Office Assistant** - General office tasks and scheduling

### Platform Features
- 🌐 Internet search via browser & HTTP requests
- 🧠 Long-term memory per customer
- 📁 File operations (read/write/edit)
- 💻 Shell command execution
- 📊 Usage tracking per tenant
- 🔒 Isolated workspaces per customer

### Tools Available
| Tool | Description |
|------|-------------|
| `browser` | Web search and browsing |
| `http_request` | API calls |
| `file_read/write/edit` | File operations |
| `memory_store/recall/forget` | Memory management |
| `shell` | Execute commands |
| `git` | Git operations |
| `schedule` | Schedule tasks |

---

## 💰 Pricing Tiers

| Plan | Price | Tokens/Month | Agents | Workspace |
|------|-------|--------------|--------|-----------|
| **Free** | $0 | 10K | 1 | 100 MB |
| **Starter** | $29/mo | 100K | 3 | 500 MB |
| **Pro** | $99/mo | 500K | 10 | 5 GB |
| **Enterprise** | $499/mo | Unlimited | All | 50 GB |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│         Your VPS Server             │
│  ┌──────────────────────────────┐  │
│  │   Nullclaw (3.3 MB binary)   │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │   Platform Code (this repo)  │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │   /customers/                │  │
│  │   ├── tenant_001/ (isolated) │  │
│  │   ├── tenant_002/ (isolated) │  │
│  │   └── tenant_003/ (isolated) │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│   OpenRouter API        │
│   (AI Models)           │
└─────────────────────────┘
```

---

## 📁 Project Structure

```
nullclow-aw/
├── README.md                 # This file
├── CONFIG_GUIDE.md           # Detailed setup guide
├── PLATFORM_STRATEGY.md      # Business strategy
├── TELEGRAM_COMMANDS.md      # Bot commands guide
├── .gitignore               # Git ignore rules
├── .env.example             # Environment template
│
├── agents/                   # Agent definitions
│   ├── sales_agent/
│   ├── hr_agent/
│   └── support_agent/
│
├── platform/                 # Platform code
│   ├── tenant_manager.py    # Create/manage customers
│   └── usage_tracker.py     # Track AI usage
│
├── deployment/               # Deployment configs
│   ├── docker-compose.yml
│   └── scripts/
│
└── docs/                     # Documentation
    └── setup.md
```

---

## 🛠️ Installation

### 1. Get API Keys

**OpenRouter (AI Provider):**
1. Go to https://openrouter.ai/keys
2. Sign up / Login
3. Create API key
4. Copy key (starts with `sk-or-v1-`)

**Telegram Bot:**
1. Open Telegram
2. Message `@BotFather`
3. Send `/newbot`
4. Follow prompts
5. Copy bot token

### 2. Install on Server

```bash
# Update system
apt update && apt upgrade -y

# Install Python
apt install python3 python3-pip git -y

# Download Nullclaw
curl -L https://github.com/nullclaw/nullclaw/releases/latest/download/nullclaw-linux-x86_64.bin -o nullclaw
chmod +x nullclaw && sudo mv nullclaw /usr/local/bin/

# Verify
nullclaw version
```

### 3. Configure

```bash
# Clone repo
git clone https://github.com/coding4vinayak/nullclow-aw.git
cd nullclow-aw

# Initialize Nullclaw
nullclaw onboard --api-key sk-or-v1-YOUR_KEY --provider openrouter

# Add Telegram to config
nano ~/.nullclaw/config.json
# Add Telegram config (see CONFIG_GUIDE.md)
```

### 4. Create First Customer

```bash
cd nullclow-aw
python3 platform/tenant_manager.py create "Acme Corp" pro
```

### 5. Start Bot

```bash
nohup nullclaw channel start telegram > /var/log/nullclaw.log 2>&1 &

# Check status
nullclaw status
```

---

## 📱 Telegram Bot Commands

### General
```
/start - Start the bot
/help - Show help
/status - Show system status
```

### Search
```
Search for [topic]
Browse [URL]
Get [API URL]
```

### Memory
```
Remember [information]
What do you remember about me?
Forget [topic]
```

### Files
```
Create [file] with: [content]
Read [file]
Edit [file]: change [old] to [new]
```

### Shell
```
Run: [command]
Execute: [command]
```

---

## 🔒 Security

- ✅ Workspace isolation per tenant
- ✅ API key encryption
- ✅ Rate limiting per customer
- ✅ Usage tracking and limits
- ✅ Directory traversal protection

---

## 📊 Monitoring

```bash
# Check usage
python3 platform/usage_tracker.py

# View logs
tail -f /var/log/nullclaw.log

# Check status
nullclaw status
nullclaw channel status
```

---

## 🆘 Troubleshooting

### Bot doesn't respond
```bash
# Check logs
cat /var/log/nullclaw.log

# Restart
pkill nullclaw
nohup nullclaw channel start telegram > /var/log/nullclaw.log 2>&1 &
```

### API errors
```bash
# Test API key
curl -H "Authorization: Bearer sk-or-v1-xxx" https://openrouter.ai/api/v1/auth/key
```

### Check Nullclaw
```bash
nullclaw doctor
nullclaw status
```

---

## 📈 Roadmap

- [x] Basic Telegram bot
- [x] Internet search capability
- [x] Multi-tenant support
- [ ] Web dashboard
- [ ] Stripe billing integration
- [ ] More pre-built agents
- [ ] Analytics dashboard

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🔗 Links

- [Nullclaw Documentation](https://github.com/nullclaw/nullclaw)
- [OpenRouter API](https://openrouter.ai)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

## 💬 Support

For issues and questions:
- Create an issue on GitHub
- Contact: [your-email@example.com]

---

**Built with ❤️ using Nullclaw**
