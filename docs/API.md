# API Documentation
## Multi-Agent Platform API Reference

---

## Overview

This document describes the programmatic interfaces for the Multi-Agent Platform.

---

## Table of Contents

1. [Tenant Manager API](#tenant-manager-api)
2. [Agent Platform API](#agent-platform-api)
3. [Usage Tracker API](#usage-tracker-api)
4. [Integration API](#integration-api)
5. [Error Codes](#error-codes)

---

## Tenant Manager API

### Create Tenant

```python
from tenant_manager import TenantManager

manager = TenantManager()

tenant_id = manager.create_tenant(
    name="Acme Corp",
    plan="starter",           # free, starter, pro, enterprise
    email="contact@acme.com",
    telegram_bot_token="123456:ABC-DEF"
)

print(f"Created: {tenant_id}")
```

**Returns:** `tenant_id` (string)

---

### Get Tenant

```python
tenant = manager.get_tenant("tenant_001")

print(tenant['name'])
print(tenant['plan'])
print(tenant['usage']['tokens_used_this_month'])
```

**Returns:** `dict` or `None`

---

### List Tenants

```python
tenants = manager.list_tenants(status="active")

for tenant in tenants:
    print(f"{tenant['tenant_id']}: {tenant['name']}")
```

**Returns:** `list` of tenant dicts

---

### Update Tenant

```python
manager.update_tenant("tenant_001", {
    "plan": "pro",
    "email": "new@email.com"
})
```

**Returns:** `None`

---

### Delete Tenant

```python
# Soft delete (mark inactive)
manager.delete_tenant("tenant_001")

# Hard delete (permanent)
manager.hard_delete_tenant("tenant_001")
```

---

### Check Usage Limit

```python
can_use = manager.check_usage_limit("tenant_001", tokens_requested=5000)

if can_use:
    # Proceed with task
    pass
else:
    # Reject - limit exceeded
    print("Monthly limit reached")
```

**Returns:** `bool`

---

### Record Usage

```python
manager.record_usage(
    tenant_id="tenant_001",
    tokens=1500,
    agent="sales_agent"
)
```

---

## Agent Platform API

### Initialize Router

```python
from agents_platform import AgentRouter, TaskManager

task_manager = TaskManager()
router = AgentRouter(task_manager)
```

---

### Route Task

```python
result = router.route_task(
    task_description="Score this sales lead: Budget $50k",
    tenant_id="tenant_001",
    input_data="{'budget': 50000, 'timeline': '2 weeks'}"
)

print(f"Agent: {result['agent_type']}")
print(f"Sub-Agent: {result['sub_agent']}")
print(f"Task ID: {result['task_id']}")
```

**Returns:** `dict` with routing information

---

### Create Task

```python
task_id = task_manager.create_task(
    tenant_id="tenant_001",
    agent_type="sales",
    sub_agent="lead_scorer",
    task_description="Score this lead",
    input_data="Budget: $50k, Timeline: 2 weeks"
)
```

**Returns:** `task_id` (int)

---

### Assign Task

```python
task_manager.assign_task(
    task_id=123,
    agent_type="sales",
    sub_agent="lead_scorer"
)
```

---

### Complete Task

```python
task_manager.complete_task(
    task_id=123,
    output_data="Score: 85/100 - High quality lead"
)
```

---

### Get Pending Tasks

```python
tasks = task_manager.get_pending_tasks(tenant_id="tenant_001")

for task in tasks:
    print(f"Task {task['id']}: {task['task_description']}")
```

---

### Get Agent Tasks

```python
sales_tasks = task_manager.get_agent_tasks(
    agent_type="sales",
    status="pending"
)
```

---

## Usage Tracker API

### Initialize Tracker

```python
from usage_tracker import UsageTracker

tracker = UsageTracker()
```

---

### Record Token Usage

```python
tracker.record_token_usage(
    tenant_id="tenant_001",
    tokens=1500,
    model="llama-3.3-70b",
    agent_type="sales",
    sub_agent="lead_scorer",
    task_id=123,
    cost_usd=0.0015
)
```

---

### Get Token Usage

```python
# Last 30 days
usage = tracker.get_token_usage("tenant_001", days=30)
print(f"Used: {usage:,} tokens")

# This month
monthly = tracker.get_monthly_usage("tenant_001")
print(f"Monthly: {monthly:,} tokens")
```

---

### Get Usage by Agent

```python
by_agent = tracker.get_usage_by_agent("tenant_001", days=7)

for agent, tokens in by_agent.items():
    print(f"{agent}: {tokens:,} tokens")
```

---

### Get Usage by Model

```python
by_model = tracker.get_usage_by_model("tenant_001", days=7)

for model, tokens in by_model.items():
    print(f"{model}: {tokens:,} tokens")
```

---

### Get Cost

```python
cost = tracker.get_cost("tenant_001", days=30)
print(f"Total cost: ${cost:.2f}")
```

---

### Log Task

```python
tracker.log_task(
    tenant_id="tenant_001",
    agent_type="sales",
    sub_agent="lead_scorer",
    task_description="Score lead #123",
    execution_time_ms=1500,
    status="completed"
)
```

---

### Get Task History

```python
history = tracker.get_task_history("tenant_001", limit=50)

for task in history:
    print(f"{task['timestamp']}: {task['task_description']}")
```

---

### Get Daily Summary

```python
daily = tracker.get_daily_summary("tenant_001", days=30)

for day in daily:
    print(f"{day['date']}: {day['total_tokens']} tokens")
```

---

### Get Alerts

```python
alerts = tracker.get_alerts(tenant_id="tenant_001", unresolved_only=True)

for alert in alerts:
    print(f"⚠️ {alert['message']}")
```

---

### Resolve Alert

```python
tracker.resolve_alert(alert_id=5)
```

---

### Generate Report

```python
report = tracker.generate_report("tenant_001")

print(f"Total Tokens: {report['total_tokens']}")
print(f"Total Tasks: {report['total_tasks']}")
print(f"Total Cost: ${report['total_cost']:.2f}")
print(f"Usage by Agent: {report['usage_by_agent']}")
```

---

## Integration API

### Nullclaw Integration

```python
from nullclaw_integration import NullclawIntegration

integration = NullclawIntegration(tenant_id="tenant_001")

# Send message to Nullclaw
response = integration.send_to_nullclaw("Search for AI news")
print(response)

# Route task
routing = integration.route_task("Score this sales lead")
print(routing)

# Execute specific agent task
result = integration.execute_agent_task(
    agent_type="sales",
    sub_agent="lead_scorer",
    task="Score this lead",
    input_data="Budget: $50k"
)

# Track usage
integration.track_usage(
    tokens_used=1500,
    agent_type="sales",
    sub_agent="lead_scorer"
)

# Check limits
if integration.check_limits():
    print("Within limits")
else:
    print("Limit exceeded")
```

---

## Error Codes

| Code | Message | Solution |
|------|---------|----------|
| `TENANT_NOT_FOUND` | Tenant does not exist | Create tenant first |
| `LIMIT_EXCEEDED` | Monthly token limit reached | Upgrade plan |
| `AGENT_NOT_FOUND` | Agent type not available | Check agent name |
| `SUB_AGENT_NOT_FOUND` | Sub-agent not found | Check sub-agent name |
| `TASK_NOT_FOUND` | Task ID does not exist | Check task ID |
| `INVALID_PLAN` | Plan name not valid | Use: free, starter, pro, enterprise |
| `WORKSPACE_NOT_FOUND` | Tenant workspace missing | Recreate tenant |
| `API_KEY_MISSING` | OpenRouter API key not set | Add to config |
| `TIMEOUT` | Task execution timeout | Retry or simplify task |

---

## Rate Limits

| Plan | Requests/Minute | Tasks/Hour |
|------|-----------------|------------|
| Free | 5 | 20 |
| Starter | 20 | 100 |
| Pro | 100 | 500 |
| Enterprise | 500 | Unlimited |

---

## Best Practices

### 1. Always Check Limits

```python
if not manager.check_usage_limit(tenant_id, tokens_needed):
    raise Exception("Monthly limit exceeded")
```

### 2. Track All Usage

```python
# Record before and after task
tracker.record_token_usage(tenant_id, tokens, model, agent)
```

### 3. Handle Errors Gracefully

```python
try:
    result = router.route_task(task, tenant_id)
except Exception as e:
    log_error(e)
    return "Sorry, I encountered an error. Please try again."
```

### 4. Set Up Alerts

```python
alerts = tracker.get_alerts(tenant_id)
if alerts:
    notify_admin(tenant_id, alerts)
```

### 5. Clean Up Old Data

```python
# Run monthly
manager.reset_monthly_usage()
```

---

## Example: Complete Workflow

```python
from tenant_manager import TenantManager
from agents_platform import AgentRouter, TaskManager
from usage_tracker import UsageTracker
from nullclaw_integration import NullclawIntegration

# Initialize
manager = TenantManager()
task_manager = TaskManager()
router = AgentRouter(task_manager)
tracker = UsageTracker()
integration = NullclawIntegration("tenant_001")

# 1. Create tenant
tenant_id = manager.create_tenant("Acme Corp", "starter")

# 2. Route task
routing = router.route_task(
    "Score this sales lead: Budget $50k",
    tenant_id
)

# 3. Execute via Nullclaw
response = integration.send_to_nullclaw("Score this lead: Budget $50k")

# 4. Track usage
tracker.record_token_usage(
    tenant_id=tenant_id,
    tokens=1500,
    model="llama-3.3",
    agent_type="sales",
    sub_agent="lead_scorer"
)

# 5. Complete task
task_manager.complete_task(routing['task_id'], response)

# 6. Generate report
report = tracker.generate_report(tenant_id)
print(f"Task completed. Total cost: ${report['total_cost']:.2f}")
```

---

## Support

For API issues or questions:
- GitHub Issues: https://github.com/coding4vinayak/nullclow-aw/issues
- Email: support@example.com
