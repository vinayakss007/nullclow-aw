#!/usr/bin/env python3
"""
Nullclaw Integration Guide
Connect Multi-Agent Platform to Nullclaw + Telegram
"""

"""
INTEGRATION ARCHITECTURE:

Telegram Message
      │
      ▼
Nullclaw (Telegram Channel)
      │
      ▼
This Integration Layer
      │
      ├─→ Route to Agent
      │
      ▼
Agent Platform
      │
      ├─→ Select Sub-Agent
      │
      ▼
Nullclaw (AI + Tools)
      │
      ▼
Response to Telegram
"""

# ============================================
# INTEGRATION CODE
# ============================================

import subprocess
import json
from pathlib import Path

class NullclawIntegration:
    """
    Integrate Multi-Agent Platform with Nullclaw
    """
    
    def __init__(self, tenant_id: str, workspace: str = None):
        self.tenant_id = tenant_id
        self.workspace = workspace or f"./customers/{tenant_id}/workspace"
        self.nullclaw_config = f"./customers/{tenant_id}/nullclaw_config.json"
    
    def send_to_nullclaw(self, message: str) -> str:
        """
        Send message to Nullclaw agent and get response
        
        Args:
            message: User message from Telegram
        
        Returns:
            Response from Nullclaw
        """
        # Ensure workspace exists
        Path(self.workspace).mkdir(parents=True, exist_ok=True)
        
        # Write message to workspace
        message_file = Path(self.workspace) / "incoming_message.txt"
        with open(message_file, 'w') as f:
            f.write(message)
        
        # Call Nullclaw CLI
        try:
            result = subprocess.run(
                ['nullclaw', 'agent', '-m', message],
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            response = result.stdout
            
            # Save response
            response_file = Path(self.workspace) / "outgoing_response.txt"
            with open(response_file, 'w') as f:
                f.write(response)
            
            return response
        
        except subprocess.TimeoutExpired:
            return "⏱️ Task is taking longer than expected. Please wait..."
        
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def route_task(self, task_description: str, input_data: str = "") -> dict:
        """
        Route task to appropriate agent using agents_platform.py
        
        Args:
            task_description: What the user wants
            input_data: Additional context/data
        
        Returns:
            Routing result with agent, sub_agent, task_id
        """
        result = subprocess.run(
            ['python3', 'agents_platform.py', 'route', self.tenant_id, task_description],
            capture_output=True,
            text=True
        )
        
        # Parse output (simplified - in production use JSON)
        output = result.stdout
        
        return {
            'output': output,
            'task_description': task_description
        }
    
    def execute_agent_task(self, agent_type: str, sub_agent: str, 
                          task: str, input_data: str = "") -> str:
        """
        Execute specific agent task via Nullclaw
        
        Args:
            agent_type: Main agent (sales, hr, etc.)
            sub_agent: Sub-agent (lead_scorer, etc.)
            task: Task description
            input_data: Data to process
        
        Returns:
            Result from agent execution
        """
        # Get sub-agent task definition
        from agents_extended import ADDITIONAL_SUB_AGENTS
        from agents_platform import SUB_AGENTS
        
        all_sub_agents = {**SUB_AGENTS, **ADDITIONAL_SUB_AGENTS}
        
        if sub_agent not in all_sub_agents:
            return f"❌ Unknown sub-agent: {sub_agent}"
        
        sub_agent_def = all_sub_agents[sub_agent]
        
        # Build prompt for Nullclaw
        prompt = f"""
{sub_agent_def['task']}

Task: {task}
Input: {input_data}

Output Format: {sub_agent_def['output_format']}

Please execute this task carefully and provide the output in the specified format.
"""
        
        # Send to Nullclaw
        response = self.send_to_nullclaw(prompt)
        
        return response
    
    def track_usage(self, tokens_used: int, agent_type: str, sub_agent: str):
        """
        Track token usage for this tenant
        
        Args:
            tokens_used: Number of tokens consumed
            agent_type: Which agent was used
            sub_agent: Which sub-agent was used
        """
        subprocess.run(
            ['python3', 'usage_tracker.py', 'record', 
             self.tenant_id, str(tokens_used), 
             'nullclaw-agent', f"{agent_type}/{sub_agent}"],
            capture_output=True
        )
    
    def check_limits(self) -> bool:
        """
        Check if tenant has exceeded usage limits
        
        Returns:
            True if within limits, False if exceeded
        """
        tenant_manager = __import__('tenant_manager')
        manager = tenant_manager.TenantManager()
        
        tenant = manager.get_tenant(self.tenant_id)
        if not tenant:
            return False
        
        # Would need to integrate with usage_tracker for real check
        # Simplified for now
        return True


# ============================================
# TELEGRAM BOT INTEGRATION
# ============================================

class TelegramBotIntegration:
    """
    Connect Telegram Bot to Multi-Agent Platform
    """
    
    def __init__(self, bot_token: str, tenant_id: str):
        self.bot_token = bot_token
        self.tenant_id = tenant_id
        self.nullclaw = NullclawIntegration(tenant_id)
        
        # Note: python-telegram-bot library would be used here
        # For now, showing the integration pattern
    
    async def handle_message(self, message: str, chat_id: int) -> str:
        """
        Handle incoming Telegram message
        
        Args:
            message: User message
            chat_id: Telegram chat ID
        
        Returns:
            Response to send back
        """
        # Step 1: Route task to agent
        routing = self.nullclaw.route_task(message)
        
        # Step 2: Execute via Nullclaw
        response = self.nullclaw.send_to_nullclaw(message)
        
        # Step 3: Track usage (estimate tokens)
        estimated_tokens = len(message) // 4  # Rough estimate
        self.nullclaw.track_usage(estimated_tokens, "auto", "auto")
        
        return response
    
    async def send_response(self, chat_id: int, response: str):
        """
        Send response back to Telegram
        
        Args:
            chat_id: Telegram chat ID
            response: Message to send
        """
        # Would use python-telegram-bot here:
        # await context.bot.send_message(chat_id=chat_id, text=response)
        pass


# ============================================
# USAGE EXAMPLES
# ============================================

"""
# Example 1: Simple Integration

integration = NullclawIntegration("tenant_001")

# User sends message via Telegram
message = "Score this sales lead: Budget $50k, decision maker available"

# Route to agent
routing = integration.route_task(message)
print(routing)

# Execute
response = integration.send_to_nullclaw(message)
print(response)

# Track
integration.track_usage(1500, "sales", "lead_scorer")


# Example 2: Specific Agent Task

integration = NullclawIntegration("tenant_001")

result = integration.execute_agent_task(
    agent_type="sales",
    sub_agent="lead_scorer",
    task="Score this lead",
    input_data="Budget: $50k, Timeline: 2 weeks, Need: Website redesign"
)

print(result)


# Example 3: Telegram Bot

# bot = TelegramBotIntegration(bot_token="123456:ABC-DEF", tenant_id="tenant_001")
# await bot.handle_message("Hello", chat_id=123456)
"""


# ============================================
# MAIN TEST FUNCTION
# ============================================

def main():
    import sys
    
    print("Nullclaw Integration Test")
    print("=" * 50)
    
    if len(sys.argv) < 3:
        print("\nUsage:")
        print("  python nullclaw_integration.py <tenant_id> <message>")
        print("\nExample:")
        print("  python nullclaw_integration.py tenant_001 'Score this lead: Budget $10k'")
        sys.exit(0)
    
    tenant_id = sys.argv[1]
    message = " ".join(sys.argv[2:])
    
    # Test integration
    integration = NullclawIntegration(tenant_id)
    
    print(f"\n📨 Message: {message}")
    print(f"🏢 Tenant: {tenant_id}")
    
    # Route
    print("\n🔀 Routing task...")
    routing = integration.route_task(message)
    print(routing['output'])
    
    # Execute
    print("\n🤖 Executing via Nullclaw...")
    response = integration.send_to_nullclaw(message)
    print(f"\n💬 Response:\n{response}")
    
    print("\n✅ Integration test complete!")


if __name__ == "__main__":
    main()
