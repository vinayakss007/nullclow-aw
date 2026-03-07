# AI Agents Platform (Nullclaw-based)

🤖 **Multi-tenant AI Agents Platform with Task Assignment & Sub-Agents** - Built on [Nullclaw](https://github.com/nullclaw/nullclaw)

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/coding4vinayak/nullclow-aw.git
cd nullclow-aw

# Install Nullclaw (Linux)
curl -L https://github.com/nullclaw/nullclaw/releases/latest/download/nullclaw-linux-x86_64.bin -o nullclaw
chmod +x nullclaw && sudo mv nullclaw /usr/local/bin/

# Create first customer
python3 tenant_manager.py create "Acme Corp" pro

# Route a task
python3 agents_platform.py route tenant_001 "Score this sales lead: Budget $10k, Timeline 1 month"

# Check usage
python3 usage_tracker.py report tenant_001
```

---

## 📦 Features

### ✅ Multi-Agent System
- **6 Pre-built Agents**: Sales, HR, Support, Research, Content, Office
- **18 Sub-Agents**: Specialized task handlers (lead_scorer, resume_screener, etc.)
- **Task Router**: Automatically assigns tasks to correct agent/sub-agent
- **Task Tracking**: Full task lifecycle management

### ✅ Multi-Tenant Platform
- **Isolated Workspaces**: Each customer gets separate data & memory
- **Usage Tracking**: Token usage per tenant with alerts
- **Pricing Tiers**: Free, Starter, Pro, Enterprise
- **Monthly Limits**: Automatic enforcement

### ✅ Tools Available
| Tool | Description |
|------|-------------|
| `browser` | Web search and browsing |
| `http_request` | API calls |
| `file_read/write/edit` | File operations |
| `memory_store/recall/forget` | Memory management |
| `shell` | Execute commands |
| `schedule` | Schedule tasks |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              Telegram / API Gateway             │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│              Agent Router                        │
│  (Routes tasks to correct agent/sub-agent)      │
└─────┬──────────────┬──────────────┬─────────────┘
      │              │              │
      ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│  Sales   │  │    HR    │  │ Support  │  ← Main Agents
│  Agent   │  │  Agent   │  │  Agent   │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     ▼             ▼             ▼
┌─────────┐  ┌──────────┐ ┌───────────┐
│ lead_   │  │ resume_  │ │ response_ │  ← Sub-Agents
│ scorer  │  │ screener │ │ generator │
│ email_  │  │ question │ │ ticket_   │
│ writer  │  │ generator│ │ classifier│
└─────────┘  └──────────┘ └───────────┘

┌─────────────────────────────────────────────────┐
│           Tenant Management Layer               │
│  - Isolated workspaces per customer            │
│  - Usage tracking & limits                     │
│  - Billing & plans                             │
└─────────────────────────────────────────────────┘
```

---

## 🤖 Available Agents

### 1. Sales Lead Agent
**Purpose**: Score and qualify sales leads automatically

**Sub-Agents**:
- `lead_scorer` - Score leads 0-100
- `email_writer` - Generate outreach emails
- `crm_updater` - Format data for CRM

**Example**:
```bash
python3 agents_platform.py route tenant_001 "Score this lead: Budget $50k, decision maker ready"
```

---

### 2. HR Screening Agent
**Purpose**: Screen resumes and rank candidates

**Sub-Agents**:
- `resume_screener` - Match resumes to job descriptions
- `question_generator` - Create interview questions
- `ranker` - Rank all candidates

**Example**:
```bash
python3 agents_platform.py route tenant_001 "Screen this resume for Python Developer role"
```

---

### 3. Support Agent
**Purpose**: Handle customer support tickets

**Sub-Agents**:
- `ticket_classifier` - Categorize and prioritize
- `response_generator` - Draft support responses
- `escalation_handler` - Flag urgent issues

**Example**:
```bash
python3 agents_platform.py route tenant_001 "Customer can't login, getting error 500"
```

---

### 4. Research Agent
**Purpose**: Research topics and summarize findings

**Sub-Agents**:
- `searcher` - Web search
- `summarizer` - Create summaries
- `citation_manager` - Track sources

**Example**:
```bash
python3 agents_platform.py route tenant_001 "Research latest AI trends in healthcare"
```

---

### 5. Content Agent
**Purpose**: Create content (blogs, social media, SEO)

**Sub-Agents**:
- `seo_analyzer` - Generate SEO keywords
- `blog_writer` - Write blog posts
- `social_media_manager` - Create social posts

**Example**:
```bash
python3 agents_platform.py route tenant_001 "Write blog post about remote work tools"
```

---

### 6. Office Assistant Agent
**Purpose**: General office tasks and scheduling

**Sub-Agents**:
- `scheduler` - Schedule meetings
- `note_taker` - Organize notes
- `reminder_manager` - Set reminders

**Example**:
```bash
python3 agents_platform.py route tenant_001 "Schedule team meeting for Friday 2pm"
```

---

## 💰 Pricing Tiers

| Plan | Price | Tokens/Month | Agents | Sub-Agents | Workspace |
|------|-------|--------------|--------|------------|-----------|
| **Free** | $0 | 10K | 1 | 1 | 100 MB |
| **Starter** | $29/mo | 100K | 3 | 5 | 500 MB |
| **Pro** | $99/mo | 500K | 10 | All | 5 GB |
| **Enterprise** | $499/mo | Unlimited | All | All | 50 GB |

---

## 🛠️ Installation

### 1. Get API Keys

**OpenRouter (AI Provider):**
1. Go to https://openrouter.ai/keys
2. Sign up / Login
3. Create API key
4. Copy key (starts with `sk-or-v1-`)

**Telegram Bot (per customer):**
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

### 3. Clone & Setup

```bash
# Clone repo
git clone https://github.com/coding4vinayak/nullclow-aw.git
cd nullclow-aw

# Create first customer
python3 tenant_manager.py create "Acme Corp" pro "acme@example.com" "TELEGRAM_BOT_TOKEN"

# Route a task
python3 agents_platform.py route tenant_001 "Search for AI news"

# Check usage
python3 usage_tracker.py report tenant_001
```

---

## 📱 Usage Examples

### Create Customer
```bash
# Free tier
python3 tenant_manager.py create "Test Company" free

# Starter tier with Telegram
python3 tenant_manager.py create "Acme Corp" starter "acme@example.com" "123456:ABC-DEF1234ghIkl"

# Enterprise
python3 tenant_manager.py create "Big Corp" enterprise "contact@bigcorp.com"
```

### Route Tasks
```bash
# Sales
python3 agents_platform.py route tenant_001 "Score this lead: Budget $10k, timeline 2 weeks"

# HR
python3 agents_platform.py route tenant_001 "Screen resume for Developer position"

# Research
python3 agents_platform.py route tenant_001 "Find trending topics in AI"

# Content
python3 agents_platform.py route tenant_001 "Generate SEO keywords for bakery website"
```

### Track Usage
```bash
# Record usage
python3 usage_tracker.py record tenant_001 1500 llama-3.3 sales_agent

# Check monthly usage
python3 usage_tracker.py monthly tenant_001

# Generate report
python3 usage_tracker.py report tenant_001

# View alerts
python3 usage_tracker.py alerts
```

### Manage Tenants
```bash
# List all
python3 tenant_manager.py list

# Get details
python3 tenant_manager.py get tenant_001

# Update plan
python3 tenant_manager.py update tenant_001 plan pro

# Usage report
python3 tenant_manager.py usage

# Reset monthly (run on 1st)
python3 tenant_manager.py reset-usage
```

---

## 🔒 Security

- ✅ Workspace isolation per tenant
- ✅ API key encryption
- ✅ Rate limiting per customer
- ✅ Usage tracking and alerts
- ✅ Directory traversal protection
- ✅ .env never committed to Git

---

## 📊 Monitoring

```bash
# Tenant usage
python3 tenant_manager.py usage

# All usage
python3 usage_tracker.py report

# Alerts
python3 usage_tracker.py alerts

# Task history
python3 agents_platform.py tasks tenant_001
```

---

## 🔄 Task Flow Example

```
User: "Score this sales lead and write email"
  │
  ▼
Agent Router
  │
  ├─→ lead_scorer (sub-agent)
  │     └─→ Score: 85/100
  │
  └─→ email_writer (sub-agent)
        └─→ Draft email generated
  
  ▼
Task Manager
  │
  ├─→ Record task
  ├─→ Track tokens
  └─→ Store result
  
  ▼
Response to User
```

---

## 🆘 Troubleshooting

### Bot doesn't respond
```bash
# Check logs
tail -f /var/log/nullclaw.log

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

### Database issues
```bash
# Reset usage tracker
rm usage.db
python3 usage_tracker.py  # Recreates tables
```

---

## 📈 Roadmap

- [x] Multi-agent system with sub-agents
- [x] Task routing and assignment
- [x] Multi-tenant support
- [x] Usage tracking
- [ ] Web dashboard
- [ ] Stripe billing integration
- [ ] Custom agent builder
- [ ] Analytics dashboard
- [ ] API for third-party integrations

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
- Contact: vinayak@example.com

---

**Built with ❤️ using Nullclaw**
