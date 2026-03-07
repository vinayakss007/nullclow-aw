FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    sqlite3 \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Install Nullclaw
RUN curl -L https://github.com/nullclaw/nullclaw/releases/latest/download/nullclaw-linux-x86_64.bin -o nullclaw \
    && chmod +x nullclaw \
    && mv nullclaw /usr/local/bin/ \
    && nullclaw version

# Copy requirements (if you have them)
COPY requirements.txt . 2>/dev/null || true
RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null || pip install --no-cache-dir flask python-telegram-bot

# Copy application code
COPY . .

# Create data directory for persistent storage
RUN mkdir -p /app/data /app/customers /app/logs

# Set permissions
RUN chmod +x quickstart.sh
RUN chmod 755 /app

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Volume for persistent data
VOLUME ["/app/data", "/app/customers"]

# Default command
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
