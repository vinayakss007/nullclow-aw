#!/usr/bin/env python3
"""
Admin Control Panel - Multi-Agent Platform
Complete admin controls for managing tenants, usage, billing, and system
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Import platform modules
from tenant_manager import TenantManager, PLANS
from usage_tracker import UsageTracker

class AdminControlPanel:
    """
    Admin Control Panel for platform management
    """
    
    def __init__(self):
        self.tenant_manager = TenantManager()
        self.usage_tracker = UsageTracker()
        self.admin_config_file = Path("admin_config.json")
        self._load_admin_config()
    
    def _load_admin_config(self):
        """Load admin configuration"""
        if self.admin_config_file.exists():
            with open(self.admin_config_file) as f:
                self.admin_config = json.load(f)
        else:
            self.admin_config = {
                "admin_email": "admin@example.com",
                "platform_name": "Multi-Agent Platform",
                "testing_mode": True,
                "maintenance_mode": False,
                "max_tenants_per_account": 10,
                "auto_approve_tenants": True
            }
            self._save_admin_config()
    
    def _save_admin_config(self):
        """Save admin configuration"""
        with open(self.admin_config_file, 'w') as f:
            json.dump(self.admin_config, f, indent=2)
    
    # ==================== TENANT MANAGEMENT ====================
    
    def list_all_tenants(self, status=None):
        """List all tenants with detailed info"""
        tenants = self.tenant_manager.list_tenants(status)
        
        print(f"\n{'='*80}")
        print(f"ADMIN: ALL TENANTS ({len(tenants)})")
        print(f"{'='*80}\n")
        
        for tenant in tenants:
            tenant_data = self.tenant_manager.get_tenant(tenant['tenant_id'])
            if tenant_data:
                usage = self.usage_tracker.get_monthly_usage(tenant['tenant_id'])
                limit = PLANS[tenant_data['plan']]['monthly_tokens']
                
                print(f"📁 {tenant['tenant_id']}: {tenant['name']}")
                print(f"   Plan: {tenant_data['plan']}")
                print(f"   Email: {tenant_data.get('email', 'N/A')}")
                print(f"   Status: {tenant_data['status']}")
                print(f"   Usage: {usage:,} / {limit if limit > 0 else '∞'} tokens")
                print(f"   Created: {tenant_data['created_at']}")
                print(f"   Telegram: {'✅' if tenant_data.get('telegram_bot_token') else '❌'}")
                print()
        
        return tenants
    
    def suspend_tenant(self, tenant_id, reason=""):
        """Suspend a tenant"""
        tenant = self.tenant_manager.get_tenant(tenant_id)
        if not tenant:
            print(f"❌ Tenant not found: {tenant_id}")
            return False
        
        self.tenant_manager.update_tenant(tenant_id, {
            "status": "suspended",
            "suspended_at": str(datetime.now()),
            "suspension_reason": reason
        })
        
        print(f"✅ Suspended tenant: {tenant_id}")
        print(f"   Reason: {reason}")
        return True
    
    def activate_tenant(self, tenant_id):
        """Activate a suspended tenant"""
        tenant = self.tenant_manager.get_tenant(tenant_id)
        if not tenant:
            print(f"❌ Tenant not found: {tenant_id}")
            return False
        
        self.tenant_manager.update_tenant(tenant_id, {
            "status": "active",
            "suspended_at": None,
            "suspension_reason": None
        })
        
        print(f"✅ Activated tenant: {tenant_id}")
        return True
    
    def delete_tenant(self, tenant_id, hard_delete=False):
        """Delete a tenant"""
        if hard_delete:
            self.tenant_manager.hard_delete_tenant(tenant_id)
            print(f"✅ Permanently deleted tenant: {tenant_id}")
        else:
            self.tenant_manager.delete_tenant(tenant_id)
            print(f"✅ Soft deleted tenant: {tenant_id}")
    
    def upgrade_tenant(self, tenant_id, new_plan):
        """Upgrade tenant plan"""
        if new_plan not in PLANS:
            print(f"❌ Invalid plan: {new_plan}")
            return False
        
        self.tenant_manager.update_tenant(tenant_id, {"plan": new_plan})
        print(f"✅ Upgraded {tenant_id} to {new_plan} plan")
        return True
    
    def reset_tenant_usage(self, tenant_id):
        """Reset tenant's monthly usage"""
        tenant = self.tenant_manager.get_tenant(tenant_id)
        if not tenant:
            print(f"❌ Tenant not found: {tenant_id}")
            return False
        
        tenant['usage']['tokens_used_this_month'] = 0
        tenant['usage']['tasks_created'] = 0
        
        # Save
        tenant_path = Path(self.tenant_manager.base_path) / tenant_id
        config_file = tenant_path / "config.json"
        with open(config_file, 'w') as f:
            json.dump(tenant, f, indent=2)
        
        print(f"✅ Reset usage for {tenant_id}")
        return True
    
    # ==================== USAGE CONTROL ====================
    
    def set_tenant_limit(self, tenant_id, custom_limit):
        """Set custom token limit for tenant"""
        tenant = self.tenant_manager.get_tenant(tenant_id)
        if not tenant:
            print(f"❌ Tenant not found: {tenant_id}")
            return False
        
        tenant['custom_token_limit'] = custom_limit
        
        # Save
        tenant_path = Path(self.tenant_manager.base_path) / tenant_id
        config_file = tenant_path / "config.json"
        with open(config_file, 'w') as f:
            json.dump(tenant, f, indent=2)
        
        print(f"✅ Set custom limit for {tenant_id}: {custom_limit:,} tokens")
        return True
    
    def add_bonus_tokens(self, tenant_id, bonus_amount):
        """Add bonus tokens to tenant"""
        tenant = self.tenant_manager.get_tenant(tenant_id)
        if not tenant:
            print(f"❌ Tenant not found: {tenant_id}")
            return False
        
        current_bonus = tenant.get('bonus_tokens', 0)
        tenant['bonus_tokens'] = current_bonus + bonus_amount
        
        # Save
        tenant_path = Path(self.tenant_manager.base_path) / tenant_id
        config_file = tenant_path / "config.json"
        with open(config_file, 'w') as f:
            json.dump(tenant, f, indent=2)
        
        print(f"✅ Added {bonus_amount:,} bonus tokens to {tenant_id}")
        print(f"   Total bonus: {tenant['bonus_tokens']:,} tokens")
        return True
    
    # ==================== SYSTEM CONTROL ====================
    
    def enable_maintenance_mode(self):
        """Enable maintenance mode"""
        self.admin_config['maintenance_mode'] = True
        self._save_admin_config()
        print("⚠️  MAINTENANCE MODE ENABLED")
        print("   No new tasks will be processed")
        return True
    
    def disable_maintenance_mode(self):
        """Disable maintenance mode"""
        self.admin_config['maintenance_mode'] = False
        self._save_admin_config()
        print("✅ MAINTENANCE MODE DISABLED")
        print("   System is back online")
        return True
    
    def toggle_testing_mode(self):
        """Toggle testing mode"""
        self.admin_config['testing_mode'] = not self.admin_config['testing_mode']
        self._save_admin_config()
        
        status = "ENABLED" if self.admin_config['testing_mode'] else "DISABLED"
        print(f"✅ TESTING MODE {status}")
        return self.admin_config['testing_mode']
    
    # ==================== REPORTS ====================
    
    def platform_report(self):
        """Generate comprehensive platform report"""
        tenants = self.tenant_manager.list_tenants()
        
        total_tenants = len(tenants)
        active_tenants = len([t for t in tenants if t.get('status') == 'active'])
        suspended_tenants = len([t for t in tenants if t.get('status') == 'suspended'])
        
        # Calculate total usage
        total_usage = 0
        for tenant in tenants:
            usage = self.usage_tracker.get_monthly_usage(tenant['tenant_id'])
            total_usage += usage
        
        # Plan distribution
        plan_counts = {}
        for tenant in tenants:
            plan = tenant['plan']
            plan_counts[plan] = plan_counts.get(plan, 0) + 1
        
        print(f"\n{'='*80}")
        print(f"PLATFORM REPORT")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        print(f"📊 TENANTS")
        print(f"   Total: {total_tenants}")
        print(f"   Active: {active_tenants}")
        print(f"   Suspended: {suspended_tenants}")
        print()
        
        print(f"📈 PLANS")
        for plan, count in plan_counts.items():
            print(f"   {plan.capitalize()}: {count}")
        print()
        
        print(f"💰 USAGE")
        print(f"   Total Tokens (this month): {total_usage:,}")
        print(f"   Average per Tenant: {total_usage // total_tenants if total_tenants > 0 else 0:,}")
        print()
        
        print(f"⚙️  SYSTEM")
        print(f"   Testing Mode: {'✅ ON' if self.admin_config['testing_mode'] else '❌ OFF'}")
        print(f"   Maintenance Mode: {'⚠️  ON' if self.admin_config['maintenance_mode'] else '✅ OFF'}")
        print()
        
        return {
            'total_tenants': total_tenants,
            'active_tenants': active_tenants,
            'suspended_tenants': suspended_tenants,
            'total_usage': total_usage,
            'plan_distribution': plan_counts
        }
    
    def top_users_report(self, limit=10):
        """Get top users by token usage"""
        tenants = self.tenant_manager.list_tenants()
        
        usage_data = []
        for tenant in tenants:
            usage = self.usage_tracker.get_monthly_usage(tenant['tenant_id'])
            usage_data.append({
                'tenant_id': tenant['tenant_id'],
                'name': tenant['name'],
                'plan': tenant['plan'],
                'usage': usage
            })
        
        # Sort by usage
        usage_data.sort(key=lambda x: x['usage'], reverse=True)
        
        print(f"\n{'='*80}")
        print(f"TOP {limit} USERS BY TOKEN USAGE")
        print(f"{'='*80}\n")
        
        for i, user in enumerate(usage_data[:limit], 1):
            print(f"{i:2}. {user['tenant_id']}: {user['name']}")
            print(f"    Plan: {user['plan']} | Usage: {user['usage']:,} tokens")
            print()
        
        return usage_data[:limit]
    
    # ==================== BILLING ====================
    
    def generate_invoice(self, tenant_id, month=None):
        """Generate invoice for tenant"""
        tenant = self.tenant_manager.get_tenant(tenant_id)
        if not tenant:
            print(f"❌ Tenant not found: {tenant_id}")
            return None
        
        usage = self.usage_tracker.get_monthly_usage(tenant_id)
        plan = tenant['plan']
        base_price = PLANS[plan]['price_monthly']
        limit = PLANS[plan]['monthly_tokens']
        
        # Calculate overage
        overage_tokens = max(0, usage - limit) if limit > 0 else 0
        overage_cost = overage_tokens * 0.00001  # $0.01 per 1K tokens
        
        total = base_price + overage_cost
        
        invoice = {
            'tenant_id': tenant_id,
            'tenant_name': tenant['name'],
            'month': month or datetime.now().strftime('%Y-%m'),
            'plan': plan,
            'base_price': base_price,
            'tokens_used': usage,
            'token_limit': limit,
            'overage_tokens': overage_tokens,
            'overage_cost': overage_cost,
            'total': total,
            'generated_at': str(datetime.now())
        }
        
        print(f"\n{'='*80}")
        print(f"INVOICE")
        print(f"{'='*80}\n")
        print(f"Tenant: {tenant['name']} ({tenant_id})")
        print(f"Period: {invoice['month']}")
        print(f"Plan: {plan} - ${base_price:.2f}")
        print(f"Usage: {usage:,} / {limit if limit > 0 else '∞'} tokens")
        if overage_tokens > 0:
            print(f"Overage: {overage_tokens:,} tokens - ${overage_cost:.2f}")
        print(f"\nTOTAL: ${total:.2f}")
        print(f"{'='*80}\n")
        
        return invoice
    
    # ==================== ADMIN HELP ====================
    
    def show_admin_commands(self):
        """Show all admin commands"""
        print(f"\n{'='*80}")
        print(f"ADMIN CONTROL PANEL - COMMANDS")
        print(f"{'='*80}\n")
        
        commands = {
            "Tenant Management": [
                "list - List all tenants",
                "suspend <id> [reason] - Suspend tenant",
                "activate <id> - Activate tenant",
                "delete <id> [--hard] - Delete tenant",
                "upgrade <id> <plan> - Upgrade plan",
                "reset-usage <id> - Reset monthly usage"
            ],
            "Usage Control": [
                "set-limit <id> <limit> - Set custom limit",
                "add-bonus <id> <amount> - Add bonus tokens"
            ],
            "System Control": [
                "maintenance on|off - Toggle maintenance mode",
                "testing on|off - Toggle testing mode",
                "report - Platform report",
                "top-users [n] - Top users by usage"
            ],
            "Billing": [
                "invoice <id> - Generate invoice"
            ],
            "Help": [
                "help - Show this help",
                "exit - Exit admin panel"
            ]
        }
        
        for category, cmds in commands.items():
            print(f"📁 {category}")
            for cmd in cmds:
                print(f"   {cmd}")
            print()
        
        print(f"{'='*80}\n")


