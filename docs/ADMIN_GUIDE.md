# Admin Control Panel Guide
## Complete Admin Controls for Multi-Agent Platform

---

## Quick Start

```bash
# Start admin panel
python3 admin_panel.py

# Or use direct commands
python3 admin_panel.py list
python3 admin_panel.py report
```

---

## Admin Commands

### Tenant Management

#### List All Tenants
```bash
python3 admin_panel.py list
```

**Output:**
```
📁 tenant_000: Test Company
   Plan: starter
   Email: test@example.com
   Status: active
   Usage: 1,500 / ∞ tokens
   Telegram: ✅
```

---

#### Suspend Tenant
```bash
python3 admin_panel.py suspend tenant_000 "Payment overdue"
```

**Interactive:**
```
admin> suspend tenant_000 Payment overdue
✅ Suspended tenant: tenant_000
   Reason: Payment overdue
```

---

#### Activate Tenant
```bash
python3 admin_panel.py activate tenant_000
```

---

#### Upgrade Plan
```bash
python3 admin_panel.py upgrade tenant_000 pro
```

---

#### Delete Tenant
```bash
# Soft delete (keeps data)
python3 admin_panel.py delete tenant_000

# Hard delete (permanent)
# Use interactive mode
admin> delete tenant_000 --hard
```

---

### Usage Control

#### Set Custom Limit
```bash
python3 admin_panel.py set-limit tenant_000 500000
```

**Interactive:**
```
admin> set-limit tenant_000 500000
✅ Set custom limit for tenant_000: 500,000 tokens
```

---

#### Add Bonus Tokens
```bash
python3 admin_panel.py add-bonus tenant_000 100000
```

---

#### Reset Usage
```bash
# Interactive only
admin> reset-usage tenant_000
✅ Reset usage for tenant_000
```

---

### System Control

#### Platform Report
```bash
python3 admin_panel.py report
```

**Output:**
```
================================================================================
PLATFORM REPORT
Generated: 2026-03-07 15:30:00
================================================================================

📊 TENANTS
   Total: 6
   Active: 6
   Suspended: 0

📈 PLANS
   Free: 2
   Starter: 2
   Pro: 2

💰 USAGE
   Total Tokens (this month): 2,668,164
   Average per Tenant: 444,694

⚙️  SYSTEM
   Testing Mode: ✅ ON
   Maintenance Mode: ❌ OFF
```

---

#### Top Users
```bash
python3 admin_panel.py top-users
python3 admin_panel.py top-users 5  # Top 5 only
```

---

#### Toggle Testing Mode
```bash
# Interactive only
admin> testing on
admin> testing off
```

---

#### Maintenance Mode
```bash
# Interactive only
admin> maintenance on
⚠️  MAINTENANCE MODE ENABLED

admin> maintenance off
✅ MAINTENANCE MODE DISABLED
```

---

### Billing

#### Generate Invoice
```bash
python3 admin_panel.py invoice tenant_000
```

**Output:**
```
================================================================================
INVOICE
================================================================================

Tenant: Test Company (tenant_000)
Period: 2026-03
Plan: starter - $29.00
Usage: 1,500 / ∞ tokens

TOTAL: $29.00
```

---

## Interactive Mode

### Start Interactive Session
```bash
python3 admin_panel.py
```

### Available Commands

```
📁 Tenant Management
   list - List all tenants
   suspend <id> [reason] - Suspend tenant
   activate <id> - Activate tenant
   delete <id> [--hard] - Delete tenant
   upgrade <id> <plan> - Upgrade plan
   reset-usage <id> - Reset monthly usage

📁 Usage Control
   set-limit <id> <limit> - Set custom limit
   add-bonus <id> <amount> - Add bonus tokens

📁 System Control
   maintenance on|off - Toggle maintenance mode
   testing on|off - Toggle testing mode
   report - Platform report
   top-users [n] - Top users by usage

📁 Billing
   invoice <id> - Generate invoice

📁 Help
   help - Show this help
   exit - Exit admin panel
```

---

## Example Admin Session

