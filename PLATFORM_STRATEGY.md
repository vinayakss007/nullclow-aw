# Nullclaw Multi-Tenant AI Agents Platform
## Complete Strategy & Implementation Guide

---

## 📋 TABLE OF CONTENTS

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [GitHub Repository Structure](#github-repository-structure)
4. [Agent Types](#agent-types)
5. [Multi-Tenant Deployment](#multi-tenant-deployment)
6. [Customer Data Isolation](#customer-data-isolation)
7. [AI Usage Control & Pricing](#ai-usage-control--pricing)
8. [Deployment Options](#deployment-options)
9. [Step-by-Step Implementation](#step-by-step-implementation)
10. [Cost & Revenue Model](#cost--revenue-model)

---

## 1. OVERVIEW

### What You're Building

A **Multi-Tenant AI Agent Platform** where:
- Multiple customers (tenants) have isolated workspaces
- Each customer has their own data, agents, and usage limits
- You control AI usage per customer (pricing tiers)
- Customers can add data → Agents work on that data
- Central dashboard for you to manage everything

### Business Model

```
You (Platform Owner)
       │
       ├── Customer A (Sales Team) → Sales Lead Agent
       ├── Customer B (HR) → HR Screening Agent
       ├── Customer C (Support) → Support Agent
       └── Customer D (Enterprise) → All Agents + Custom
```

---

## 2. ARCHITECTURE

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CENTRAL PLATFORM                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Management Dashboard                    │   │
│  │  - Customer management                               │   │
│  │  - Usage monitoring                                  │   │
│  │  - Billing & plans                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│         ┌────────────────┼────────────────┐                │
│         │                │                │                │
│    ┌────▼────┐     ┌────▼────┐     ┌────▼────┐           │
│    │Tenant A │     │Tenant B │     │Tenant C │           │
│    │Workspace│     │Workspace│     │Workspace│           │
│    │ + Data  │     │ + Data  │     │ + Data  │           │
│    │ + Agent │     │ + Agent │     │ + Agent │           │
│    └────┬────┘     └────┬────┘     └────┬────┘           │
│         │                │                │                │
└─────────┼────────────────┼────────────────┼────────────────┘
          │                │                │
    ┌─────▼────────────────▼────────────────▼─────┐
    │           SHARED AI PROVIDERS                │
    │  - OpenRouter API (your master key)          │
    │  - Rate limiting per tenant                  │
    │  - Usage tracking                            │
    └──────────────────────────────────────────────┘
```

### Component Flow

```
Customer Telegram/Dashboard
         │
         ▼
┌─────────────────┐
│  API Gateway    │ ← Authentication & Rate Limiting
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Tenant Router  │ ← Routes to correct workspace
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Customer Agent  │ ← Sales/HR/Support Agent
│ + Customer Data │ ← Isolated per customer
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AI Provider    │ ← Your OpenRouter key (tracked)
└─────────────────┘
```

---

## 3. GITHUB REPOSITORY STRUCTURE

### Save This on GitHub

```
github.com/yourusername/ai-agents-platform/
│
├── README.md                    # Platform overview
├── LICENSE                      # MIT or Commercial
├── .env.example                 # Environment template
│
├── platform/                    # CORE PLATFORM
│   ├── config.py               # Platform configuration
│   ├── database.py             # Database connections
│   ├── auth.py                 # Authentication
│   ├── rate_limiter.py         # AI usage limits
│   └── billing.py              # Pricing & plans
│
├── agents/                      # AGENT DEFINITIONS
│   ├── base_agent.py           # Base agent class
│   ├── sales_agent/            # Sales Lead Agent
│   │   ├── agent.py
│   │   ├── prompts.py
│   │   └── tools.py
│   ├── hr_agent/               # HR Screening Agent
│   │   ├── agent.py
│   │   ├── prompts.py
│   │   └── tools.py
│   ├── support_agent/          # Support Agent
│   │   ├── agent.py
│   │   ├── prompts.py
│   │   └── tools.py
│   └── office_agent/           # General Office Agent
│       ├── agent.py
│       ├── prompts.py
│       └── tools.py
│
├── tenants/                     # TENANT MANAGEMENT
│   ├── manager.py              # Create/list/delete tenants
│   ├── workspace.py            # Workspace isolation
│   └── data_loader.py          # Customer data ingestion
│
├── deployment/                  # DEPLOYMENT CONFIGS
│   ├── docker-compose.yml      # Multi-tenant setup
│   ├── kubernetes/             # K8s configs
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── ingress.yaml
│   ├── systemd/                # Linux service files
│   │   ├── platform.service
│   │   └── tenant@.service
│   └── scripts/
│       ├── deploy.sh
│       ├── backup.sh
│       └── migrate.sh
│
├── dashboard/                   # WEB DASHBOARD
│   ├── app.py                  # Flask/FastAPI dashboard
│   ├── templates/
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── usage.html
│   │   └── billing.html
│   └── static/
│       └── css/
│
├── api/                         # REST API
│   ├── routes/
│   │   ├── tenants.py
│   │   ├── agents.py
│   │   ├── usage.py
│   │   └── billing.py
│   └── middleware/
│       └── auth.py
│
├── monitoring/                  # MONITORING
│   ├── usage_tracker.py        # Track AI usage per tenant
│   ├── alerts.py               # Usage alerts
│   └── reports.py              # Usage reports
│
├── customers/                   # CUSTOMER DATA (GitIgnored)
│   ├── tenant_001/             # Customer A
│   │   ├── workspace/
│   │   ├── data/
│   │   └── config.json
│   ├── tenant_002/             # Customer B
│   │   └── ...
│   └── ...
│
└── docs/                        # DOCUMENTATION
    ├── setup.md
    ├── deployment.md
    ├── api.md
    └── pricing.md
```

### .gitignore (IMPORTANT!)
```gitignore
# NEVER commit customer data
customers/
.env
*.db
*.sqlite
logs/
__pycache__/
*.pyc
```

---

## 4. AGENT TYPES

### Agent 1: Sales Lead Score Agent

**Purpose:** Score and qualify sales leads automatically

**Customer Data Needed:**
- CRM exports (CSV)
- Lead information
- Historical conversion data
- Product pricing

**Agent Capabilities:**
```python
# agents/sales_agent/agent.py

class SalesLeadAgent:
    def __init__(self, tenant_id):
        self.tenant_id = tenant_id
        self.workspace = f"./customers/tenant_{tenant_id}/workspace"
    
    def score_lead(self, lead_data):
        """Score a lead from 0-100"""
        prompt = f"""
        Analyze this lead and score 0-100:
        - Budget: {lead_data.budget}
        - Timeline: {lead_data.timeline}
        - Need fit: {lead_data.need_fit}
        - Decision maker: {lead_data.decision_maker}
        
        Score based on historical conversion data.
        """
        return self.call_ai(prompt)
    
    def prioritize_leads(self, leads):
        """Rank leads by priority"""
        # Process all leads
        pass
    
    def generate_outreach(self, lead):
        """Generate personalized outreach email"""
        pass
```

**Telegram Commands:**
```
Score this lead: [lead data]
Prioritize my leads
Generate email for lead #123
Show hot leads (score > 80)
```

---

### Agent 2: HR Screening Agent

**Purpose:** Screen job applicants automatically

**Customer Data Needed:**
- Job descriptions
- Resume database
- Screening criteria
- Interview questions

**Agent Capabilities:**
```python
# agents/hr_agent/agent.py

class HRScreeningAgent:
    def screen_resume(self, resume, job_description):
        """Score resume match 0-100"""
        pass
    
    def generate_questions(self, candidate):
        """Generate interview questions"""
        pass
    
    def rank_candidates(self, candidates):
        """Rank all candidates"""
        pass
```

**Telegram Commands:**
```
Screen this resume: [upload PDF]
Generate questions for John Doe
Rank all applicants for Developer role
```

---

### Agent 3: Support Agent

**Purpose:** Handle customer support tickets

**Customer Data Needed:**
- Product documentation
- FAQ database
- Past tickets
- Customer info

**Telegram Commands:**
```
Create ticket: [issue]
Check ticket #123 status
Search knowledge base for [topic]
```

---

### Agent 4: Office Assistant Agent

**Purpose:** General office tasks (scheduling, notes, reminders)

**Telegram Commands:**
```
Schedule meeting for tomorrow 10am
Take notes: [meeting notes]
Remind me to send report on Friday
Summarize this document: [upload]
```

---

## 5. MULTI-TENANT DEPLOYMENT

### Option A: Single Server, Multiple Workspaces (Recommended for Start)

```
Your Server (1x VM, $20-50/month)
│
├── /opt/ai-platform/           # Platform code
├── /opt/customers/             # Customer data
│   ├── customer_001/           # Isolated workspace
│   │   ├── workspace/
│   │   ├── config.json         # Plan, limits
│   │   └── data/
│   ├── customer_002/
│   └── ...
└── /var/log/ai-platform/       # Logs
```

**Docker Compose:**
```yaml
# deployment/docker-compose.yml
version: '3.8'

services:
  platform:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./customers:/app/customers
      - ./platform_config.json:/app/config.json
    environment:
      - MASTER_API_KEY=${OPENROUTER_KEY}
      - DATABASE_URL=sqlite:///platform.db
    restart: unless-stopped

  dashboard:
    build: ./dashboard
    ports:
      - "3000:3000"
    depends_on:
      - platform
```

---

### Option B: Kubernetes (For Scale)

```yaml
# deployment/kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-platform
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: platform
        image: your-username/ai-agents:latest
        env:
        - name: TENANT_ISOLATION
          value: "namespace"
```

Each tenant gets isolated namespace.

---

### Option C: Serverless (Cheapest for Low Usage)

- Deploy on Railway, Render, or Fly.io
- Auto-scales with usage
- Pay per request

---

## 6. CUSTOMER DATA ISOLATION

### Workspace Structure

```
/customers/
├── tenant_001/
│   ├── config.json
│   │   {
│   │     "name": "Acme Corp",
│   │     "plan": "pro",
│   │     "monthly_token_limit": 100000,
│   │     "allowed_agents": ["sales", "support"],
│   │     "telegram_bot_token": "xxx"
│   │   }
│   ├── workspace/           # Agent working directory
│   ├── data/               # Uploaded files
│   │   ├── crm_exports/
│   │   ├── resumes/
│   │   └── documents/
│   └── memory.db           # Isolated memory
│
├── tenant_002/
│   └── ...
```

### Isolation Code

```python
# tenants/manager.py

class TenantManager:
    def __init__(self, tenant_id):
        self.tenant_id = tenant_id
        self.workspace = f"./customers/tenant_{tenant_id}/workspace"
        self.config = self.load_config()
    
    def load_config(self):
        with open(f"./customers/tenant_{tenant_id}/config.json") as f:
            return json.load(f)
    
    def check_usage_limit(self, tokens_used):
        if tokens_used >= self.config['monthly_token_limit']:
            raise Exception("Monthly limit reached. Upgrade plan.")
    
    def get_workspace_path(self):
        # Ensure tenant can't escape their workspace
        return os.path.abspath(self.workspace)
```

### Security Measures

```python
# Prevent directory traversal
def safe_path(tenant_id, requested_path):
    base = f"./customers/tenant_{tenant_id}/workspace"
    requested = os.path.abspath(os.path.join(base, requested_path))
    
    if not requested.startswith(base):
        raise SecurityError("Access denied: Outside workspace")
    
    return requested
```

---

## 7. AI USAGE CONTROL & PRICING

### Pricing Tiers

```python
# platform/billing.py

PLANS = {
    "free": {
        "monthly_tokens": 10000,
        "max_agents": 1,
        "max_workspace_mb": 100,
        "price_monthly": 0,
        "features": ["basic_agent"]
    },
    "starter": {
        "monthly_tokens": 100000,
        "max_agents": 3,
        "max_workspace_mb": 500,
        "price_monthly": 29,
        "features": ["sales_agent", "support_agent"]
    },
    "pro": {
        "monthly_tokens": 500000,
        "max_agents": 10,
        "max_workspace_mb": 5000,
        "price_monthly": 99,
        "features": ["all_agents", "priority_support"]
    },
    "enterprise": {
        "monthly_tokens": -1,  # Unlimited
        "max_agents": -1,
        "max_workspace_mb": 50000,
        "price_monthly": 499,
        "features": ["all", "custom_agents", "sla"]
    }
}
```

### Usage Tracking

```python
# monitoring/usage_tracker.py

class UsageTracker:
    def __init__(self, tenant_id):
        self.tenant_id = tenant_id
        self.db = sqlite3.connect('./usage.db')
    
    def record_usage(self, tokens, model, agent):
        self.db.execute("""
            INSERT INTO usage_log 
            (tenant_id, tokens, model, agent, timestamp)
            VALUES (?, ?, ?, ?, datetime('now'))
        """, (self.tenant_id, tokens, model, agent))
        self.db.commit()
    
    def get_monthly_usage(self):
        result = self.db.execute("""
            SELECT SUM(tokens) FROM usage_log 
            WHERE tenant_id = ? 
            AND strftime('%Y-%m', timestamp) = strftime('%Y-%m', 'now')
        """, (self.tenant_id,)).fetchone()
        return result[0] or 0
    
    def check_limit(self):
        plan = self.get_tenant_plan()
        limit = PLANS[plan]['monthly_tokens']
        used = self.get_monthly_usage()
        
        if limit > 0 and used >= limit:
            return False  # Limit exceeded
        return True
```

### Rate Limiting

```python
# platform/rate_limiter.py

class RateLimiter:
    def __init__(self):
        self.requests = {}  # tenant_id -> [timestamps]
    
    def check_rate_limit(self, tenant_id, max_per_minute=10):
        now = time.time()
        minute_ago = now - 60
        
        # Clean old requests
        self.requests[tenant_id] = [
            t for t in self.requests.get(tenant_id, [])
            if t > minute_ago
        ]
        
        if len(self.requests[tenant_id]) >= max_per_minute:
            return False  # Rate limited
        
        self.requests[tenant_id].append(now)
        return True
```

---

## 8. DEPLOYMENT OPTIONS

### Option 1: Your Own Server (Full Control)

**Best for:** Full control, higher margins

**Setup:**
```bash
# On Ubuntu VPS ($20-50/month)
git clone https://github.com/you/ai-agents-platform
cd ai-agents-platform
docker-compose up -d

# Add customer
python platform/cli.py tenant create --name "Acme Corp" --plan pro
```

**Customer Access:**
- Each customer gets unique Telegram bot OR
- Shared bot with tenant authentication

---

### Option 2: Platform-as-a-Service (Easiest)

**Best for:** Quick start, no server management

**Railway.app:**
```bash
railway init
railway up
```

**Render.com:**
- Push to GitHub
- Connect to Render
- Auto-deploys

**Fly.io:**
```bash
flyctl launch
flyctl deploy
```

---

### Option 3: Hybrid (Recommended)

- **Platform code:** Your server
- **AI processing:** OpenRouter (pay per use)
- **Customer bots:** Telegram (free)
- **Dashboard:** Vercel/Netlify (free tier)

---

### Customer Onboarding Flow

```
1. Customer signs up on dashboard
         │
2. Platform creates tenant workspace
         │
3. Customer gets:
   - Unique Telegram bot OR
   - Auth token for shared bot
   - Dashboard login
         │
4. Customer uploads data (CRM, docs, etc.)
         │
5. Agent starts working on customer data
         │
6. Usage tracked automatically
```

---

## 9. STEP-BY-STEP IMPLEMENTATION

### Phase 1: MVP (Week 1-2)

```bash
# 1. Set up repository
mkdir ai-agents-platform
cd ai-agents-platform
git init

# 2. Create basic structure
mkdir -p platform agents tenants deployment dashboard

# 3. Install dependencies
pip install fastapi uvicorn sqlite3 python-telegram-bot openai

# 4. Create tenant manager
# (See tenants/manager.py above)

# 5. Create sales agent
# (See agents/sales_agent/agent.py above)

# 6. Deploy locally
python platform/main.py

# 7. Test with 1 customer
```

### Phase 2: Multi-Tenant (Week 3-4)

```bash
# 1. Add authentication
# 2. Add usage tracking
# 3. Add rate limiting
# 4. Create dashboard
# 5. Deploy to VPS
```

### Phase 3: Scale (Month 2+)

```bash
# 1. Add more agents
# 2. Add billing integration (Stripe)
# 3. Add monitoring
# 4. Add customer support
# 5. Marketing & sales
```

---

## 10. COST & REVENUE MODEL

### Your Costs (Monthly)

| Item | Cost |
|------|------|
| VPS Server | $20-50 |
| OpenRouter API | Pay per use (~$0.01-0.10 per 1000 tokens) |
| Domain | $10/year |
| **Total Fixed** | **~$50/month** |

### Revenue Per Customer

| Plan | Price | Your Cost (AI) | Profit |
|------|-------|----------------|--------|
| Free | $0 | $0 | $0 |
| Starter | $29/mo | ~$5 | $24 |
| Pro | $99/mo | ~$20 | $79 |
| Enterprise | $499/mo | ~$100 | $399 |

### Break-Even

- **5 Starter customers** = $145 revenue - $50 cost = **$95 profit**
- **10 Pro customers** = $990 revenue - $200 cost = **$790 profit**

---

## QUICK START CHECKLIST

### Today
- [ ] Create GitHub repository
- [ ] Copy this strategy to docs/
- [ ] Set up basic folder structure

### Week 1
- [ ] Build tenant manager
- [ ] Build 1 agent (sales)
- [ ] Test with fake customer data

### Week 2
- [ ] Add Telegram integration
- [ ] Add usage tracking
- [ ] Deploy to VPS

### Week 3
- [ ] Onboard first beta customer (free)
- [ ] Get feedback
- [ ] Iterate

### Month 2
- [ ] Add billing (Stripe)
- [ ] Launch publicly
- [ ] Marketing

---

## CONTACT & SUPPORT

For questions about this strategy:
- Review each section carefully
- Start with MVP (Phase 1)
- Don't over-engineer initially
- Get customers early, iterate based on feedback

---

## KEY TAKEAWAYS

1. **Start Simple:** 1 agent, 1 customer, manual setup
2. **Isolate Data:** Each customer gets separate workspace
3. **Track Usage:** Token limits per plan
4. **Control Access:** Authentication per tenant
5. **Scale Gradually:** Add features as you grow
6. **Profit Margins:** AI cost is low, charge premium for value

---

**Good luck building your AI Agents Platform! 🚀**
