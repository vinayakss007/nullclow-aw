#!/usr/bin/env python3
"""
Additional Agents for Multi-Agent Platform
Finance, Marketing, Legal, Operations, IT, E-commerce, and more
"""

# ============================================
# ADDITIONAL AGENTS (6 More)
# ============================================

ADDITIONAL_AGENTS = {
    
    # ==================== FINANCE AGENT ====================
    "finance": {
        "name": "Finance & Accounting Agent",
        "description": "Handle invoices, expenses, financial reports, and bookkeeping",
        "tools": ["file_read", "file_write", "http_request", "browser"],
        "sub_agents": [
            "invoice_generator",
            "expense_tracker",
            "financial_reporter",
            "tax_calculator",
            "budget_analyzer"
        ],
        "prompt": "You are a finance expert. Handle invoicing, expense tracking, financial reporting, tax calculations, and budget analysis. Always ensure accuracy and compliance."
    },
    
    # ==================== MARKETING AGENT ====================
    "marketing": {
        "name": "Marketing Campaign Agent",
        "description": "Create and manage marketing campaigns, ads, and analytics",
        "tools": ["browser", "http_request", "file_write"],
        "sub_agents": [
            "campaign_planner",
            "ad_copy_writer",
            "audience_researcher",
            "analytics_reporter",
            "competitor_analyzer"
        ],
        "prompt": "You are a marketing expert. Plan campaigns, write ad copy, research audiences, analyze performance, and track competitors."
    },
    
    # ==================== LEGAL AGENT ====================
    "legal": {
        "name": "Legal Document Agent",
        "description": "Draft contracts, NDAs, terms of service, and legal summaries",
        "tools": ["file_read", "file_write", "browser"],
        "sub_agents": [
            "contract_drafter",
            "nda_generator",
            "terms_writer",
            "legal_researcher",
            "compliance_checker"
        ],
        "prompt": "You are a legal assistant. Draft contracts, NDAs, terms of service, research legal topics, and check compliance. Always include disclaimer that this is not legal advice."
    },
    
    # ==================== OPERATIONS AGENT ====================
    "operations": {
        "name": "Operations Management Agent",
        "description": "Manage workflows, SOPs, inventory, and process optimization",
        "tools": ["file_read", "file_write", "schedule", "memory_store"],
        "sub_agents": [
            "workflow_designer",
            "sop_writer",
            "inventory_tracker",
            "process_optimizer",
            "vendor_manager"
        ],
        "prompt": "You are an operations expert. Design workflows, write SOPs, track inventory, optimize processes, and manage vendor relationships."
    },
    
    # ==================== IT/DEVOPS AGENT ====================
    "it_devops": {
        "name": "IT & DevOps Agent",
        "description": "Handle server monitoring, deployments, troubleshooting, and IT support",
        "tools": ["shell", "http_request", "browser", "schedule"],
        "sub_agents": [
            "server_monitor",
            "deployment_manager",
            "troubleshooter",
            "security_auditor",
            "backup_manager"
        ],
        "prompt": "You are an IT/DevOps expert. Monitor servers, manage deployments, troubleshoot issues, audit security, and manage backups."
    },
    
    # ==================== E-COMMERCE AGENT ====================
    "ecommerce": {
        "name": "E-commerce Agent",
        "description": "Manage product listings, orders, customer reviews, and inventory",
        "tools": ["browser", "http_request", "file_write", "memory_store"],
        "sub_agents": [
            "product_lister",
            "order_processor",
            "review_manager",
            "pricing_optimizer",
            "inventory_sync"
        ],
        "prompt": "You are an e-commerce expert. Manage product listings, process orders, handle reviews, optimize pricing, and sync inventory across platforms."
    },
    
    # ==================== REAL ESTATE AGENT ====================
    "real_estate": {
        "name": "Real Estate Agent",
        "description": "Property listings, valuations, client matching, and market analysis",
        "tools": ["browser", "http_request", "file_write"],
        "sub_agents": [
            "property_lister",
            "valuation_expert",
            "client_matcher",
            "market_analyst",
            "document_processor"
        ],
        "prompt": "You are a real estate expert. List properties, provide valuations, match clients to properties, analyze markets, and process documents."
    },
    
    # ==================== HEALTHCARE AGENT ====================
    "healthcare": {
        "name": "Healthcare Assistant Agent",
        "description": "Appointment scheduling, patient records, medical research (not diagnosis)",
        "tools": ["schedule", "file_read", "file_write", "browser"],
        "sub_agents": [
            "appointment_scheduler",
            "records_manager",
            "medical_researcher",
            "insurance_processor",
            "reminder_manager"
        ],
        "prompt": "You are a healthcare assistant. Schedule appointments, manage records, research medical topics, process insurance. IMPORTANT: Never provide medical diagnoses - always refer to licensed professionals."
    },
    
    # ==================== EDUCATION AGENT ====================
    "education": {
        "name": "Education & Training Agent",
        "description": "Create courses, quizzes, lesson plans, and track student progress",
        "tools": ["file_write", "memory_store", "schedule"],
        "sub_agents": [
            "course_creator",
            "quiz_generator",
            "lesson_planner",
            "progress_tracker",
            "certificate_generator"
        ],
        "prompt": "You are an education expert. Create courses, generate quizzes, plan lessons, track student progress, and generate certificates."
    },
    
    # ==================== RECRUITMENT AGENT ====================
    "recruitment": {
        "name": "Recruitment & Hiring Agent",
        "description": "Job postings, candidate sourcing, interview scheduling, onboarding",
        "tools": ["browser", "http_request", "schedule", "file_write"],
        "sub_agents": [
            "job_poster",
            "candidate_sourcer",
            "interview_scheduler",
            "onboarding_coordinator",
            "reference_checker"
        ],
        "prompt": "You are a recruitment expert. Post jobs, source candidates, schedule interviews, coordinate onboarding, and check references."
    },
    
    # ==================== SOCIAL MEDIA AGENT ====================
    "social_media": {
        "name": "Social Media Management Agent",
        "description": "Post scheduling, engagement tracking, content creation, analytics",
        "tools": ["browser", "http_request", "schedule", "file_write"],
        "sub_agents": [
            "content_creator",
            "post_scheduler",
            "engagement_tracker",
            "hashtag_researcher",
            "analytics_reporter"
        ],
        "prompt": "You are a social media expert. Create content, schedule posts, track engagement, research hashtags, and report analytics across platforms."
    },
    
    # ==================== DATA ANALYSIS AGENT ====================
    "data_analysis": {
        "name": "Data Analysis Agent",
        "description": "Analyze datasets, generate insights, create visualizations, reports",
        "tools": ["file_read", "shell", "http_request"],
        "sub_agents": [
            "data_cleaner",
            "insight_generator",
            "visualization_creator",
            "statistical_analyst",
            "report_writer"
        ],
        "prompt": "You are a data analyst. Clean data, generate insights, create visualizations, perform statistical analysis, and write reports."
    },
    
    # ==================== TRANSLATION AGENT ====================
    "translation": {
        "name": "Translation & Localization Agent",
        "description": "Translate content, localize for regions, proofread translations",
        "tools": ["file_read", "file_write", "browser"],
        "sub_agents": [
            "document_translator",
            "website_localizer",
            "proofreader",
            "cultural_advisor",
            "terminology_manager"
        ],
        "prompt": "You are a translation expert. Translate documents, localize websites, proofread translations, advise on cultural nuances, and manage terminology."
    },
    
    # ==================== VIDEO AGENT ====================
    "video": {
        "name": "Video Production Agent",
        "description": "Script writing, video editing plans, thumbnail creation, optimization",
        "tools": ["file_write", "browser", "http_request"],
        "sub_agents": [
            "script_writer",
            "editing_planner",
            "thumbnail_designer",
            "seo_optimizer",
            "analytics_tracker"
        ],
        "prompt": "You are a video production expert. Write scripts, plan edits, design thumbnails, optimize for SEO, and track video analytics."
    },
    
    # ==================== PODCAST AGENT ====================
    "podcast": {
        "name": "Podcast Production Agent",
        "description": "Episode planning, guest coordination, show notes, distribution",
        "tools": ["schedule", "file_write", "browser"],
        "sub_agents": [
            "episode_planner",
            "guest_coordinator",
            "show_notes_writer",
            "distribution_manager",
            "promotion_manager"
        ],
        "prompt": "You are a podcast production expert. Plan episodes, coordinate guests, write show notes, manage distribution, and handle promotion."
    }
}