```bash
$ python3 admin_panel.py

🎛️  ADMIN CONTROL PANEL
Type 'help' for commands

admin> list

================================================================================
ADMIN: ALL TENANTS (6)
================================================================================

📁 tenant_000: Test Company
   Plan: starter
   Email: test@example.com
   Status: active
   Usage: 1,500 / ∞ tokens
   Created: 2026-03-07 14:00:00
   Telegram: ✅

📁 tenant_001: Acme Corp
   Plan: pro
   Email: acme@example.com
   Status: active
   Usage: 888,888 / ∞ tokens
   Created: 2026-03-07 14:10:00
   Telegram: ✅

admin> report

================================================================================
PLATFORM REPORT
Generated: 2026-03-07 15:30:00
================================================================================

📊 TENANTS
   Total: 6
   Active: 6
   Suspended: 0

📈 PLANS
   Free: 2
   Starter: 2
   Pro: 2

💰 USAGE
   Total Tokens (this month): 2,668,164

admin> top-users 3

================================================================================
TOP 3 USERS BY TOKEN USAGE
================================================================================

 1. tenant_000: Test Company
    Plan: starter | Usage: 1,001,499 tokens

 2. tenant_001: Acme Corp
    Plan: pro | Usage: 888,888 tokens

 3. tenant_002: Startup Inc
    Plan: free | Usage: 777,777 tokens

admin> upgrade tenant_002 pro
✅ Upgraded tenant_002 to pro plan

admin> invoice tenant_002

================================================================================
INVOICE
================================================================================

Tenant: Startup Inc (tenant_002)
Period: 2026-03
Plan: pro - $99.00
Usage: 777,777 / ∞ tokens

TOTAL: $99.00

admin> exit
Exiting admin panel...
```

---

## Admin Permissions

### What Admin Can Do:

✅ **Tenant Management**
- View all tenants
- Suspend/activate tenants
- Upgrade/downgrade plans
- Delete tenants
- Reset usage

✅ **Usage Control**
- Set custom limits
- Add bonus tokens
- View detailed usage
- Generate reports

✅ **System Control**
- Toggle maintenance mode
- Toggle testing mode
- View platform stats

✅ **Billing**
- Generate invoices
- View payment status
- Track overages

---

## Admin Configuration

### Config File: `admin_config.json`

```json
{
  "admin_email": "admin@example.com",
  "platform_name": "Multi-Agent Platform",
  "testing_mode": true,
  "maintenance_mode": false,
  "max_tenants_per_account": 10,
  "auto_approve_tenants": true
}
```

### Modify Config:
```bash
# Edit manually
nano admin_config.json

# Or via panel
admin> testing off
admin> maintenance on
```

---

## Security

### Best Practices:

1. **Protect Admin Access**
   ```bash
   # Don't commit admin credentials
   echo "admin_config.json" >> .gitignore
   ```

2. **Use Strong Passwords** (when implemented)
   ```bash
   # Future: Add password protection
   python3 admin_panel.py --auth
   ```

3. **Audit Logs** (when implemented)
   ```bash
   # View admin actions
   cat logs/admin_actions.log
   ```

4. **Regular Backups**
   ```bash
   # Backup admin config
   cp admin_config.json backups/
   ```

---

## Monitoring

### Daily Admin Tasks:

1. **Check Platform Health**
   ```bash
   admin> report
   ```

2. **Review Top Users**
   ```bash
   admin> top-users 10
   ```

3. **Check for Issues**
   ```bash
   admin> list
   # Look for suspended tenants, high usage, etc.
   ```

4. **Generate Invoices**
   ```bash
   admin> invoice tenant_000
   ```

---

## Troubleshooting

### Tenant Can't Access
```bash
# Check status
admin> list

# If suspended
admin> activate tenant_000
```

### Usage Limit Issues
```bash
# Check usage
admin> report

# Reset if needed
admin> reset-usage tenant_000

# Add bonus if needed
admin> add-bonus tenant_000 50000
```

### System Issues
```bash
# Enable maintenance mode
admin> maintenance on

# Fix issues...

# Disable maintenance
admin> maintenance off
```

---

## API Access (Future)

### REST API Endpoints (Planned):

```
GET    /admin/tenants          # List tenants
POST   /admin/tenants/{id}/suspend    # Suspend tenant
POST   /admin/tenants/{id}/activate   # Activate tenant
PUT    /admin/tenants/{id}/plan      # Update plan
GET    /admin/report           # Platform report
POST   /admin/invoice/{id}     # Generate invoice
```

---

## Support

For admin issues:
- Check logs: `logs/admin_actions.log`
- Review config: `admin_config.json`
- GitHub Issues: https://github.com/coding4vinayak/nullclow-aw/issues

---

**Admin Panel Ready! Start with:** `python3 admin_panel.py` 🎛️
