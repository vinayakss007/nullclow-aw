# Telegram Bot Commands Guide

Your bot **@vin11search_bot** has 16+ tools. Here's how to use each:

---

## 🌐 INTERNET SEARCH TOOLS

### 1. Browser Tool (Web Search)
```
Search for latest AI news
Browse https://github.com/nullclaw/nullclaw
What's trending on Hacker News?
Search for Node.js tutorials 2026
```

### 2. HTTP Request (API Calls)
```
Get https://api.coindesk.com/v1/bpi/currentprice.json
Call https://api.github.com/repos/nullclaw/nullclaw
Fetch weather from https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41
```

---

## 📁 FILE TOOLS

### 3. File Read
```
Read /path/to/file.txt
Show me /home/user/config.json
What's in ./package.json?
```

### 4. File Write
```
Create file /tmp/test.txt with content: Hello World
Write to /home/user/notes.md: This is my note
Save this to file: [content]
```

### 5. File Edit
```
Edit /path/to/file.txt and change "old" to "new"
Replace "foo" with "bar" in config.json
```

---

## 🧠 MEMORY TOOLS

### 6. Memory Store
```
Remember that my name is Vina
Save this: API key is abc123
Store: Meeting at 3pm tomorrow
```

### 7. Memory Recall
```
What do you remember about me?
Recall my API key
Show stored memories
What's my name?
```

### 8. Memory Forget
```
Forget my API key
Delete memory about meeting
Clear all memories
```

---

## 💻 SHELL TOOLS

### 9. Shell Commands
```
Run: ls -la
Execute: pwd
What's in current directory?
Run: git status
Show: docker ps
```

**⚠️ Warning:** Shell runs in workspace only for safety!

---

## 🔧 GIT TOOLS

### 10. Git Operations
```
Git clone https://github.com/nullclaw/nullclaw.git
Git status
Git pull origin main
Show git log
```

---

## ⏰ SCHEDULE TOOLS

### 11. Schedule Tasks
```
Remind me tomorrow at 10am to check prices
Schedule: Run every day at 9am "search for news"
Create daily reminder for weather
```

### 12. Spawn (Run Background Tasks)
```
Run in background: monitor prices
Start task: check news every hour
```

---

## 🔄 AGENT TOOLS

### 13. Delegate (Ask Another Agent)
```
Delegate to researcher: Find AI papers
Ask coding agent: Fix this bug
```

### 14. Image Info
```
Analyze this image: [send image]
What's in this photo?
```

### 15. Screenshot
```
Take screenshot of https://example.com
Capture https://google.com
```

---

## 🎯 PRACTICAL EXAMPLES

### Crypto Price Check
```
Get https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd
```

### Weather
```
Search for weather in New York
Get https://api.open-meteo.com/v1/forecast?latitude=40.71&longitude=-74.01
```

### News
```
Search for latest tech news
Browse https://news.ycombinator.com
```

### Code Help
```
Search for Python tutorial
Find React documentation
```

### File Operations
```
Create /tmp/notes.txt with: Buy milk, eggs, bread
Read /tmp/notes.txt
```

### Memory
```
Remember my birthday is March 15
What did I ask you to remember?
```

---

## 🚀 QUICK START COMMANDS

Try these now on Telegram:

```
1. Hello
2. Search for AI news
3. What is Bitcoin price?
4. Remember my favorite color is blue
5. What do you remember about me?
6. Run: ls -la
7. Create /tmp/test.txt with: Test content
8. Read /tmp/test.txt
```

---

## ⚠️ LIMITATIONS

- **Workspace only:** Files limited to `/root/.nullclaw/workspace`
- **Security:** Some dangerous commands blocked
- **Rate limits:** Max 20 actions per hour
- **Timeout:** Commands timeout after 60 seconds

---

## 💡 TIPS

1. **Be natural:** Just ask like talking to a person
2. **Be specific:** "Search for React tutorials" vs "Search"
3. **Use follow-ups:** "What about Vue.js?" after React search
4. **Check memory:** "What do you know about me?"

---

## 🔧 ADVANCED USAGE

### Multi-step Tasks
```
1. Search for best laptops 2026
2. Now compare prices on Amazon
3. Save the results to /tmp/laptops.txt
4. Remember to check back next week
```

### Automation
```
Every morning at 8am: Search for crypto prices
Daily: Check weather and news
```

### Research
```
1. Find papers about transformer models
2. Summarize the top 3 results
3. Store summary in memory
4. Create file with full report
```
