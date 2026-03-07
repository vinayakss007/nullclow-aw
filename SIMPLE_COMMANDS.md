# Simple Telegram Bot Commands
# No agents yet - just direct functions

"""
Usage:
    /start - Start bot
    /search <query> - Search internet
    /summarize <text> - Summarize text
    /seo <topic> - Generate SEO keywords
    /blog <topic> - Generate blog outline
"""

# Example commands for your bot:

# Search
/search latest AI news

# SEO
SEO keywords for bakery website

# Blog
Blog outline about digital marketing

# Summarize
Summarize: [paste long text]

# Lead Score
Score this lead: Budget $10k, Timeline 1 month, Need: website

---

## Simple Implementation (No Agents)

```python
# commands.py - Simple functions, no agents

def seo_keywords(topic):
    """Generate SEO keywords"""
    prompt = f"Generate 10 SEO keywords for: {topic}"
    return call_ai(prompt)

def blog_outline(topic):
    """Generate blog outline"""
    prompt = f"Create blog outline for: {topic}"
    return call_ai(prompt)

def score_lead(lead_data):
    """Score sales lead 0-100"""
    prompt = f"Score this lead 0-100: {lead_data}"
    return call_ai(prompt)

# That's it! No agent loop needed for MVP.
```

---

## When to Add Agents Later

Add NullClaw agents when you need:

- ✅ Multi-step reasoning (search → read → summarize)
- ✅ Tool automation (API calls, file operations)
- ✅ Memory across conversations
- ✅ Multiple specialized bots

**For now:** Simple commands work fine!
