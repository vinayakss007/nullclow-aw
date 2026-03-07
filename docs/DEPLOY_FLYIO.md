# Fly.io Deployment Guide
## Deploy Multi-Agent Platform to Fly.io

---

## Quick Deploy (5 minutes)

### 1. Install Fly.io CLI

```bash
# macOS/Linux
curl -L https://fly.io/install.sh | sh

# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### 2. Login to Fly.io

```bash
flyctl auth login
```

### 3. Clone Your Repo

```bash
git clone https://github.com/coding4vinayak/nullclow-aw.git
cd nullclow-aw
```

### 4. Set Required Secrets

**REQUIRED - OpenRouter API Key:**
```bash
# Get your key from: https://openrouter.ai/keys
flyctl secrets set OPENROUTER_API_KEY=sk-or-v1-your-actual-key
```

**RECOMMENDED - Secret Key:**
```bash
# Generate random key
python3 -c "import secrets; print(secrets.token_hex(32))"

# Set it (replace with generated key)
flyctl secrets set SECRET_KEY=your-generated-key-here
```

**OPTIONAL - Admin Email:**
```bash
flyctl secrets set ADMIN_EMAIL=your-email@example.com
```

### 5. Deploy to Fly.io

```bash
# Initialize Fly.io app (if not done)
flyctl launch --no-deploy

# Deploy
flyctl deploy
```

### 6. Open Your App

```bash
# Open in browser
flyctl open

# Or get the URL
flyctl status
```

---

## Environment Variables Reference

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | `sk-or-v1-xxx` |

### Recommended Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Session security | Random 64-char string |
| `ADMIN_EMAIL` | Admin contact | `admin@example.com` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection | `sqlite:///app/data/platform.db` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `PORT` | App port | `5000` |

---

## Set/Update Secrets

### View Current Secrets

```bash
flyctl secrets list
```

### Add New Secret

```bash
flyctl secrets set KEY=value
```

### Update Secret

```bash
flyctl secrets set KEY=new-value
```

### Remove Secret

```bash
flyctl secrets unset KEY
```

### Set Multiple at Once

```bash
flyctl secrets set \
  OPENROUTER_API_KEY=sk-or-v1-xxx \
  SECRET_KEY=your-key \
  ADMIN_EMAIL=admin@example.com
```

---

## Testing Your Deployment

### 1. Check App Status

```bash
flyctl status
```

### 2. View Logs

```bash
# Real-time logs
flyctl logs

# Recent logs
flyctl logs --num 50
```

### 3. Test Health Endpoint

```bash
curl https://your-app.fly.dev/health
```

### 4. Test Platform

```bash
# SSH into the machine (advanced)
flyctl ssh console

# Test tenant manager
python3 tenant_manager.py list

# Test agent routing
python3 agents_platform.py route tenant_000 "Test task"
```

---

## Persistent Storage

Fly.io automatically creates a volume for your data based on `fly.toml`:

```toml
[[mounts]]
  source = "nullclow_data"
  destination = "/app/data"
  initial_size = "1gb"
```

This persists:
- Database (`platform.db`)
- Customer data (`customers/`)
- Logs

### Check Volume

```bash
flyctl volumes list
```

### Increase Volume Size

```bash
flyctl volumes update nullclow_data --size 5
```

---

## Scaling

### Change Machine Size

```bash
# More RAM/CPU
flyctl scale vm shared-cpu-2x

# Even more
flyctl scale vm performance-1x
```

### Add More Instances

```bash
flyctl scale count 2
```

---

## Custom Domain

### Add Custom Domain

```bash
flyctl certs add your-domain.com
```

### Update DNS

Point your domain to:
- **A record:** `fly.io` IP (provided in output)
- **CNAME:** `your-app.fly.dev`

---

## Troubleshooting

### App Won't Start

```bash
# Check logs
flyctl logs

# Check status
flyctl status

# Restart app
flyctl restart
```

### Database Errors

```bash
# SSH into machine
flyctl ssh console

# Check database
ls -la /app/data/
sqlite3 /app/data/platform.db ".tables"
```

### Out of Memory

```bash
# Increase memory
flyctl scale vm shared-cpu-2x --memory 1024
```

### High CPU Usage

```bash
# Check metrics
flyctl apps monitor nullclow-aw

# Scale up
flyctl scale count 2
```

---

## Costs

### Free Tier (What You Get)
- Up to 3 shared-cpu-1x VMs (256MB each)
- 3GB persistent volume
- 160GB outbound transfer/month
- **Enough for testing and small deployments**

### Paid (If You Exceed Free Tier)
- shared-cpu-1x: ~$2/month per VM
- Additional storage: $0.15/GB/month
- Additional transfer: $0.01/GB

### Estimate Your Costs

```bash
flyctl console --eval "pricing estimate"
```

---

## CI/CD with GitHub Actions

### Auto-Deploy on Push

Create `.github/workflows/deploy.yml`:

```yaml
name: Fly.io Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: superfly/flyctl-actions@v1
        with:
          args: "deploy"
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

### Add Fly.io API Token to GitHub

```bash
# Generate token
flyctl tokens create deploy

# Add to GitHub Secrets
# Go to: GitHub repo → Settings → Secrets → Actions
# Add: FLY_API_TOKEN = your-token
```

---

## Security Best Practices

### 1. Never Commit Secrets

```bash
# .gitignore should include
.env
*.key
secrets.json
```

### 2. Use Fly.io Secrets

```bash
# Good - secrets encrypted
flyctl secrets set OPENROUTER_API_KEY=xxx

# Bad - don't commit to git
echo "OPENROUTER_API_KEY=xxx" >> .env  # DON'T!
```

### 3. Enable HTTPS

Already enabled by default in `fly.toml`:
```toml
[http_service]
  force_https = true
```

### 4. Regular Backups

```bash
# SSH and backup
flyctl ssh console
tar -czf /tmp/backup.tar.gz /app/data
# Download backup
flyctl ssh sftp get /tmp/backup.tar.gz
```

---

## Next Steps After Deploy

1. **Test the platform:**
   ```bash
   flyctl ssh console
   python3 tenant_manager.py create "Test Corp" starter
   ```

2. **Add Telegram integration:**
   - Create bot via @BotFather
   - Add token to customer config

3. **Monitor usage:**
   ```bash
   flyctl logs
   ```

4. **Scale as needed:**
   ```bash
   flyctl scale count 2
   ```

---

## Support

- **Fly.io Docs:** https://fly.io/docs/
- **Fly.io Community:** https://community.fly.io/
- **GitHub Issues:** https://github.com/coding4vinayak/nullclow-aw/issues

---

**Deployed successfully? Open your app:**
```bash
flyctl open
```
