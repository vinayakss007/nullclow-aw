#!/usr/bin/env python3
"""
Tenant Manager - Create and manage customer workspaces
Each tenant gets isolated workspace, agents, and usage limits
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime

# Pricing plans
PLANS = {
    "free": {
        "monthly_tokens": 10000,
        "max_agents": 1,
        "max_workspace_mb": 100,
        "price_monthly": 0,
        "allowed_agents": ["basic"],
        "allowed_sub_agents": ["searcher"]
    },
    "starter": {
        "monthly_tokens": 100000,
        "max_agents": 3,
        "max_workspace_mb": 500,
        "price_monthly": 29,
        "allowed_agents": ["sales", "support", "research"],
        "allowed_sub_agents": ["lead_scorer", "email_writer", "response_generator", "searcher", "summarizer"]
    },
    "pro": {
        "monthly_tokens": 500000,
        "max_agents": 10,
        "max_workspace_mb": 5000,
        "price_monthly": 99,
        "allowed_agents": ["all"],
        "allowed_sub_agents": ["all"]
    },
    "enterprise": {
        "monthly_tokens": -1,  # unlimited
        "max_agents": -1,
        "max_workspace_mb": 50000,
        "price_monthly": 499,
        "allowed_agents": ["all"],
        "allowed_sub_agents": ["all"],
        "custom_agents": True
    }
}

class TenantManager:
    def __init__(self, base_path="./customers"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        self._create_registry()
    
    def _create_registry(self):
        """Create tenant registry file"""
        registry_file = self.base_path / "registry.json"
        if not registry_file.exists():
            with open(registry_file, 'w') as f:
                json.dump({"tenants": [], "created_at": str(datetime.now())}, f, indent=2)
    
    def _get_registry(self):
        """Load tenant registry"""
        registry_file = self.base_path / "registry.json"
        with open(registry_file) as f:
            return json.load(f)
    
    def _save_registry(self, registry):
        """Save tenant registry"""
        registry_file = self.base_path / "registry.json"
        with open(registry_file, 'w') as f:
            json.dump(registry, f, indent=2)
    
    def create_tenant(self, name: str, plan: str = "starter", 
                      email: str = None, telegram_bot_token: str = None) -> str:
        """
        Create a new tenant workspace
        
        Args:
            name: Customer/company name
            plan: free, starter, pro, or enterprise
            email: Customer email
            telegram_bot_token: Telegram bot token for this tenant
        
        Returns:
            tenant_id
        """
        if plan not in PLANS:
            raise ValueError(f"Invalid plan: {plan}. Must be one of: {list(PLANS.keys())}")
        
        # Generate tenant ID
        registry = self._get_registry()
        tenant_num = len(registry['tenants'])
        tenant_id = f"tenant_{tenant_num:03d}"
        
        # Create workspace directories
        tenant_path = self.base_path / tenant_id
        (tenant_path / "workspace").mkdir(parents=True, exist_ok=True)
        (tenant_path / "data").mkdir(parents=True, exist_ok=True)
        (tenant_path / "memory").mkdir(parents=True, exist_ok=True)
        (tenant_path / "agents").mkdir(parents=True, exist_ok=True)
        
        # Create tenant config
        config = {
            "tenant_id": tenant_id,
            "name": name,
            "plan": plan,
            "email": email,
            "created_at": str(datetime.now()),
            "status": "active",
            "telegram_bot_token": telegram_bot_token,
            "limits": PLANS[plan],
            "usage": {
                "tokens_used_this_month": 0,
                "tasks_created": 0,
                "agents_active": 0
            },
            "settings": {
                "timezone": "UTC",
                "language": "en",
                "notifications_enabled": True
            }
        }
        
        # Save config
        config_file = tenant_path / "config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Create Nullclaw config for this tenant
        nullclaw_config = self._create_nullclaw_config(tenant_id, telegram_bot_token)
        nullclaw_config_file = tenant_path / "nullclaw_config.json"
        with open(nullclaw_config_file, 'w') as f:
            json.dump(nullclaw_config, f, indent=2)
        
        # Add to registry
        registry['tenants'].append({
            "tenant_id": tenant_id,
            "name": name,
            "plan": plan,
            "email": email,
            "created_at": str(datetime.now()),
            "status": "active"
        })
        self._save_registry(registry)
        
        print(f"✅ Created tenant: {tenant_id}")
        print(f"   Name: {name}")
        print(f"   Plan: {plan}")
        print(f"   Workspace: {tenant_path}")
        print(f"   Token Limit: {PLANS[plan]['monthly_tokens']}")
        
        return tenant_id
    
    def _create_nullclaw_config(self, tenant_id: str, telegram_bot_token: str = None):
        """Create Nullclaw configuration for tenant"""
        config = {
            "tenant_id": tenant_id,
            "workspace": f"./customers/{tenant_id}/workspace",
            "memory": {
                "backend": "sqlite",
                "path": f"./customers/{tenant_id}/memory/memory.db"
            },
            "channels": {}
        }
        
        if telegram_bot_token:
            config["channels"]["telegram"] = {
                "accounts": {
                    "main": {
                        "bot_token": telegram_bot_token,
                        "allow_from": ["all"],
                        "reply_in_private": True
                    }
                }
            }
        
        return config
    
    def get_tenant(self, tenant_id: str) -> dict:
        """Get tenant by ID"""
        tenant_path = self.base_path / tenant_id
        config_file = tenant_path / "config.json"
        
        if not config_file.exists():
            return None
        
        with open(config_file) as f:
            return json.load(f)
    
    def list_tenants(self, status: str = None) -> list:
        """List all tenants"""
        registry = self._get_registry()
        tenants = registry['tenants']
        
        if status:
            tenants = [t for t in tenants if t.get('status') == status]
        
        return tenants
    
    def update_tenant(self, tenant_id: str, updates: dict):
        """Update tenant configuration"""
        tenant = self.get_tenant(tenant_id)
        if not tenant:
            raise ValueError(f"Tenant not found: {tenant_id}")
        
        # Update fields
        for key, value in updates.items():
            if key in tenant:
                tenant[key] = value
        
        # Save
        tenant_path = self.base_path / tenant_id
        config_file = tenant_path / "config.json"
        with open(config_file, 'w') as f:
            json.dump(tenant, f, indent=2)
        
        print(f"✅ Updated tenant: {tenant_id}")
    
    def delete_tenant(self, tenant_id: str):
        """Delete tenant (soft delete - just mark as inactive)"""
        tenant = self.get_tenant(tenant_id)
        if not tenant:
            raise ValueError(f"Tenant not found: {tenant_id}")
        
        # Mark as inactive
        self.update_tenant(tenant_id, {"status": "inactive"})
        
        print(f"✅ Tenant {tenant_id} marked as inactive")
    
    def hard_delete_tenant(self, tenant_id: str):
        """Permanently delete tenant and all data"""
        tenant_path = self.base_path / tenant_id
        
        if not tenant_path.exists():
            raise ValueError(f"Tenant not found: {tenant_id}")
        
        # Remove from registry
        registry = self._get_registry()
        registry['tenants'] = [t for t in registry['tenants'] if t['tenant_id'] != tenant_id]
        self._save_registry(registry)
        
        # Delete directory
        shutil.rmtree(tenant_path)
        
        print(f"✅ Permanently deleted tenant: {tenant_id}")
    
    def check_usage_limit(self, tenant_id: str, tokens_requested: int) -> bool:
        """Check if tenant can use requested tokens"""
        tenant = self.get_tenant(tenant_id)
        if not tenant:
            return False
        
        plan = tenant['plan']
        limit = PLANS[plan]['monthly_tokens']
        
        # Unlimited
        if limit < 0:
            return True
        
        used = tenant['usage']['tokens_used_this_month']
        
        return (used + tokens_requested) <= limit
    
    def record_usage(self, tenant_id: str, tokens: int, agent: str = None):
        """Record token usage for tenant"""
        tenant = self.get_tenant(tenant_id)
        if not tenant:
            return
        
        tenant['usage']['tokens_used_this_month'] += tokens
        tenant['usage']['tasks_created'] += 1
        
        if agent:
            tenant['usage']['agents_active'] = tenant['usage'].get('agents_active', 0) + 1
        
        # Save
        tenant_path = self.base_path / tenant_id
        config_file = tenant_path / "config.json"
        with open(config_file, 'w') as f:
            json.dump(tenant, f, indent=2)
    
    def reset_monthly_usage(self):
        """Reset monthly usage for all tenants (run on 1st of month)"""
        registry = self._get_registry()
        
        for tenant_info in registry['tenants']:
            tenant = self.get_tenant(tenant_info['tenant_id'])
            if tenant:
                tenant['usage']['tokens_used_this_month'] = 0
                tenant['usage']['tasks_created'] = 0
                
                # Save
                tenant_path = self.base_path / tenant_info['tenant_id']
                config_file = tenant_path / "config.json"
                with open(config_file, 'w') as f:
                    json.dump(tenant, f, indent=2)
        
        print(f"✅ Reset monthly usage for {len(registry['tenants'])} tenants")
    
    def get_usage_report(self, tenant_id: str = None) -> dict:
        """Get usage report"""
        registry = self._get_registry()
        
        if tenant_id:
            tenant = self.get_tenant(tenant_id)
            if not tenant:
                return None
            
            return {
                "tenant_id": tenant_id,
                "name": tenant['name'],
                "plan": tenant['plan'],
                "tokens_used": tenant['usage']['tokens_used_this_month'],
                "tokens_limit": PLANS[tenant['plan']]['monthly_tokens'],
                "tasks_created": tenant['usage']['tasks_created'],
                "usage_percent": (tenant['usage']['tokens_used_this_month'] / PLANS[tenant['plan']]['monthly_tokens'] * 100) if PLANS[tenant['plan']]['monthly_tokens'] > 0 else 0
            }
        else:
            # All tenants
            reports = []
            for tenant_info in registry['tenants']:
                report = self.get_usage_report(tenant_info['tenant_id'])
                if report:
                    reports.append(report)
            
            return {
                "total_tenants": len(reports),
                "tenants": reports
            }

# CLI
def main():
    import sys
    
    manager = TenantManager()
    
    if len(sys.argv) < 2:
        print("Tenant Manager - Multi-Agent Platform")
        print("\nUsage:")
        print("  python tenant_manager.py create <name> [plan] [email] [telegram_token]")
        print("  python tenant_manager.py list")
        print("  python tenant_manager.py get <tenant_id>")
        print("  python tenant_manager.py update <tenant_id> <field> <value>")
        print("  python tenant_manager.py delete <tenant_id>")
        print("  python tenant_manager.py usage [tenant_id]")
        print("  python tenant_manager.py reset-usage")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "create":
        if len(sys.argv) < 3:
            print("Usage: python tenant_manager.py create <name> [plan] [email] [telegram_token]")
            sys.exit(1)
        
        name = sys.argv[2]
        plan = sys.argv[3] if len(sys.argv) > 3 else "starter"
        email = sys.argv[4] if len(sys.argv) > 4 else None
        telegram_token = sys.argv[5] if len(sys.argv) > 5 else None
        
        manager.create_tenant(name, plan, email, telegram_token)
    
    elif command == "list":
        tenants = manager.list_tenants()
        print(f"\n📋 Tenants ({len(tenants)}):\n")
        for t in tenants:
            print(f"  {t['tenant_id']}: {t['name']} ({t['plan']}) - {t['status']}")
        print()
    
    elif command == "get":
        if len(sys.argv) < 3:
            print("Usage: python tenant_manager.py get <tenant_id>")
            sys.exit(1)
        
        tenant_id = sys.argv[2]
        tenant = manager.get_tenant(tenant_id)
        
        if tenant:
            print(f"\n📄 Tenant: {tenant_id}\n")
            print(f"  Name: {tenant['name']}")
            print(f"  Plan: {tenant['plan']}")
            print(f"  Email: {tenant.get('email', 'N/A')}")
            print(f"  Status: {tenant['status']}")
            print(f"  Created: {tenant['created_at']}")
            print(f"  Tokens Used: {tenant['usage']['tokens_used_this_month']}")
            print()
        else:
            print(f"Tenant not found: {tenant_id}")
    
    elif command == "update":
        if len(sys.argv) < 5:
            print("Usage: python tenant_manager.py update <tenant_id> <field> <value>")
            sys.exit(1)
        
        tenant_id = sys.argv[2]
        field = sys.argv[3]
        value = sys.argv[4]
        
        manager.update_tenant(tenant_id, {field: value})
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: python tenant_manager.py delete <tenant_id>")
            sys.exit(1)
        
        tenant_id = sys.argv[2]
        manager.delete_tenant(tenant_id)
    
    elif command == "usage":
        tenant_id = sys.argv[2] if len(sys.argv) > 2 else None
        report = manager.get_usage_report(tenant_id)
        
        if tenant_id:
            if report:
                print(f"\n📊 Usage Report: {report['name']}\n")
                print(f"  Plan: {report['plan']}")
                print(f"  Tokens: {report['tokens_used']} / {report['tokens_limit']}")
                print(f"  Usage: {report['usage_percent']:.1f}%")
                print(f"  Tasks: {report['tasks_created']}")
                print()
            else:
                print(f"Tenant not found: {tenant_id}")
        else:
            print(f"\n📊 Usage Report (All Tenants)\n")
            print(f"  Total Tenants: {report['total_tenants']}")
            for t in report['tenants']:
                print(f"  {t['tenant_id']}: {t['name']} - {t['tokens_used']}/{t['tokens_limit']} tokens ({t['usage_percent']:.1f}%)")
            print()
    
    elif command == "reset-usage":
        manager.reset_monthly_usage()
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