# ============================================
# ADDITIONAL SUB-AGENT DEFINITIONS
# ============================================

ADDITIONAL_SUB_AGENTS = {
    # Finance sub-agents
    "invoice_generator": {
        "parent": "finance",
        "task": "Generate professional invoices with line items, taxes, and payment terms",
        "output_format": "PDF-ready invoice with all details"
    },
    "expense_tracker": {
        "parent": "finance",
        "task": "Categorize and track business expenses",
        "output_format": "Categorized expense report with totals"
    },
    "financial_reporter": {
        "parent": "finance",
        "task": "Generate P&L, balance sheet, cash flow statements",
        "output_format": "Financial statements in standard format"
    },
    "tax_calculator": {
        "parent": "finance",
        "task": "Calculate estimated taxes based on income and expenses",
        "output_format": "Tax estimate with breakdown by category"
    },
    "budget_analyzer": {
        "parent": "finance",
        "task": "Analyze budgets vs actual spending, identify variances",
        "output_format": "Budget analysis report with recommendations"
    },
    
    # Marketing sub-agents
    "campaign_planner": {
        "parent": "marketing",
        "task": "Create comprehensive marketing campaign plans",
        "output_format": "Campaign plan with timeline, channels, budget"
    },
    "ad_copy_writer": {
        "parent": "marketing",
        "task": "Write compelling ad copy for various platforms",
        "output_format": "Ad variations for Google, Facebook, LinkedIn"
    },
    "audience_researcher": {
        "parent": "marketing",
        "task": "Research target audiences and create personas",
        "output_format": "Detailed audience personas with demographics"
    },
    "analytics_reporter": {
        "parent": "marketing",
        "task": "Analyze campaign performance and create reports",
        "output_format": "Performance report with KPIs and insights"
    },
    "competitor_analyzer": {
        "parent": "marketing",
        "task": "Analyze competitor strategies and positioning",
        "output_format": "Competitor analysis with SWOT"
    },
    
    # Legal sub-agents
    "contract_drafter": {
        "parent": "legal",
        "task": "Draft standard business contracts",
        "output_format": "Contract template with customizable fields"
    },
    "nda_generator": {
        "parent": "legal",
        "task": "Generate Non-Disclosure Agreements",
        "output_format": "NDA template (mutual or one-way)"
    },
    "terms_writer": {
        "parent": "legal",
        "task": "Write Terms of Service and Privacy Policies",
        "output_format": "ToS and Privacy Policy documents"
    },
    "legal_researcher": {
        "parent": "legal",
        "task": "Research legal topics and regulations",
        "output_format": "Legal research summary with sources"
    },
    "compliance_checker": {
        "parent": "legal",
        "task": "Check compliance with regulations (GDPR, CCPA, etc.)",
        "output_format": "Compliance checklist with gaps"
    },
    
    # Operations sub-agents
    "workflow_designer": {
        "parent": "operations",
        "task": "Design business workflows and process maps",
        "output_format": "Workflow diagram description and steps"
    },
    "sop_writer": {
        "parent": "operations",
        "task": "Write Standard Operating Procedures",
        "output_format": "SOP document with steps and checklists"
    },
    "inventory_tracker": {
        "parent": "operations",
        "task": "Track inventory levels and generate alerts",
        "output_format": "Inventory report with reorder alerts"
    },
    "process_optimizer": {
        "parent": "operations",
        "task": "Analyze and optimize business processes",
        "output_format": "Optimization recommendations with ROI"
    },
    "vendor_manager": {
        "parent": "operations",
        "task": "Manage vendor relationships and contracts",
        "output_format": "Vendor comparison and recommendations"
    },
    
    # IT/DevOps sub-agents
    "server_monitor": {
        "parent": "it_devops",
        "task": "Monitor server health and performance",
        "output_format": "Server status report with alerts"
    },
    "deployment_manager": {
        "parent": "it_devops",
        "task": "Manage application deployments",
        "output_format": "Deployment plan and checklist"
    },
    "troubleshooter": {
        "parent": "it_devops",
        "task": "Diagnose and troubleshoot IT issues",
        "output_format": "Diagnosis and step-by-step fix guide"
    },
    "security_auditor": {
        "parent": "it_devops",
        "task": "Audit security configurations and practices",
        "output_format": "Security audit report with recommendations"
    },
    "backup_manager": {
        "parent": "it_devops",
        "task": "Manage backup schedules and verify integrity",
        "output_format": "Backup status report"
    },
    
    # E-commerce sub-agents
    "product_lister": {
        "parent": "ecommerce",
        "task": "Create product listings with descriptions and SEO",
        "output_format": "Product listing optimized for marketplace"
    },
    "order_processor": {
        "parent": "ecommerce",
        "task": "Process orders and generate shipping labels",
        "output_format": "Order confirmation and shipping details"
    },
    "review_manager": {
        "parent": "ecommerce",
        "task": "Monitor and respond to customer reviews",
        "output_format": "Review responses and sentiment analysis"
    },
    "pricing_optimizer": {
        "parent": "ecommerce",
        "task": "Optimize pricing based on competition and demand",
        "output_format": "Pricing recommendations with rationale"
    },
    "inventory_sync": {
        "parent": "ecommerce",
        "task": "Sync inventory across multiple channels",
        "output_format": "Inventory sync report"
    },
    
    # Real Estate sub-agents
    "property_lister": {
        "parent": "real_estate",
        "task": "Create property listings with descriptions",
        "output_format": "Property listing with features and photos"
    },
    "valuation_expert": {
        "parent": "real_estate",
        "task": "Provide property valuations based on comparables",
        "output_format": "Valuation report with comparables"
    },
    "client_matcher": {
        "parent": "real_estate",
        "task": "Match clients to suitable properties",
        "output_format": "Property recommendations with match scores"
    },
    "market_analyst": {
        "parent": "real_estate",
        "task": "Analyze real estate market trends",
        "output_format": "Market analysis report"
    },
    "document_processor": {
        "parent": "real_estate",
        "task": "Process real estate documents and forms",
        "output_format": "Completed forms and checklists"
    },
    
    # Healthcare sub-agents
    "appointment_scheduler": {
        "parent": "healthcare",
        "task": "Schedule patient appointments",
        "output_format": "Appointment confirmation with details"
    },
    "records_manager": {
        "parent": "healthcare",
        "task": "Organize and manage patient records",
        "output_format": "Patient record summary"
    },
    "medical_researcher": {
        "parent": "healthcare",
        "task": "Research medical topics and studies",
        "output_format": "Research summary with citations"
    },
    "insurance_processor": {
        "parent": "healthcare",
        "task": "Process insurance claims and verify coverage",
        "output_format": "Insurance verification result"
    },
    "reminder_manager": {
        "parent": "healthcare",
        "task": "Send medication and appointment reminders",
        "output_format": "Reminder messages"
    },
    
    # Education sub-agents
    "course_creator": {
        "parent": "education",
        "task": "Create online course curricula",
        "output_format": "Course outline with modules and lessons"
    },
    "quiz_generator": {
        "parent": "education",
        "task": "Generate quizzes and assessments",
        "output_format": "Quiz with questions and answer key"
    },
    "lesson_planner": {
        "parent": "education",
        "task": "Create detailed lesson plans",
        "output_format": "Lesson plan with objectives and activities"
    },
    "progress_tracker": {
        "parent": "education",
        "task": "Track student progress and grades",
        "output_format": "Progress report with grades"
    },
    "certificate_generator": {
        "parent": "education",
        "task": "Generate completion certificates",
        "output_format": "Certificate template with details"
    },
    
    # Recruitment sub-agents
    "job_poster": {
        "parent": "recruitment",
        "task": "Create and post job listings",
        "output_format": "Job description optimized for platforms"
    },
    "candidate_sourcer": {
        "parent": "recruitment",
        "task": "Source candidates from various channels",
        "output_format": "Candidate list with profiles"
    },
    "interview_scheduler": {
        "parent": "recruitment",
        "task": "Schedule interviews between candidates and hiring managers",
        "output_format": "Interview schedule with details"
    },
    "onboarding_coordinator": {
        "parent": "recruitment",
        "task": "Coordinate new hire onboarding",
        "output_format": "Onboarding checklist and schedule"
    },
    "reference_checker": {
        "parent": "recruitment",
        "task": "Check candidate references",
        "output_format": "Reference check summary"
    },
    
    # Social Media sub-agents
    "content_creator": {
        "parent": "social_media",
        "task": "Create social media content",
        "output_format": "Content calendar with posts"
    },
    "post_scheduler": {
        "parent": "social_media",
        "task": "Schedule posts across platforms",
        "output_format": "Scheduled posts with timestamps"
    },
    "engagement_tracker": {
        "parent": "social_media",
        "task": "Track engagement metrics",
        "output_format": "Engagement report with insights"
    },
    "hashtag_researcher": {
        "parent": "social_media",
        "task": "Research trending and relevant hashtags",
        "output_format": "Hashtag list with performance data"
    },
    "analytics_reporter": {
        "parent": "social_media",
        "task": "Generate social media analytics reports",
        "output_format": "Analytics dashboard summary"
    },
    
    # Data Analysis sub-agents
    "data_cleaner": {
        "parent": "data_analysis",
        "task": "Clean and preprocess datasets",
        "output_format": "Cleaned dataset with documentation"
    },
    "insight_generator": {
        "parent": "data_analysis",
        "task": "Generate insights from data analysis",
        "output_format": "Insights report with key findings"
    },
    "visualization_creator": {
        "parent": "data_analysis",
        "task": "Create data visualizations",
        "output_format": "Charts and graphs with descriptions"
    },
    "statistical_analyst": {
        "parent": "data_analysis",
        "task": "Perform statistical analysis",
        "output_format": "Statistical analysis report"
    },
    "report_writer": {
        "parent": "data_analysis",
        "task": "Write comprehensive data reports",
        "output_format": "Full analysis report with executive summary"
    },
    
    # Translation sub-agents
    "document_translator": {
        "parent": "translation",
        "task": "Translate documents between languages",
        "output_format": "Translated document"
    },
    "website_localizer": {
        "parent": "translation",
        "task": "Localize websites for different regions",
        "output_format": "Localized content with cultural adaptations"
    },
    "proofreader": {
        "parent": "translation",
        "task": "Proofread translations for accuracy",
        "output_format": "Proofread document with corrections"
    },
    "cultural_advisor": {
        "parent": "translation",
        "task": "Advise on cultural nuances and sensitivities",
        "output_format": "Cultural adaptation recommendations"
    },
    "terminology_manager": {
        "parent": "translation",
        "task": "Manage terminology glossaries",
        "output_format": "Terminology glossary"
    },
    
    # Video sub-agents
    "script_writer": {
        "parent": "video",
        "task": "Write video scripts",
        "output_format": "Video script with scenes and dialogue"
    },
    "editing_planner": {
        "parent": "video",
        "task": "Plan video editing workflow",
        "output_format": "Editing plan with timeline"
    },
    "thumbnail_designer": {
        "parent": "video",
        "task": "Design video thumbnails",
        "output_format": "Thumbnail concepts and descriptions"
    },
    "seo_optimizer": {
        "parent": "video",
        "task": "Optimize videos for search",
        "output_format": "SEO-optimized titles, descriptions, tags"
    },
    "analytics_tracker": {
        "parent": "video",
        "task": "Track video performance analytics",
        "output_format": "Analytics report with insights"
    },
    
    # Podcast sub-agents
    "episode_planner": {
        "parent": "podcast",
        "task": "Plan podcast episodes",
        "output_format": "Episode outline with topics"
    },
    "guest_coordinator": {
        "parent": "podcast",
        "task": "Coordinate podcast guests",
        "output_format": "Guest schedule and briefing"
    },
    "show_notes_writer": {
        "parent": "podcast",
        "task": "Write podcast show notes",
        "output_format": "Show notes with timestamps and links"
    },
    "distribution_manager": {
        "parent": "podcast",
        "task": "Manage podcast distribution",
        "output_format": "Distribution checklist"
    },
    "promotion_manager": {
        "parent": "podcast",
        "task": "Promote podcast episodes",
        "output_format": "Promotion plan and content"
    }
}

# ============================================
# EXPORT FOR AGENTS_PLATFORM.PY
# ============================================

def get_all_agents():
    """Merge with base agents"""
    from agents_platform import AGENTS, SUB_AGENTS
    
    all_agents = {**AGENTS, **ADDITIONAL_AGENTS}
    all_sub_agents = {**SUB_AGENTS, **ADDITIONAL_SUB_AGENTS}
    
    return all_agents, all_sub_agents

# Print summary
if __name__ == "__main__":
    print("\n📋 Additional Agents Added:\n")
    
    for key, agent in ADDITIONAL_AGENTS.items():
        print(f"🤖 {agent['name']} ({key})")
        print(f"   Sub-Agents: {len(agent['sub_agents'])}")
        print()
    
    print(f"\n✅ Total Additional Agents: {len(ADDITIONAL_AGENTS)}")
    print(f"✅ Total Additional Sub-Agents: {len(ADDITIONAL_SUB_AGENTS)}")
