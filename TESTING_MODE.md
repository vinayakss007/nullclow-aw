# Testing Mode Configuration
## Unlimited Testing - All Limits Disabled

---

## ✅ Current Status: TESTING MODE ENABLED

All usage limits, token limits, and restrictions are **DISABLED** for unlimited testing.

---

## What's Unlimited:

### Token Usage
- ✅ **Unlimited tokens** - No monthly limits
- ✅ **All models** - Access to all AI models
- ✅ **All agents** - Use all 20 agents
- ✅ **All sub-agents** - Access to 80+ sub-agents

### Workspace
- ✅ **Unlimited storage** - No workspace size limits
- ✅ **Unlimited tenants** - Create as many as needed
- ✅ **Unlimited tasks** - No task execution limits

### Features
- ✅ **All agents enabled** - Free tier gets all agents
- ✅ **All tools enabled** - Browser, HTTP, file operations
- ✅ **No rate limiting** - Unlimited requests

---

## How to Enable/Disable Testing Mode

### In tenant_manager.py:
```python
# Line 14-15
TESTING_MODE = True   # Enable unlimited testing
TESTING_MODE = False  # Disable for production
```

### In usage_tracker.py:
```python
# Line 14-15
TESTING_MODE = True   # Enable unlimited testing
TESTING_MODE = False  # Disable for production
```

---

## Testing vs Production

| Feature | Testing Mode | Production Mode |
|---------|--------------|-----------------|
| Token Limits | Unlimited | Based on plan |
| Agent Access | All agents | Based on plan |
| Workspace Size | Unlimited | Based on plan |
| Rate Limiting | Disabled | Enabled |
| Alerts | Disabled | Enabled |
| Billing | $0 | Based on plan |

---

## Test Tenants Created

All tenants upgraded to **Enterprise (Unlimited)**:

```
tenant_000: Test Company    - Enterprise - Unlimited tokens
tenant_001: Acme Corp       - Enterprise - Unlimited tokens
tenant_002: Startup Inc     - Enterprise - Unlimited tokens
```

---

## What You Can Test

### ✅ Unlimited Agent Usage
```bash
# Use any agent, anytime
python3 agents_platform.py route tenant_000 "Score this lead"
python3 agents_platform.py route tenant_000 "Screen resume"
python3 agents_platform.py route tenant_000 "Search for news"
# No limits!
```

### ✅ Unlimited Token Consumption
```bash
# Record as many tokens as needed
python3 usage_tracker.py record tenant_000 1000000 "test-model" "test-agent"
# No alerts, no limits!
```

### ✅ Create Unlimited Tenants
```bash
# Create as many tenants as you want
python3 tenant_manager.py create "Company 1" free
python3 tenant_manager.py create "Company 2" free
python3 tenant_manager.py create "Company 3" free
# All get unlimited access!
```

---

## Switching to Production

When ready for production:

### 1. Update tenant_manager.py
```python
TESTING_MODE = False  # Change to False
```

### 2. Update usage_tracker.py
```python
TESTING_MODE = False  # Change to False
```

### 3. Set proper plans for tenants
```bash
python3 tenant_manager.py update tenant_000 plan starter
python3 tenant_manager.py update tenant_001 plan pro
```

### 4. Enable alerts
```bash
# Alerts will automatically activate when TESTING_MODE = False
```

---

## Monitoring During Testing

Even with unlimited mode, you can still track usage:

```bash
# View usage reports
python3 usage_tracker.py report tenant_000

# Check monthly usage (for reference)
python3 usage_tracker.py monthly tenant_000

# View all tenant usage
python3 usage_tracker.py report
```

---

## Important Notes

### ⚠️ API Costs Still Apply
- Testing mode removes **platform limits**
- OpenRouter API still charges for token usage
- Monitor your OpenRouter dashboard: https://openrouter.ai/activity

### ⚠️ Before Production
- Set `TESTING_MODE = False`
- Configure proper pricing plans
- Enable usage alerts
- Set up billing (Stripe)

### ✅ Safe for Testing
- No accidental charges from platform
- No unexpected limits during demos
- No restrictions on feature testing

---

## Recommended Testing Workflow

### Phase 1: Unlimited Testing (Now)
```
✅ TESTING_MODE = True
✅ Test all features
✅ Create multiple tenants
✅ Use all agents freely
```

### Phase 2: Simulate Production
```
⏭️ TESTING_MODE = False
⏭️ Set up pricing plans
⏭️ Test limit enforcement
⏭️ Test billing integration
```

### Phase 3: Live Deployment
```
⏭️ Deploy to Fly.io/Oracle Cloud
⏭️ Add real customers
⏭️ Monitor actual usage
⏭️ Collect payments
```

---

## Quick Commands for Testing

```bash
# Create unlimited tenant
python3 tenant_manager.py create "Test Corp" enterprise

# Route unlimited tasks
python3 agents_platform.py route tenant_000 "Task 1"
python3 agents_platform.py route tenant_000 "Task 2"
python3 agents_platform.py route tenant_000 "Task 3"

# Record unlimited usage
python3 usage_tracker.py record tenant_000 999999 "unlimited" "test"

# Check status (no alerts!)
python3 usage_tracker.py alerts
```

---

## Status

**Current Mode:** ✅ TESTING MODE (Unlimited)
**Production Ready:** ⏭️ Set TESTING_MODE = False when ready
**API Costs:** ⚠️ Still apply (OpenRouter charges)

---

**Test freely! No limits enforced.** 🚀
