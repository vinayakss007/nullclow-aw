#!/usr/bin/env python3
"""
Multi-Agent Platform with Task Assignment
Create agents, sub-agents, and assign tasks automatically
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# ============================================
# AGENT REGISTRY - Define all available agents
# ============================================

AGENTS = {
    "sales": {
        "name": "Sales Lead Agent",
        "description": "Score and qualify sales leads",
        "tools": ["browser", "http_request", "memory_store"],
        "sub_agents": ["lead_scorer", "email_writer", "crm_updater"],
        "prompt": "You are a sales expert. Score leads, generate outreach emails, and manage CRM."
    },
    
    "hr": {
        "name": "HR Screening Agent",
        "description": "Screen resumes and rank candidates",
        "tools": ["file_read", "memory_store"],
        "sub_agents": ["resume_screener", "question_generator", "ranker"],
        "prompt": "You are an HR expert. Screen resumes, generate interview questions, rank candidates."
    },
    
    "support": {
        "name": "Customer Support Agent",
        "description": "Handle customer support tickets",
        "tools": ["browser", "memory_recall", "memory_store"],
        "sub_agents": ["ticket_classifier", "response_generator", "escalation_handler"],
        "prompt": "You are a support expert. Classify tickets, generate responses, escalate when needed."
    },
    
    "research": {
        "name": "Research Agent",
        "description": "Research topics and summarize findings",
        "tools": ["browser", "http_request"],
        "sub_agents": ["searcher", "summarizer", "citation_manager"],
        "prompt": "You are a researcher. Search web, read sources, summarize findings with citations."
    },
    
    "content": {
        "name": "Content Agent",
        "description": "Create content (blogs, social media, SEO)",
        "tools": ["browser", "file_write"],
        "sub_agents": ["seo_analyzer", "blog_writer", "social_media_manager"],
        "prompt": "You are a content expert. Generate SEO content, blogs, and social media posts."
    },
    
    "office": {
        "name": "Office Assistant Agent",
        "description": "General office tasks and scheduling",
        "tools": ["schedule", "memory_store", "shell"],
        "sub_agents": ["scheduler", "note_taker", "reminder_manager"],
        "prompt": "You are an office assistant. Schedule meetings, take notes, set reminders."
    }
}

# ============================================
# SUB-AGENT DEFINITIONS
# ============================================

SUB_AGENTS = {
    # Sales sub-agents
    "lead_scorer": {
        "parent": "sales",
        "task": "Score leads from 0-100 based on budget, timeline, need, and decision-maker access",
        "output_format": "JSON: {score: number, reasoning: string, next_action: string}"
    },
    
    "email_writer": {
        "parent": "sales",
        "task": "Write personalized outreach emails based on lead data",
        "output_format": "Email draft with subject line and body"
    },
    
    "crm_updater": {
        "parent": "sales",
        "task": "Format lead data for CRM import",
        "output_format": "CSV or JSON formatted for CRM"
    },
    
    # HR sub-agents
    "resume_screener": {
        "parent": "hr",
        "task": "Screen resumes against job description, score match 0-100",
        "output_format": "JSON: {score: number, strengths: [], gaps: [], recommendation: string}"
    },
    
    "question_generator": {
        "parent": "hr",
        "task": "Generate interview questions based on resume and job requirements",
        "output_format": "List of 5-10 targeted interview questions"
    },
    
    "ranker": {
        "parent": "hr",
        "task": "Rank all candidates for a position",
        "output_format": "Ranked list with scores and reasoning"
    },
    
    # Support sub-agents
    "ticket_classifier": {
        "parent": "support",
        "task": "Classify support tickets by urgency and category",
        "output_format": "JSON: {category: string, urgency: low/medium/high, assigned_to: string}"
    },
    
    "response_generator": {
        "parent": "support",
        "task": "Generate helpful support responses",
        "output_format": "Professional support response"
    },
    
    "escalation_handler": {
        "parent": "support",
        "task": "Determine if ticket needs human escalation",
        "output_format": "JSON: {escalate: boolean, reason: string, priority: string}"
    },
    
    # Research sub-agents
    "searcher": {
        "parent": "research",
        "task": "Search web for relevant information on topic",
        "output_format": "List of sources with URLs and key points"
    },
    
    "summarizer": {
        "parent": "research",
        "task": "Summarize research findings into concise report",
        "output_format": "Structured summary with key findings"
    },
    
    "citation_manager": {
        "parent": "research",
        "task": "Manage citations and sources",
        "output_format": "Formatted bibliography with links"
    },
    
    # Content sub-agents
    "seo_analyzer": {
        "parent": "content",
        "task": "Analyze and generate SEO keywords and recommendations",
        "output_format": "JSON: {keywords: [], difficulty: string, volume: string, recommendations: []}"
    },
    
    "blog_writer": {
        "parent": "content",
        "task": "Write blog posts with proper structure",
        "output_format": "Blog post with title, headings, and content"
    },
    
    "social_media_manager": {
        "parent": "content",
        "task": "Create social media posts for multiple platforms",
        "output_format": "Posts for Twitter, LinkedIn, Instagram with hashtags"
    },
    
    # Office sub-agents
    "scheduler": {
        "parent": "office",
        "task": "Schedule meetings and manage calendars",
        "output_format": "Calendar event details with time, attendees, agenda"
    },
    
    "note_taker": {
        "parent": "office",
        "task": "Take and organize meeting notes",
        "output_format": "Structured notes with action items"
    },
    
    "reminder_manager": {
        "parent": "office",
        "task": "Set and manage reminders",
        "output_format": "Reminder with time, message, and priority"
    }
}

# ============================================
# TASK MANAGER - Assign and track tasks
# ============================================

class TaskManager:
    def __init__(self, db_path="./tasks.db"):
        self.db = sqlite3.connect(db_path)
        self._create_tables()
    
    def _create_tables(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                tenant_id TEXT,
                agent_type TEXT,
                sub_agent TEXT,
                task_description TEXT,
                status TEXT DEFAULT 'pending',
                input_data TEXT,
                output_data TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                completed_at DATETIME
            )
        """)
        
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS agent_assignments (
                id INTEGER PRIMARY KEY,
                tenant_id TEXT,
                agent_type TEXT,
                sub_agent TEXT,
                task_id INTEGER,
                status TEXT DEFAULT 'active',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.db.commit()
    
    def create_task(self, tenant_id: str, agent_type: str, 
                    task_description: str, input_data: str = "",
                    sub_agent: str = None) -> int:
        """Create a new task"""
        cursor = self.db.execute("""
            INSERT INTO tasks (tenant_id, agent_type, sub_agent, task_description, input_data)
            VALUES (?, ?, ?, ?, ?)
        """, (tenant_id, agent_type, sub_agent, task_description, input_data))
        self.db.commit()
        return cursor.lastrowid
    
    def assign_task(self, task_id: int, agent_type: str, sub_agent: str = None):
        """Assign task to agent/sub-agent"""
        task = self.get_task(task_id)
        tenant_id = task['tenant_id']
        
        self.db.execute("""
            INSERT INTO agent_assignments (tenant_id, agent_type, sub_agent, task_id)
            VALUES (?, ?, ?, ?)
        """, (tenant_id, agent_type, sub_agent, task_id))
        self.db.commit()
    
    def complete_task(self, task_id: int, output_data: str):
        """Mark task as complete"""
        self.db.execute("""
            UPDATE tasks 
            SET status = 'completed', output_data = ?, completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (output_data, task_id))
        self.db.commit()
    
    def get_task(self, task_id: int) -> Dict:
        """Get task by ID"""
        row = self.db.execute("""
            SELECT * FROM tasks WHERE id = ?
        """, (task_id,)).fetchone()
        
        if row:
            return {
                'id': row[0],
                'tenant_id': row[1],
                'agent_type': row[2],
                'sub_agent': row[3],
                'task_description': row[4],
                'status': row[5],
                'input_data': row[6],
                'output_data': row[7],
                'created_at': row[8],
                'completed_at': row[9]
            }
        return None
    
    def get_pending_tasks(self, tenant_id: str = None) -> List[Dict]:
        """Get all pending tasks"""
        query = "SELECT * FROM tasks WHERE status = 'pending'"
        params = []
        
        if tenant_id:
            query += " AND tenant_id = ?"
            params.append(tenant_id)
        
        rows = self.db.execute(query, params).fetchall()
        
        return [{
            'id': row[0],
            'tenant_id': row[1],
            'agent_type': row[2],
            'sub_agent': row[3],
            'task_description': row[4],
            'status': row[5],
            'input_data': row[6],
            'output_data': row[7],
            'created_at': row[8],
            'completed_at': row[9]
        } for row in rows]
    
    def get_agent_tasks(self, agent_type: str, status: str = 'pending') -> List[Dict]:
        """Get tasks for specific agent"""
        rows = self.db.execute("""
            SELECT * FROM tasks 
            WHERE agent_type = ? AND status = ?
        """, (agent_type, status)).fetchall()
        
        return [{
            'id': row[0],
            'tenant_id': row[1],
            'agent_type': row[2],
            'sub_agent': row[3],
            'task_description': row[4],
            'status': row[5],
            'input_data': row[6],
            'output_data': row[7],
            'created_at': row[8],
            'completed_at': row[9]
        } for row in rows]

# ============================================
# AGENT ROUTER - Route tasks to correct agent
# ============================================

class AgentRouter:
    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager
        self.active_agents = {}
    
    def route_task(self, task_description: str, tenant_id: str, 
                   input_data: str = "") -> Dict:
        """
        Analyze task and route to appropriate agent
        Returns: {agent_type, sub_agent, task_id}
        """
        
        # Simple keyword-based routing (can be enhanced with AI)
        task_lower = task_description.lower()
        
        # Sales keywords
        if any(word in task_lower for word in ['lead', 'sales', 'prospect', 'crm', 'outreach']):
            agent_type = 'sales'
            sub_agent = self._select_sales_subagent(task_lower)
        
        # HR keywords
        elif any(word in task_lower for word in ['resume', 'candidate', 'interview', 'hire', 'applicant']):
            agent_type = 'hr'
            sub_agent = self._select_hr_subagent(task_lower)
        
        # Support keywords
        elif any(word in task_lower for word in ['ticket', 'support', 'customer', 'issue', 'complaint']):
            agent_type = 'support'
            sub_agent = self._select_support_subagent(task_lower)
        
        # Research keywords
        elif any(word in task_lower for word in ['research', 'search', 'find', 'investigate', 'study']):
            agent_type = 'research'
            sub_agent = self._select_research_subagent(task_lower)
        
        # Content keywords
        elif any(word in task_lower for word in ['blog', 'seo', 'content', 'post', 'article', 'social']):
            agent_type = 'content'
            sub_agent = self._select_content_subagent(task_lower)
        
        # Office keywords
        elif any(word in task_lower for word in ['schedule', 'meeting', 'reminder', 'note', 'calendar']):
            agent_type = 'office'
            sub_agent = self._select_office_subagent(task_lower)
        
        # Default to research
        else:
            agent_type = 'research'
            sub_agent = 'searcher'
        
        # Create task
        task_id = self.task_manager.create_task(
            tenant_id=tenant_id,
            agent_type=agent_type,
            sub_agent=sub_agent,
            task_description=task_description,
            input_data=input_data
        )
        
        # Assign to agent
        self.task_manager.assign_task(task_id, agent_type, sub_agent)
        
        return {
            'task_id': task_id,
            'agent_type': agent_type,
            'agent_name': AGENTS[agent_type]['name'],
            'sub_agent': sub_agent,
            'sub_agent_task': SUB_AGENTS[sub_agent]['task'] if sub_agent in SUB_AGENTS else None,
            'prompt': AGENTS[agent_type]['prompt']
        }
    
    def _select_sales_subagent(self, task: str) -> str:
        if 'score' in task or 'qualify' in task:
            return 'lead_scorer'
        elif 'email' in task or 'outreach' in task:
            return 'email_writer'
        elif 'crm' in task or 'import' in task:
            return 'crm_updater'
        return 'lead_scorer'
    
    def _select_hr_subagent(self, task: str) -> str:
        if 'screen' in task or 'resume' in task:
            return 'resume_screener'
        elif 'question' in task or 'interview' in task:
            return 'question_generator'
        elif 'rank' in task or 'compare' in task:
            return 'ranker'
        return 'resume_screener'
    
    def _select_support_subagent(self, task: str) -> str:
        if 'classify' in task or 'category' in task:
            return 'ticket_classifier'
        elif 'response' in task or 'reply' in task:
            return 'response_generator'
        elif 'escalat' in task or 'urgent' in task:
            return 'escalation_handler'
        return 'response_generator'
    
    def _select_research_subagent(self, task: str) -> str:
        if 'search' in task or 'find' in task:
            return 'searcher'
        elif 'summarize' in task or 'summary' in task:
            return 'summarizer'
        elif 'citation' in task or 'source' in task:
            return 'citation_manager'
        return 'searcher'
    
    def _select_content_subagent(self, task: str) -> str:
        if 'seo' in task or 'keyword' in task:
            return 'seo_analyzer'
        elif 'blog' in task or 'article' in task:
            return 'blog_writer'
        elif 'social' in task or 'post' in task:
            return 'social_media_manager'
        return 'blog_writer'
    
    def _select_office_subagent(self, task: str) -> str:
        if 'schedule' in task or 'meeting' in task or 'calendar' in task:
            return 'scheduler'
        elif 'note' in task:
            return 'note_taker'
        elif 'remind' in task:
            return 'reminder_manager'
        return 'scheduler'

# ============================================
# CLI - Command Line Interface
# ============================================

def main():
    import sys
    
    task_manager = TaskManager()
    router = AgentRouter(task_manager)
    
    if len(sys.argv) < 2:
        print("Multi-Agent Platform")
        print("\nUsage:")
        print("  python agents_platform.py route <tenant_id> <task>")
        print("  python agents_platform.py list-agents")
        print("  python agents_platform.py list-subagents")
        print("  python agents_platform.py tasks [tenant_id]")
        print("  python agents_platform.py complete <task_id> <output>")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "route":
        if len(sys.argv) < 4:
            print("Usage: python agents_platform.py route <tenant_id> <task description>")
            sys.exit(1)
        
        tenant_id = sys.argv[2]
        task_desc = " ".join(sys.argv[3:])
        
        result = router.route_task(task_desc, tenant_id)
        
        print(f"\n✅ Task Routed Successfully!")
        print(f"   Task ID: {result['task_id']}")
        print(f"   Agent: {result['agent_name']}")
        print(f"   Sub-Agent: {result['sub_agent']}")
        print(f"   Task: {result['sub_agent_task']}")
        print(f"\nPrompt for agent:")
        print(f"   {result['prompt']}")
    
    elif command == "list-agents":
        print("\n📋 Available Agents:\n")
        for key, agent in AGENTS.items():
            print(f"🤖 {agent['name']} ({key})")
            print(f"   Description: {agent['description']}")
            print(f"   Tools: {', '.join(agent['tools'])}")
            print(f"   Sub-Agents: {', '.join(agent['sub_agents'])}")
            print()
    
    elif command == "list-subagents":
        print("\n📋 Available Sub-Agents:\n")
        for key, sub in SUB_AGENTS.items():
            print(f"└─ {key}")
            print(f"   Parent: {sub['parent']}")
            print(f"   Task: {sub['task']}")
            print(f"   Output: {sub['output_format']}")
            print()
    
    elif command == "tasks":
        tenant_id = sys.argv[2] if len(sys.argv) > 2 else None
        tasks = task_manager.get_pending_tasks(tenant_id)
        
        if not tasks:
            print("No pending tasks")
        else:
            print(f"\n📋 Pending Tasks ({len(tasks)}):\n")
            for task in tasks:
                print(f"#{task['id']} - {task['agent_type']}/{task['sub_agent']}")
                print(f"   Task: {task['task_description']}")
                print(f"   Tenant: {task['tenant_id']}")
                print(f"   Created: {task['created_at']}")
                print()
    
    elif command == "complete":
        if len(sys.argv) < 4:
            print("Usage: python agents_platform.py complete <task_id> <output>")
            sys.exit(1)
        
        task_id = int(sys.argv[2])
        output = " ".join(sys.argv[3:])
        
        task_manager.complete_task(task_id, output)
        print(f"✅ Task {task_id} marked as complete")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
