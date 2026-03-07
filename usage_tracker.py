#!/usr/bin/env python3
"""
Usage Tracker - Track AI token usage per tenant
Monitor costs, enforce limits, generate reports
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

class UsageTracker:
    def __init__(self, db_path="./usage.db"):
        self.db = sqlite3.connect(db_path)
        self._create_tables()
    
    def _create_tables(self):
        """Create database tables"""
        # Token usage log
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS token_usage (
                id INTEGER PRIMARY KEY,
                tenant_id TEXT NOT NULL,
                tokens INTEGER NOT NULL,
                model TEXT,
                agent_type TEXT,
                sub_agent TEXT,
                task_id INTEGER,
                cost_usd REAL DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Task execution log
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS task_log (
                id INTEGER PRIMARY KEY,
                tenant_id TEXT NOT NULL,
                agent_type TEXT,
                sub_agent TEXT,
                task_description TEXT,
                status TEXT DEFAULT 'completed',
                execution_time_ms INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # API calls log
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS api_calls (
                id INTEGER PRIMARY KEY,
                tenant_id TEXT NOT NULL,
                endpoint TEXT,
                method TEXT,
                response_time_ms INTEGER,
                status_code INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Daily usage summary
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS daily_summary (
                id INTEGER PRIMARY KEY,
                tenant_id TEXT NOT NULL,
                date DATE NOT NULL,
                total_tokens INTEGER,
                total_tasks INTEGER,
                total_api_calls INTEGER,
                total_cost_usd REAL,
                UNIQUE(tenant_id, date)
            )
        """)
        
        # Alerts
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY,
                tenant_id TEXT NOT NULL,
                alert_type TEXT,
                message TEXT,
                threshold_percent REAL,
                is_resolved BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                resolved_at DATETIME
            )
        """)
        
        self.db.commit()
    
    # ==================== TOKEN USAGE ====================
    
    def record_token_usage(self, tenant_id: str, tokens: int, 
                          model: str = None, agent_type: str = None,
                          sub_agent: str = None, task_id: int = None,
                          cost_usd: float = 0):
        """Record token usage"""
        self.db.execute("""
            INSERT INTO token_usage 
            (tenant_id, tokens, model, agent_type, sub_agent, task_id, cost_usd)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (tenant_id, tokens, model, agent_type, sub_agent, task_id, cost_usd))
        self.db.commit()
        
        # Update daily summary
        self._update_daily_summary(tenant_id, tokens, cost_usd)
        
        # Check for alerts
        self._check_usage_alerts(tenant_id)
    
    def get_token_usage(self, tenant_id: str, days: int = 30) -> int:
        """Get total tokens used in last N days"""
        cutoff = datetime.now() - timedelta(days=days)
        
        result = self.db.execute("""
            SELECT SUM(tokens) FROM token_usage
            WHERE tenant_id = ? AND timestamp >= ?
        """, (tenant_id, cutoff.isoformat())).fetchone()
        
        return result[0] or 0
    
    def get_monthly_usage(self, tenant_id: str) -> int:
        """Get tokens used this month"""
        now = datetime.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        result = self.db.execute("""
            SELECT SUM(tokens) FROM token_usage
            WHERE tenant_id = ? AND timestamp >= ?
        """, (tenant_id, month_start.isoformat())).fetchone()
        
        return result[0] or 0
    
    def get_usage_by_agent(self, tenant_id: str, days: int = 7) -> Dict:
        """Get token usage broken down by agent"""
        cutoff = datetime.now() - timedelta(days=days)
        
        rows = self.db.execute("""
            SELECT agent_type, SUM(tokens) as total_tokens
            FROM token_usage
            WHERE tenant_id = ? AND timestamp >= ?
            GROUP BY agent_type
        """, (tenant_id, cutoff.isoformat())).fetchall()
        
        return {row[0]: row[1] for row in rows}
    
    def get_usage_by_model(self, tenant_id: str, days: int = 7) -> Dict:
        """Get token usage broken down by model"""
        cutoff = datetime.now() - timedelta(days=days)
        
        rows = self.db.execute("""
            SELECT model, SUM(tokens) as total_tokens
            FROM token_usage
            WHERE tenant_id = ? AND timestamp >= ?
            GROUP BY model
        """, (tenant_id, cutoff.isoformat())).fetchall()
        
        return {row[0]: row[1] for row in rows}
    
    def get_cost(self, tenant_id: str, days: int = 30) -> float:
        """Get total cost in USD"""
        cutoff = datetime.now() - timedelta(days=days)
        
        result = self.db.execute("""
            SELECT SUM(cost_usd) FROM token_usage
            WHERE tenant_id = ? AND timestamp >= ?
        """, (tenant_id, cutoff.isoformat())).fetchone()
        
        return result[0] or 0
    
    # ==================== TASK LOGGING ====================
    
    def log_task(self, tenant_id: str, agent_type: str,
                 task_description: str, sub_agent: str = None,
                 execution_time_ms: int = None, status: str = "completed"):
        """Log task execution"""
        self.db.execute("""
            INSERT INTO task_log 
            (tenant_id, agent_type, sub_agent, task_description, execution_time_ms, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tenant_id, agent_type, sub_agent, task_description, execution_time_ms, status))
        self.db.commit()
        
        # Update daily summary
        self.db.execute("""
            INSERT OR REPLACE INTO daily_summary 
            (tenant_id, date, total_tasks)
            VALUES (?, DATE('now'), 
                COALESCE((SELECT total_tasks FROM daily_summary 
                         WHERE tenant_id = ? AND date = DATE('now')), 0) + 1)
        """, (tenant_id, tenant_id))
        self.db.commit()
    
    def get_task_count(self, tenant_id: str, days: int = 30) -> int:
        """Get number of tasks executed"""
        cutoff = datetime.now() - timedelta(days=days)
        
        result = self.db.execute("""
            SELECT COUNT(*) FROM task_log
            WHERE tenant_id = ? AND timestamp >= ?
        """, (tenant_id, cutoff.isoformat())).fetchone()
        
        return result[0] or 0
    
    def get_task_history(self, tenant_id: str, limit: int = 50) -> List[Dict]:
        """Get recent task history"""
        rows = self.db.execute("""
            SELECT * FROM task_log
            WHERE tenant_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (tenant_id, limit)).fetchall()
        
        return [{
            'id': row[0],
            'tenant_id': row[1],
            'agent_type': row[2],
            'sub_agent': row[3],
            'task_description': row[4],
            'status': row[5],
            'execution_time_ms': row[6],
            'timestamp': row[7]
        } for row in rows]
    
    # ==================== API CALLS ====================
    
    def log_api_call(self, tenant_id: str, endpoint: str,
                     method: str = "GET", response_time_ms: int = None,
                     status_code: int = 200):
        """Log API call"""
        self.db.execute("""
            INSERT INTO api_calls 
            (tenant_id, endpoint, method, response_time_ms, status_code)
            VALUES (?, ?, ?, ?, ?)
        """, (tenant_id, endpoint, method, response_time_ms, status_code))
        self.db.commit()
        
        # Update daily summary
        self.db.execute("""
            INSERT OR REPLACE INTO daily_summary 
            (tenant_id, date, total_api_calls)
            VALUES (?, DATE('now'), 
                COALESCE((SELECT total_api_calls FROM daily_summary 
                         WHERE tenant_id = ? AND date = DATE('now')), 0) + 1)
        """, (tenant_id, tenant_id))
        self.db.commit()
    
    # ==================== DAILY SUMMARY ====================
    
    def _update_daily_summary(self, tenant_id: str, tokens: int, cost_usd: float):
        """Update daily summary with new usage"""
        self.db.execute("""
            INSERT OR REPLACE INTO daily_summary 
            (tenant_id, date, total_tokens, total_cost_usd)
            VALUES (?, DATE('now'), 
                COALESCE((SELECT total_tokens FROM daily_summary 
                         WHERE tenant_id = ? AND date = DATE('now')), 0) + ?,
                COALESCE((SELECT total_cost_usd FROM daily_summary 
                         WHERE tenant_id = ? AND date = DATE('now')), 0) + ?)
        """, (tenant_id, tenant_id, tokens, tenant_id, cost_usd))
        self.db.commit()
    
    def get_daily_summary(self, tenant_id: str, days: int = 30) -> List[Dict]:
        """Get daily usage summary"""
        cutoff = datetime.now() - timedelta(days=days)
        
        rows = self.db.execute("""
            SELECT * FROM daily_summary
            WHERE tenant_id = ? AND date >= ?
            ORDER BY date DESC
        """, (tenant_id, cutoff.date().isoformat())).fetchall()
        
        return [{
            'date': row[2],
            'total_tokens': row[3],
            'total_tasks': row[4],
            'total_api_calls': row[5],
            'total_cost_usd': row[6]
        } for row in rows]
    
    # ==================== ALERTS ====================
    
    def _check_usage_alerts(self, tenant_id: str, limit: int = None):
        """Check if usage exceeds thresholds and create alerts"""
        if limit is None:
            # Would need to get from tenant config
            return
        
        monthly_usage = self.get_monthly_usage(tenant_id)
        usage_percent = (monthly_usage / limit * 100) if limit > 0 else 0
        
        # Check thresholds
        thresholds = [80, 90, 100]
        
        for threshold in thresholds:
            if usage_percent >= threshold:
                # Check if alert already exists
                existing = self.db.execute("""
                    SELECT * FROM alerts
                    WHERE tenant_id = ? AND alert_type = 'usage_threshold'
                    AND threshold_percent = ? AND is_resolved = FALSE
                """, (tenant_id, threshold)).fetchone()
                
                if not existing:
                    self.db.execute("""
                        INSERT INTO alerts 
                        (tenant_id, alert_type, message, threshold_percent)
                        VALUES (?, 'usage_threshold', 
                               ?, ?)
                    """, (tenant_id, 
                          f"Usage exceeded {threshold}% of monthly limit",
                          threshold))
                    self.db.commit()
    
    def get_alerts(self, tenant_id: str = None, unresolved_only: bool = True) -> List[Dict]:
        """Get alerts"""
        query = "SELECT * FROM alerts WHERE 1=1"
        params = []
        
        if tenant_id:
            query += " AND tenant_id = ?"
            params.append(tenant_id)
        
        if unresolved_only:
            query += " AND is_resolved = FALSE"
        
        rows = self.db.execute(query, params).fetchall()
        
        return [{
            'id': row[0],
            'tenant_id': row[1],
            'alert_type': row[2],
            'message': row[3],
            'threshold_percent': row[4],
            'is_resolved': row[5],
            'created_at': row[6],
            'resolved_at': row[7]
        } for row in rows]
    
    def resolve_alert(self, alert_id: int):
        """Mark alert as resolved"""
        self.db.execute("""
            UPDATE alerts 
            SET is_resolved = TRUE, resolved_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (alert_id,))
        self.db.commit()
    
    # ==================== REPORTS ====================
    
    def generate_report(self, tenant_id: str = None) -> Dict:
        """Generate comprehensive usage report"""
        if tenant_id:
            # Single tenant
            return {
                'tenant_id': tenant_id,
                'period': 'last_30_days',
                'total_tokens': self.get_token_usage(tenant_id, 30),
                'monthly_tokens': self.get_monthly_usage(tenant_id),
                'total_tasks': self.get_task_count(tenant_id, 30),
                'total_cost': self.get_cost(tenant_id, 30),
                'usage_by_agent': self.get_usage_by_agent(tenant_id, 7),
                'usage_by_model': self.get_usage_by_model(tenant_id, 7),
                'recent_tasks': self.get_task_history(tenant_id, 10),
                'alerts': self.get_alerts(tenant_id, True)
            }
        else:
            # All tenants - aggregate
            all_tenants = self.db.execute("""
                SELECT DISTINCT tenant_id FROM token_usage
            """).fetchall()
            
            reports = []
            for (tenant_id,) in all_tenants:
                report = self.generate_report(tenant_id)
                reports.append(report)
            
            return {
                'period': 'last_30_days',
                'total_tenants': len(reports),
                'tenants': reports
            }

# CLI
def main():
    import sys
    
    tracker = UsageTracker()
    
    if len(sys.argv) < 2:
        print("Usage Tracker - Multi-Agent Platform")
        print("\nUsage:")
        print("  python usage_tracker.py record <tenant_id> <tokens> [model] [agent]")
        print("  python usage_tracker.py usage <tenant_id> [days]")
        print("  python usage_tracker.py monthly <tenant_id>")
        print("  python usage_tracker.py tasks <tenant_id>")
        print("  python usage_tracker.py cost <tenant_id>")
        print("  python usage_tracker.py report [tenant_id]")
        print("  python usage_tracker.py alerts [tenant_id]")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "record":
        if len(sys.argv) < 4:
            print("Usage: python usage_tracker.py record <tenant_id> <tokens> [model] [agent]")
            sys.exit(1)
        
        tenant_id = sys.argv[2]
        tokens = int(sys.argv[3])
        model = sys.argv[4] if len(sys.argv) > 4 else None
        agent = sys.argv[5] if len(sys.argv) > 5 else None
        
        tracker.record_token_usage(tenant_id, tokens, model, agent)
        print(f"✅ Recorded {tokens} tokens for {tenant_id}")
    
    elif command == "usage":
        if len(sys.argv) < 3:
            print("Usage: python usage_tracker.py usage <tenant_id> [days]")
            sys.exit(1)
        
        tenant_id = sys.argv[2]
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        
        usage = tracker.get_token_usage(tenant_id, days)
        print(f"\n📊 Token Usage: {tenant_id}")
        print(f"   Last {days} days: {usage:,} tokens\n")
    
    elif command == "monthly":
        if len(sys.argv) < 3:
            print("Usage: python usage_tracker.py monthly <tenant_id>")
            sys.exit(1)
        
        tenant_id = sys.argv[2]
        usage = tracker.get_monthly_usage(tenant_id)
        print(f"\n📊 Monthly Usage: {tenant_id}")
        print(f"   This month: {usage:,} tokens\n")
    
    elif command == "tasks":
        if len(sys.argv) < 3:
            print("Usage: python usage_tracker.py tasks <tenant_id>")
            sys.exit(1)
        
        tenant_id = sys.argv[2]
        count = tracker.get_task_count(tenant_id)
        print(f"\n📊 Task Count: {tenant_id}")
        print(f"   Last 30 days: {count:,} tasks\n")
    
    elif command == "cost":
        if len(sys.argv) < 3:
            print("Usage: python usage_tracker.py cost <tenant_id>")
            sys.exit(1)
        
        tenant_id = sys.argv[2]
        cost = tracker.get_cost(tenant_id)
        print(f"\n📊 Cost: {tenant_id}")
        print(f"   Last 30 days: ${cost:.2f}\n")
    
    elif command == "report":
        tenant_id = sys.argv[2] if len(sys.argv) > 2 else None
        report = tracker.generate_report(tenant_id)
        
        print("\n📊 Usage Report\n")
        print(json.dumps(report, indent=2, default=str))
        print()
    
    elif command == "alerts":
        tenant_id = sys.argv[2] if len(sys.argv) > 2 else None
        alerts = tracker.get_alerts(tenant_id)
        
        if not alerts:
            print("✅ No unresolved alerts")
        else:
            print(f"\n🚨 Alerts ({len(alerts)}):\n")
            for alert in alerts:
                print(f"  [{alert['id']}] {alert['tenant_id']}: {alert['message']}")
                print(f"      Threshold: {alert['threshold_percent']}%")
                print(f"      Created: {alert['created_at']}")
                print()
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
