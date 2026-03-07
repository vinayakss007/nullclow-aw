# Complete Configuration Guide
## Step-by-Step Setup for Your AI Agents Platform

---

## 📋 OVERVIEW

You need to configure **3 things**:

1. **GitHub Repository** - Your code storage
2. **Server** - Where bot runs (for customers)
3. **Nullclaw** - AI engine (per customer)

---

## PART 1: GITHUB REPOSITORY SETUP

### Step 1: Create Repository
```bash
# Go to github.com
# Click "New" or "+" → "New repository"
# Name: ai-agents-platform
# Description: "Multi-tenant AI Agents Platform built on Nullclaw"
# Public or Private (your choice)
# Click "Create repository"
```

### Step 2: Create Folder Structure on Your Computer
```bash
# On your local computer
mkdir ai-agents-platform
cd ai-agents-platform

# Create folders
mkdir -p agents/sales_agent
mkdir -p agents/hr_agent
mkdir -p agents/support_agent
mkdir -p platform
mkdir -p deployment
mkdir -p docs
mkdir -p dashboard

# Initialize git
git init
```

### Step 3: Create Required Files

#### README.md
```markdown
# AI Agents Platform

Multi-tenant AI platform for businesses. Built on [Nullclaw](https://github.com/nullclaw/nullclaw).

## Features
- Sales Lead Scoring Agent
- HR Screening Agent
- Customer Support Agent
- Office Assistant Agent

## Quick Start
```bash
git clone https://github.com/YOURNAME/ai-agents-platform
cd ai-agents-platform
docker-compose up -d
```

## Pricing
- Free: 10K tokens/month
- Starter: $29/mo (100K tokens)
- Pro: $99/mo (500K tokens)
- Enterprise: $499/mo (unlimited)

## License
MIT
```

#### .gitignore
```gitignore
# Customer data - NEVER commit
customers/
tenant_*/
*.db
*.sqlite

# API Keys - NEVER commit
.env
*.key
config.json
secrets.json

# Logs
logs/
*.log

# Python
__pycache__/
*.pyc
*.pyo
.env

# Node
node_modules/

# IDE
.vscode/
.idea/
```

#### .env.example
```bash
# Copy this to .env and fill in your values

# OpenRouter API Key (get from https://openrouter.ai)
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Database
DATABASE_URL=sqlite:///platform.db

# Telegram Bot (for platform notifications)
ADMIN_TELEGRAM_BOT_TOKEN=your-bot-token

# Stripe (for billing)
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

### Step 4: Create Basic Platform Code

#### platform/tenant_manager.py
```python
#!/usr/bin/env python3
"""
Tenant Manager - Create and manage customer workspaces
"""

import os
import json
from pathlib import Path

