# Deployment Guide
## Production Deployment for Multi-Agent Platform

---

## Table of Contents

1. [Deployment Options](#deployment-options)
2. [Single Server Deployment](#single-server-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Cloud Platform Deployment](#cloud-platform-deployment)
6. [Security Hardening](#security-hardening)
7. [Monitoring & Logging](#monitoring--logging)
8. [Backup & Recovery](#backup--recovery)
9. [Scaling Strategy](#scaling-strategy)

---

## Deployment Options

### Option Comparison

| Option | Cost | Complexity | Best For |
|--------|------|------------|----------|
| Single Server | $ | Low | MVP, < 100 customers |
| Docker | $$ | Medium | 100-1000 customers |
| Kubernetes | $$$$ | High | Enterprise, 1000+ customers |
| Cloud PaaS | $$ | Low | Quick start, auto-scale |

---

## Single Server Deployment

### Prerequisites

- Ubuntu 22.04 LTS server
- 2 CPU, 4GB RAM minimum
- 50GB SSD storage
- Root access

### Step 1: Server Setup

```bash
# Update system
apt update && apt upgrade -y

# Install dependencies
apt install -y python3 python3-pip git curl wget nginx sqlite3

# Install Nullclaw
curl -L https://github.com/nullclaw/nullclaw/releases/latest/download/nullclaw-linux-x86_64.bin -o nullclaw
chmod +x nullclaw
sudo mv nullclaw /usr/local/bin/

# Verify
nullclaw version
```

### Step 2: Clone Platform

```bash
# Create app user
useradd -m -s /bin/bash aiplatform
su - aiplatform

# Clone repository
git clone https://github.com/coding4vinayak/nullclow-aw.git
cd nullclow-aw

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Configure Environment

```bash
# Create .env file
cat > .env << EOF
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY
DATABASE_URL=sqlite:///platform.db
ADMIN_EMAIL=admin@example.com
SECRET_KEY=your-secret-key-here
EOF

# Set permissions
chmod 600 .env
```

### Step 4: Create Systemd Service

```bash
sudo nano /etc/systemd/system/ai-platform.service
```

**Service File:**
```ini
[Unit]
Description=AI Agents Platform
After=network.target

[Service]
Type=simple
User=aiplatform
WorkingDirectory=/home/aiplatform/nullclow-aw
Environment="PATH=/home/aiplatform/nullclow-aw/venv/bin"
ExecStart=/home/aiplatform/nullclow-aw/venv/bin/python3 -m flask run --host 127.0.0.1 --port 5000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable Service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-platform
sudo systemctl start ai-platform
sudo systemctl status ai-platform
```

### Step 5: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/ai-platform
```

**Nginx Config:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/aiplatform/nullclow-aw/static;
        expires 30d;
    }
}
```

**Enable Site:**
```bash
sudo ln -s /etc/nginx/sites-available/ai-platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: SSL Certificate (Let's Encrypt)

```bash
apt install -y certbot python3-certbot-nginx

certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

---

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Install Nullclaw
RUN curl -L https://github.com/nullclaw/nullclaw/releases/latest/download/nullclaw-linux-x86_64.bin -o nullclaw \
    && chmod +x nullclaw \
    && mv nullclaw /usr/local/bin/

# Copy application
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create volumes
VOLUME ["/app/customers", "/app/data"]

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./customers:/app/customers
      - ./data:/app/data
      - ./nullclaw_config:/root/.nullclaw
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - DATABASE_URL=sqlite:///app/data/platform.db
      - SECRET_KEY=${SECRET_KEY}
    restart: unless-stopped
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    restart: unless-stopped

volumes:
  redis_data:
```

### Deploy with Docker

```bash
# Build
docker-compose build

# Start
docker-compose up -d

# Check logs
docker-compose logs -f app

# Stop
docker-compose down
```

---

## Kubernetes Deployment

### Deployment YAML

```yaml
# deployment/kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-platform
  labels:
    app: ai-platform
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-platform
  template:
    metadata:
      labels:
        app: ai-platform
    spec:
      containers:
      - name: app
        image: your-registry/ai-platform:latest
        ports:
        - containerPort: 5000
        env:
        - name: OPENROUTER_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: openrouter-key
        - name: DATABASE_URL
          value: "postgresql://user:pass@db-service:5432/aiplatform"
        volumeMounts:
        - name: customers-data
          mountPath: /app/customers
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: customers-data
        persistentVolumeClaim:
          claimName: customers-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: ai-platform-service
spec:
  selector:
    app: ai-platform
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
```

### Apply to Cluster

```bash
# Create secrets
kubectl create secret generic api-secrets \
  --from-literal=openrouter-key=sk-or-v1-YOUR_KEY

# Apply deployment
kubectl apply -f deployment/kubernetes/

# Check status
kubectl get pods
kubectl get services
```

---

## Cloud Platform Deployment

### Railway.app

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize
railway init

# Deploy
railway up
```

**railway.json:**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python3 -m flask run --host 0.0.0.0",
    "healthcheckPath": "/health",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

---

### Render.com

1. Push code to GitHub
2. Go to render.com → New Web Service
3. Connect repository
4. Configure:
   - Build: `pip install -r requirements.txt`
   - Start: `python3 -m flask run --host 0.0.0.0`
5. Add environment variables
6. Deploy

---

### Fly.io

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Launch
flyctl launch

# Deploy
flyctl deploy
```

**fly.toml:**
```toml
app = "ai-platform"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "5000"

[[services]]
  http_checks = []
  internal_port = 5000
  protocol = "tcp"

  [[services.ports]]
    port = 80
    handlers = ["http"]

  [[services.ports]]
    port = 443
    handlers = ["tls"]
```

---

## Security Hardening

### Firewall Configuration

```bash
# Install UFW
apt install -y ufw

# Configure
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow http
ufw allow https
ufw enable
```

### Fail2Ban

```bash
apt install -y fail2ban

# Create jail
nano /etc/fail2ban/jail.local
```

** Jail Config:**
```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true

[nginx-http-auth]
enabled = true
```

### Database Security

```bash
# Set secure permissions
chmod 600 platform.db
chown aiplatform:aiplatform platform.db
```

### API Key Encryption

```python
# Use environment variables
import os
API_KEY = os.environ.get('OPENROUTER_API_KEY')

# Or use secrets manager
from cryptography.fernet import Fernet
```

---

## Monitoring & Logging

### Application Logs

```bash
# Create log directory
mkdir -p /var/log/ai-platform

# Configure logging in app
import logging
logging.basicConfig(
    filename='/var/log/ai-platform/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Log Rotation

```bash
nano /etc/logrotate.d/ai-platform
```

**Config:**
```
/var/log/ai-platform/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 aiplatform aiplatform
    sharedscripts
}
```

### Monitoring with Prometheus

```yaml
# docker-compose monitoring
prometheus:
  image: prom/prometheus
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
  ports:
    - "9090:9090"

grafana:
  image: grafana/grafana
  ports:
    - "3000:3000"
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=admin
```

---

## Backup & Recovery

### Automated Backups

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/ai-platform/$DATE"

mkdir -p $BACKUP_DIR

# Backup database
cp /app/data/platform.db $BACKUP_DIR/

# Backup customer data
tar -czf $BACKUP_DIR/customers.tar.gz /app/customers/

# Backup configs
cp /app/.env $BACKUP_DIR/

# Upload to S3 (optional)
aws s3 cp $BACKUP_DIR s3://your-bucket/backups/$DATE/

# Keep only last 7 days
find /backups/ai-platform -type d -mtime +7 -exec rm -rf {} \;
```

**Cron Job:**
```bash
# Run daily at 2 AM
0 2 * * * /app/backup.sh
```

### Recovery Procedure

```bash
# Stop services
systemctl stop ai-platform

# Restore from backup
cp /backups/ai-platform/20260307_020000/platform.db /app/data/
tar -xzf /backups/ai-platform/20260307_020000/customers.tar.gz -C /app/

# Start services
systemctl start ai-platform
```

---

## Scaling Strategy

### Horizontal Scaling

```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ai-platform-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ai-platform
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Database Scaling

- **Read Replicas:** For read-heavy workloads
- **Connection Pooling:** Use PgBouncer for PostgreSQL
- **Sharding:** By tenant_id for multi-tenant

### Caching Strategy

```python
# Redis caching
import redis
cache = redis.Redis(host='localhost', port=6379)

# Cache tenant config
def get_tenant_config(tenant_id):
    cached = cache.get(f"tenant:{tenant_id}")
    if cached:
        return json.loads(cached)
    
    config = db.get_tenant(tenant_id)
    cache.setex(f"tenant:{tenant_id}", 300, json.dumps(config))
    return config
```

---

## Performance Optimization

### Database Indexing

```sql
CREATE INDEX idx_tenant_id ON token_usage(tenant_id);
CREATE INDEX idx_timestamp ON token_usage(timestamp);
CREATE INDEX idx_agent_type ON token_usage(agent_type);
```

### Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'sqlite:///platform.db',
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40
)
```

### Async Processing

```python
# Use Celery for background tasks
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def process_agent_task(tenant_id, task_data):
    # Long-running task
    pass
```

---

## Troubleshooting

### Common Issues

**High Memory Usage:**
```bash
# Check processes
ps aux --sort=-%mem | head

# Restart services
systemctl restart ai-platform
```

**Database Lock:**
```bash
# Check locks
sqlite3 platform.db "PRAGMA locking_mode;"

# Vacuum database
sqlite3 platform.db "VACUUM;"
```

**Slow Responses:**
```bash
# Check logs
tail -f /var/log/ai-platform/app.log

# Profile application
python3 -m cProfile -o profile.stats app.py
```

---

## Support

For deployment issues:
- GitHub Issues: https://github.com/coding4vinayak/nullclow-aw/issues
- Documentation: https://github.com/coding4vinayak/nullclow-aw/docs