# ==================== CLI ====================

def main():
    admin = AdminControlPanel()
    
    if len(sys.argv) < 2:
        # Interactive mode
        print("\n🎛️  ADMIN CONTROL PANEL")
        print("Type 'help' for commands\n")
        
        while True:
            try:
                command = input("admin> ").strip()
                
                if not command:
                    continue
                
                if command in ['exit', 'quit', 'q']:
                    print("Exiting admin panel...")
                    break
                
                if command == 'help':
                    admin.show_admin_commands()
                    continue
                
                if command == 'list':
                    admin.list_all_tenants()
                    continue
                
                if command == 'report':
                    admin.platform_report()
                    continue
                
                if command == 'top-users':
                    admin.top_users_report()
                    continue
                
                if command.startswith('suspend '):
                    parts = command.split(' ', 2)
                    tenant_id = parts[1] if len(parts) > 1 else None
                    reason = parts[2] if len(parts) > 2 else "No reason provided"
                    if tenant_id:
                        admin.suspend_tenant(tenant_id, reason)
                    continue
                
                if command.startswith('activate '):
                    parts = command.split(' ')
                    tenant_id = parts[1] if len(parts) > 1 else None
                    if tenant_id:
                        admin.activate_tenant(tenant_id)
                    continue
                
                if command.startswith('upgrade '):
                    parts = command.split(' ')
                    tenant_id = parts[1] if len(parts) > 1 else None
                    plan = parts[2] if len(parts) > 2 else 'starter'
                    if tenant_id:
                        admin.upgrade_tenant(tenant_id, plan)
                    continue
                
                if command.startswith('invoice '):
                    parts = command.split(' ')
                    tenant_id = parts[1] if len(parts) > 1 else None
                    if tenant_id:
                        admin.generate_invoice(tenant_id)
                    continue
                
                if command.startswith('set-limit '):
                    parts = command.split(' ')
                    tenant_id = parts[1] if len(parts) > 1 else None
                    limit = int(parts[2]) if len(parts) > 2 else 100000
                    if tenant_id:
                        admin.set_tenant_limit(tenant_id, limit)
                    continue
                
                if command.startswith('add-bonus '):
                    parts = command.split(' ')
                    tenant_id = parts[1] if len(parts) > 1 else None
                    bonus = int(parts[2]) if len(parts) > 2 else 10000
                    if tenant_id:
                        admin.add_bonus_tokens(tenant_id, bonus)
                    continue
                
                if command == 'maintenance on':
                    admin.enable_maintenance_mode()
                    continue
                
                if command == 'maintenance off':
                    admin.disable_maintenance_mode()
                    continue
                
                if command == 'testing on':
                    admin.toggle_testing_mode()
                    continue
                
                print(f"Unknown command: {command}")
                print("Type 'help' for available commands")
                
            except KeyboardInterrupt:
                print("\nExiting admin panel...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    else:
        # Command line mode
        command = sys.argv[1]
        
        if command == 'list':
            admin.list_all_tenants()
        
        elif command == 'report':
            admin.platform_report()
        
        elif command == 'top-users':
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            admin.top_users_report(limit)
        
        elif command == 'suspend':
            if len(sys.argv) < 3:
                print("Usage: python admin_panel.py suspend <tenant_id> [reason]")
                sys.exit(1)
            tenant_id = sys.argv[2]
            reason = sys.argv[3] if len(sys.argv) > 3 else "No reason"
            admin.suspend_tenant(tenant_id, reason)
        
        elif command == 'activate':
            if len(sys.argv) < 3:
                print("Usage: python admin_panel.py activate <tenant_id>")
                sys.exit(1)
            admin.activate_tenant(sys.argv[2])
        
        elif command == 'upgrade':
            if len(sys.argv) < 4:
                print("Usage: python admin_panel.py upgrade <tenant_id> <plan>")
                sys.exit(1)
            admin.upgrade_tenant(sys.argv[2], sys.argv[3])
        
        elif command == 'invoice':
            if len(sys.argv) < 3:
                print("Usage: python admin_panel.py invoice <tenant_id>")
                sys.exit(1)
            admin.generate_invoice(sys.argv[2])
        
        elif command == 'help':
            admin.show_admin_commands()
        
        else:
            print(f"Unknown command: {command}")
            print("Run 'python admin_panel.py help' for available commands")
            sys.exit(1)


if __name__ == "__main__":
    main()