class TenantManager:
    def __init__(self, base_path="./customers"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
    
    def create_tenant(self, name, plan="starter"):
        """Create a new tenant workspace"""
        tenant_id = f"tenant_{len(list(self.base_path.glob('tenant_*'))):03d}"
        tenant_path = self.base_path / tenant_id
        
        # Create workspace
        (tenant_path / "workspace").mkdir(parents=True, exist_ok=True)
        (tenant_path / "data").mkdir(parents=True, exist_ok=True)
        
        # Create config
        config = {
            "name": name,
            "plan": plan,
            "monthly_token_limit": self._get_plan_limit(plan),
            "allowed_agents": self._get_plan_agents(plan)
        }
        
        with open(tenant_path / "config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Created tenant: {tenant_id} ({name})")
        return tenant_id
    
    def _get_plan_limit(self, plan):
        limits = {
            "free": 10000,
            "starter": 100000,
            "pro": 500000,
            "enterprise": -1  # unlimited
        }
        return limits.get(plan, 10000)
    
    def _get_plan_agents(self, plan):
        agents = {
            "free": ["basic"],
            "starter": ["sales", "support"],
            "pro": ["sales", "support", "hr", "office"],
            "enterprise": ["all"]
        }
        return agents.get(plan, ["basic"])
    
    def list_tenants(self):
        """List all tenants"""
        tenants = []
        for tenant_path in self.base_path.glob("tenant_*"):
            config_file = tenant_path / "config.json"
            if config_file.exists():
                with open(config_file) as f:
                    config = json.load(f)
                tenants.append({
                    "id": tenant_path.name,
                    **config
                })
        return tenants

# CLI
if __name__ == "__main__":
    import sys
    
    manager = TenantManager()
    
    if len(sys.argv) < 2:
        print("Usage: python tenant_manager.py <command> [args]")
        print("Commands:")
        print("  create <name> [plan]  - Create new tenant")
        print("  list                  - List all tenants")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "create":
        name = sys.argv[2] if len(sys.argv) > 2 else "New Customer"
        plan = sys.argv[3] if len(sys.argv) > 3 else "starter"
        manager.create_tenant(name, plan)
    
    elif command == "list":
        tenants = manager.list_tenants()
        for t in tenants:
            print(f"{t['id']}: {t['name']} ({t['plan']})")
```

#### platform/usage_tracker.py
```python
#!/usr/bin/env python3
"""
Usage Tracker - Track AI token usage per tenant
"""

import sqlite3
from datetime import datetime

class UsageTracker:
    def __init__(self, db_path="./usage.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
    
    def _create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS usage_log (
                id INTEGER PRIMARY KEY,
                tenant_id TEXT,
                tokens INTEGER,
                model TEXT,
                agent TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
    
    def record(self, tenant_id, tokens, model="unknown", agent="unknown"):
        """Record token usage"""
        self.conn.execute("""
            INSERT INTO usage_log (tenant_id, tokens, model, agent)
            VALUES (?, ?, ?, ?)
        """, (tenant_id, tokens, model, agent))
        self.conn.commit()
    
    def get_monthly_usage(self, tenant_id):
        """Get total tokens used this month"""
        result = self.conn.execute("""
            SELECT SUM(tokens) FROM usage_log 
            WHERE tenant_id = ? 
            AND strftime('%Y-%m', timestamp) = strftime('%Y-%m', 'now')
        """, (tenant_id,)).fetchone()
        return result[0] or 0
    
    def check_limit(self, tenant_id, limit):
        """Check if tenant exceeded limit"""
        if limit < 0:  # unlimited
            return True
        used = self.get_monthly_usage(tenant_id)
        return used < limit

# Test
if __name__ == "__main__":
    tracker = UsageTracker()
    tracker.record("tenant_001", 1000, "llama-3.3", "sales_agent")
    print(f"Usage: {tracker.get_monthly_usage('tenant_001')} tokens")
```

### Step 5: Push to GitHub
```bash
# Add all files
git add .

# Commit
git commit -m "Initial commit: AI Agents Platform structure"

# Add remote (replace YOURNAME with your GitHub username)
git remote add origin https://github.com/YOURNAME/ai-agents-platform

# Push
git push -u origin main
```

---

## PART 2: SERVER SETUP (For Each Customer)

### Step 1: Get a VPS (Virtual Private Server)

**Recommended Providers:**
- DigitalOcean: $6-12/month (https://digitalocean.com)
- Linode: $5-10/month (https://linode.com)
- Hetzner: €5/month (https://hetzner.com)

**Minimum Specs:**
- 1 CPU
- 1 GB RAM
- 25 GB SSD

### Step 2: Connect to Your Server
```bash
# SSH into your server
ssh root@your-server-ip
```

### Step 3: Install Dependencies
```bash
# Update system
apt update && apt upgrade -y

# Install Python
apt install python3 python3-pip -y

# Install Git
apt install git -y

# Install Docker (optional)
curl -fsSL https://get.docker.com | sh
```

### Step 4: Download Nullclaw
```bash
# Download binary
curl -L https://github.com/nullclaw/nullclaw/releases/latest/download/nullclaw-linux-x86_64.bin -o nullclaw

# Make executable
chmod +x nullclaw

# Move to system path
mv nullclaw /usr/local/bin/

# Verify
nullclaw version
```

### Step 5: Clone Your Platform
```bash
# Clone from GitHub
git clone https://github.com/YOURNAME/ai-agents-platform
cd ai-agents-platform

# Create .env from example
cp .env.example .env

# Edit .env with your API key
nano .env
# Add: OPENROUTER_API_KEY=sk-or-v1-your-actual-key
```

### Step 6: Create First Customer
```bash
# Run tenant manager
python3 platform/tenant_manager.py create "Acme Corp" pro

# This creates:
# ./customers/tenant_001/
# ├── config.json
# ├── workspace/
# └── data/
```

### Step 7: Configure Nullclaw for Customer
```bash
# Initialize Nullclaw for this tenant
nullclaw onboard --api-key sk-or-v1-your-key --provider openrouter

# Edit config to add Telegram
nano ~/.nullclaw/config.json

# Add under "channels":
"telegram": {
  "accounts": {
    "main": {
      "bot_token": "CUSTOMER_BOT_TOKEN",
      "allow_from": ["all"],
      "reply_in_private": true
    }
  }
}
```

### Step 8: Start the Bot
```bash
# Start Telegram channel
nohup nullclaw channel start telegram > /var/log/nullclaw.log 2>&1 &

# Check it's running
ps aux | grep nullclaw
```

---

## PART 3: NULLCLAW CONFIGURATION

### Required Config File (~/.nullclaw/config.json)

```json
{
  "models": {
    "providers": {
      "openrouter": {
        "api_key": "sk-or-v1-YOUR-KEY-HERE"
      }
    }
  },

  "agents": {
    "defaults": {
      "model": {
        "primary": "openrouter/meta-llama/llama-3.3-70b-instruct",
        "fallback": [
          "openrouter/arcee-ai/trinity-large-preview:free",
          "openrouter/z-ai/glm-4.5-air:free"
        ]
      }
    }
  },

  "channels": {
    "telegram": {
      "accounts": {
        "main": {
          "bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
          "allow_from": ["all"],
          "reply_in_private": true
        }
      }
    }
  },

  "browser": {
    "enabled": true,
    "allowed_domains": []
  },

  "http_request": {
    "enabled": true,
    "allowed_domains": []
  },

  "memory": {
    "backend": "hybrid",
    "auto_save": true
  },

  "autonomy": {
    "level": "supervised",
    "workspace_only": true,
    "max_actions_per_hour": 20
  }
}
```

---

## PART 4: GET TELEGRAM BOT TOKEN

### Step 1: Open Telegram
Search for `@BotFather`

### Step 2: Create Bot
```
Send: /newbot
BotFather: Choose a name
You: Acme Corp Assistant
BotFather: Choose username
You: acme_corp_bot
BotFather: Done! Token: 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

### Step 3: Save Token
Copy the token and add to Nullclaw config:
```json
"telegram": {
  "accounts": {
    "main": {
      "bot_token": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    }
  }
}
```

---

## PART 5: GET OPENROUTER API KEY

### Step 1: Go to OpenRouter
https://openrouter.ai/keys

### Step 2: Sign Up / Login
Create account or login

### Step 3: Create Key
Click "Create Key"
Name: "AI Platform"
Copy the key (starts with `sk-or-v1-`)

### Step 4: Add to Config
```bash
nano ~/.nullclaw/config.json
# Add your key in models.providers.openrouter.api_key
```

---

## ✅ VERIFICATION CHECKLIST

### GitHub
- [ ] Repository created
- [ ] Files pushed
- [ ] .gitignore includes customers/ and .env

### Server
- [ ] Nullclaw installed (`nullclaw version` works)
- [ ] Platform code cloned
- [ ] .env file created with API key

### Customer
- [ ] Tenant created (`tenant_001`)
- [ ] Telegram bot token added
- [ ] Bot responds to `/start`

### Testing
```bash
# Check Nullclaw
nullclaw status

# Check tenant
ls customers/tenant_001/

# Check bot
# Send message on Telegram to your bot
```

---

## 🚨 TROUBLESHOOTING

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

# Check config
cat ~/.nullclaw/config.json
```

### Tenant not created
```bash
# Run manually
python3 platform/tenant_manager.py create "Test" free

# Check
ls -la customers/
```

---

## 📊 QUICK REFERENCE

### Commands You'll Use Often

```bash
# Create customer
python3 platform/tenant_manager.py create "Company Name" pro

# List customers
python3 platform/tenant_manager.py list

# Check usage
python3 platform/usage_tracker.py

# Restart bot
pkill nullclaw && nohup nullclaw channel start telegram > /var/log/nullclaw.log 2>&1 &

# View logs
tail -f /var/log/nullclaw.log
```

---

## 🎯 NEXT STEPS

After basic setup:
1. Add more agents (sales, HR, support)
2. Add Stripe billing
3. Build web dashboard
4. Add monitoring
5. Market to customers

---

**You're ready! Start with GitHub repo creation now!** 🚀
