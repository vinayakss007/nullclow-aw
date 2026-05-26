#!/usr/bin/env node
/**
 * NullClaw AI Multi-Agent Platform
 * Telegram Bot + OpenRouter AI + Web Search + Agent Routing
 * 
 * This is the main entry point that connects:
 * - Telegram Bot (user interface)
 * - OpenRouter (AI model provider)
 * - DuckDuckGo (web search)
 * - Multi-Agent Router (task assignment)
 */

require('dotenv').config();
const TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');
const cheerio = require('cheerio');
const express = require('express');
const fs = require('fs');
const path = require('path');

// ============================================
// CONFIGURATION
// ============================================

const CONFIG = {
  telegram: {
    token: process.env.TELEGRAM_BOT_TOKEN,
    polling: true
  },
  openrouter: {
    apiKey: process.env.OPENROUTER_API_KEY,
    baseUrl: 'https://openrouter.ai/api/v1',
    model: process.env.AI_MODEL || 'google/gemini-2.0-flash-exp:free',
    fallbackModel: process.env.AI_FALLBACK_MODEL || 'meta-llama/llama-3.1-8b-instruct:free'
  },
  platform: {
    name: 'NullClaw AI Platform',
    version: '1.0.0',
    adminChatId: process.env.ADMIN_CHAT_ID || null,
    maxSearchResults: 5,
    maxResponseLength: 4000,
    port: process.env.PORT || 3000
  }
};

// ============================================
// AGENT DEFINITIONS
// ============================================

const AGENTS = {
  sales: {
    name: 'Sales Lead Agent',
    description: 'Score and qualify sales leads, write outreach emails',
    keywords: ['lead', 'sales', 'score', 'prospect', 'outreach', 'email', 'crm', 'pipeline', 'deal'],
    subAgents: ['lead_scorer', 'email_writer', 'crm_updater'],
    systemPrompt: `You are a sales expert AI agent. You help with:
- Scoring leads (0-100 based on budget, timeline, need, authority)
- Writing personalized outreach emails
- Managing sales pipeline
- Qualifying prospects
Always provide actionable scores and specific recommendations.`
  },
  hr: {
    name: 'HR Screening Agent',
    description: 'Screen resumes, rank candidates, generate interview questions',
    keywords: ['resume', 'candidate', 'hire', 'interview', 'screen', 'recruit', 'job', 'talent'],
    subAgents: ['resume_screener', 'question_generator', 'ranker'],
    systemPrompt: `You are an HR screening expert AI agent. You help with:
- Screening and scoring resumes against job requirements
- Ranking candidates by fit
- Generating tailored interview questions
- Identifying red flags and strengths
Always be objective and focus on qualifications.`
  },
  support: {
    name: 'Customer Support Agent',
    description: 'Handle support tickets, classify issues, generate responses',
    keywords: ['support', 'ticket', 'issue', 'bug', 'help', 'complaint', 'escalate', 'customer'],
    subAgents: ['ticket_classifier', 'response_generator', 'escalation_handler'],
    systemPrompt: `You are a customer support expert AI agent. You help with:
- Classifying support tickets by priority and category
- Generating helpful, empathetic responses
- Deciding when to escalate issues
- Tracking recurring problems
Always be professional and solution-oriented.`
  },
  research: {
    name: 'Research Agent',
    description: 'Research topics, summarize findings, provide citations',
    keywords: ['research', 'find', 'search', 'summarize', 'analyze', 'report', 'study', 'data'],
    subAgents: ['searcher', 'summarizer', 'citation_manager'],
    systemPrompt: `You are a research expert AI agent. You help with:
- Researching topics using web search
- Summarizing findings with key points
- Providing citations and sources
- Comparing different perspectives
Always cite sources and be thorough.`
  },
  content: {
    name: 'Content Agent',
    description: 'Create blogs, social media posts, SEO content',
    keywords: ['blog', 'content', 'write', 'seo', 'social', 'post', 'article', 'copy', 'marketing'],
    subAgents: ['seo_analyzer', 'blog_writer', 'social_media_manager'],
    systemPrompt: `You are a content creation expert AI agent. You help with:
- Writing SEO-optimized blog posts
- Creating social media content for multiple platforms
- Analyzing keywords and competition
- Generating engaging headlines and CTAs
Always optimize for engagement and SEO.`
  },
  finance: {
    name: 'Finance Agent',
    description: 'Handle invoices, expenses, financial analysis, budgets',
    keywords: ['invoice', 'expense', 'budget', 'finance', 'tax', 'accounting', 'revenue', 'cost', 'profit'],
    subAgents: ['invoice_generator', 'expense_tracker', 'financial_reporter'],
    systemPrompt: `You are a finance expert AI agent. You help with:
- Generating invoices and expense reports
- Budget analysis and planning
- Financial projections
- Cost optimization recommendations
Always ensure accuracy and include relevant calculations.`
  },
  legal: {
    name: 'Legal Document Agent',
    description: 'Draft contracts, NDAs, terms, legal summaries',
    keywords: ['contract', 'legal', 'nda', 'terms', 'agreement', 'clause', 'compliance', 'policy'],
    subAgents: ['contract_drafter', 'nda_generator', 'compliance_checker'],
    systemPrompt: `You are a legal document assistant AI agent. You help with:
- Drafting contracts and agreements
- Generating NDAs and terms of service
- Summarizing legal documents
- Checking compliance requirements
DISCLAIMER: This is AI-generated content and not legal advice. Always consult a qualified attorney.`
  },
  general: {
    name: 'General Assistant',
    description: 'General AI assistant for any task',
    keywords: [],
    subAgents: [],
    systemPrompt: `You are NullClaw, a helpful AI assistant. You can help with any task including:
- Answering questions
- Writing and editing text
- Problem solving
- Brainstorming ideas
- Explaining concepts
Be concise, helpful, and accurate.`
  }
};

// ============================================
// WEB SEARCH (DuckDuckGo - No API Key Needed)
// ============================================

async function webSearch(query, limit = 5) {
  try {
    const response = await axios.get('https://html.duckduckgo.com/html/', {
      params: { q: query },
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      },
      timeout: 10000
    });

    const $ = cheerio.load(response.data);
    const results = [];

    $('.result').each((i, el) => {
      if (i >= limit) return false;
      const title = $(el).find('.result__title').text().trim();
      const snippet = $(el).find('.result__snippet').text().trim();
      const url = $(el).find('.result__url').text().trim();
      if (title && snippet) {
        results.push({ title, snippet, url });
      }
    });

    return results;
  } catch (error) {
    console.error('Search error:', error.message);
    return [];
  }
}

// ============================================
// AI PROVIDER (OpenRouter - Multi-Model)
// ============================================

async function callAI(messages, options = {}) {
  const model = options.model || CONFIG.openrouter.model;
  
  if (!CONFIG.openrouter.apiKey) {
    return 'AI is not configured. Please set OPENROUTER_API_KEY environment variable.';
  }

  try {
    const response = await axios.post(
      `${CONFIG.openrouter.baseUrl}/chat/completions`,
      {
        model: model,
        messages: messages,
        max_tokens: options.maxTokens || 2000,
        temperature: options.temperature || 0.7,
        stream: false
      },
      {
        headers: {
          'Authorization': `Bearer ${CONFIG.openrouter.apiKey}`,
          'Content-Type': 'application/json',
          'HTTP-Referer': 'https://github.com/nullclaw',
          'X-Title': 'NullClaw AI Platform'
        },
        timeout: 60000
      }
    );

    const content = response.data?.choices?.[0]?.message?.content;
    if (!content) {
      throw new Error('Empty response from AI');
    }
    return content;
  } catch (error) {
    // Try fallback model
    if (model !== CONFIG.openrouter.fallbackModel && !options._isFallback) {
      console.log(`Primary model failed (${error.message}), trying fallback...`);
      return callAI(messages, { 
        ...options, 
        model: CONFIG.openrouter.fallbackModel, 
        _isFallback: true 
      });
    }
    console.error('AI Error:', error.response?.data || error.message);
    return `Sorry, AI is temporarily unavailable. Error: ${error.message}`;
  }
}

// ============================================
// AGENT ROUTER
// ============================================

function routeToAgent(message) {
  const lower = message.toLowerCase();
  
  for (const [key, agent] of Object.entries(AGENTS)) {
    if (key === 'general') continue;
    if (agent.keywords.some(kw => lower.includes(kw))) {
      return { agentKey: key, agent };
    }
  }
  
  return { agentKey: 'general', agent: AGENTS.general };
}

// ============================================
// CONVERSATION MEMORY (In-Memory Per Chat)
// ============================================

const conversations = new Map();
const MAX_HISTORY = 20;

function getConversation(chatId) {
  if (!conversations.has(chatId)) {
    conversations.set(chatId, []);
  }
  return conversations.get(chatId);
}

function addToConversation(chatId, role, content) {
  const conv = getConversation(chatId);
  conv.push({ role, content });
  if (conv.length > MAX_HISTORY) {
    conv.splice(0, conv.length - MAX_HISTORY);
  }
}

function clearConversation(chatId) {
  conversations.delete(chatId);
}

// ============================================
// USAGE TRACKING (In-Memory)
// ============================================

const usage = {
  totalMessages: 0,
  totalSearches: 0,
  totalAICalls: 0,
  byAgent: {},
  startedAt: new Date().toISOString()
};

function trackUsage(agentKey) {
  usage.totalMessages++;
  usage.byAgent[agentKey] = (usage.byAgent[agentKey] || 0) + 1;
}

// ============================================
// TELEGRAM BOT
// ============================================

function startBot() {
  if (!CONFIG.telegram.token) {
    console.error('TELEGRAM_BOT_TOKEN is not set!');
    console.log('Set it in your .env file or environment variables.');
    console.log('Get a token from @BotFather on Telegram.');
    console.log('\nStarting in API-only mode (no Telegram)...\n');
    return null;
  }

  const bot = new TelegramBot(CONFIG.telegram.token, { polling: true });
  console.log('Telegram bot started successfully!');

  // /start command
  bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    clearConversation(chatId);
    
    bot.sendMessage(chatId, `
*Welcome to NullClaw AI Platform!* 

I'm your multi-agent AI assistant. I can help with:

*Available Agents:*
- /sales - Lead scoring & outreach
- /hr - Resume screening & interviews
- /support - Ticket handling & responses
- /research - Web research & summaries
- /content - Blog, SEO & social media
- /finance - Invoices & budgets
- /legal - Contracts & NDAs

*Commands:*
- /search <query> - Web search
- /agent <name> - Switch agent mode
- /clear - Clear conversation history
- /status - Bot status & usage
- /help - Show this message

Or just send me any message and I'll route it to the best agent!
    `.trim(), { parse_mode: 'Markdown' });
  });

  // /help command
  bot.onText(/\/help/, (msg) => {
    bot.sendMessage(msg.chat.id, `
*NullClaw Commands:*

/start - Welcome & reset
/search <query> - Search the web
/agent <name> - Use specific agent (sales, hr, support, research, content, finance, legal)
/clear - Clear chat history
/status - Bot statistics
/agents - List all agents
/help - This message

*Tips:*
- Just type naturally, I'll auto-route to the right agent
- Use /search for real-time web info
- Use /agent to force a specific expert mode
    `.trim(), { parse_mode: 'Markdown' });
  });

  // /agents command
  bot.onText(/\/agents/, (msg) => {
    let text = '*Available Agents:*\n\n';
    for (const [key, agent] of Object.entries(AGENTS)) {
      if (key === 'general') continue;
      text += `*${agent.name}*\n`;
      text += `  ${agent.description}\n`;
      text += `  Sub-agents: ${agent.subAgents.join(', ')}\n\n`;
    }
    bot.sendMessage(msg.chat.id, text, { parse_mode: 'Markdown' });
  });

  // /search command
  bot.onText(/\/search (.+)/, async (msg, match) => {
    const chatId = msg.chat.id;
    const query = match[1];

    bot.sendChatAction(chatId, 'typing');
    usage.totalSearches++;

    const results = await webSearch(query, CONFIG.platform.maxSearchResults);

    if (results.length === 0) {
      bot.sendMessage(chatId, 'No search results found. Try a different query.');
      return;
    }

    let text = `*Search Results for:* "${query}"\n\n`;
    results.forEach((r, i) => {
      text += `*${i + 1}. ${r.title}*\n`;
      text += `${r.snippet}\n`;
      if (r.url) text += `_${r.url}_\n`;
      text += '\n';
    });

    // Ask AI to summarize
    const summaryMessages = [
      { role: 'system', content: 'Summarize these search results in 2-3 sentences. Be concise.' },
      { role: 'user', content: `Query: ${query}\n\nResults:\n${results.map(r => `${r.title}: ${r.snippet}`).join('\n')}` }
    ];

    const summary = await callAI(summaryMessages, { maxTokens: 300 });
    text += `\n*Summary:* ${summary}`;

    // Truncate if too long for Telegram
    if (text.length > CONFIG.platform.maxResponseLength) {
      text = text.substring(0, CONFIG.platform.maxResponseLength) + '...';
    }

    bot.sendMessage(chatId, text, { parse_mode: 'Markdown' }).catch(() => {
      // Fallback without markdown if it fails
      bot.sendMessage(chatId, text.replace(/[*_`]/g, ''));
    });
  });

  // /agent command - switch to specific agent
  bot.onText(/\/agent (.+)/, (msg, match) => {
    const chatId = msg.chat.id;
    const agentName = match[1].toLowerCase().trim();

    if (AGENTS[agentName]) {
      clearConversation(chatId);
      // Store agent preference
      conversations.set(`${chatId}_agent`, agentName);
      bot.sendMessage(chatId, `Switched to *${AGENTS[agentName].name}*\n\n${AGENTS[agentName].description}\n\nSend me a task!`, { parse_mode: 'Markdown' });
    } else {
      const available = Object.keys(AGENTS).filter(k => k !== 'general').join(', ');
      bot.sendMessage(chatId, `Unknown agent "${agentName}"\n\nAvailable: ${available}`);
    }
  });

  // /clear command
  bot.onText(/\/clear/, (msg) => {
    clearConversation(msg.chat.id);
    conversations.delete(`${msg.chat.id}_agent`);
    bot.sendMessage(msg.chat.id, 'Conversation cleared! Start fresh.');
  });

  // /status command
  bot.onText(/\/status/, (msg) => {
    const uptime = Math.floor((Date.now() - new Date(usage.startedAt).getTime()) / 1000);
    const hours = Math.floor(uptime / 3600);
    const minutes = Math.floor((uptime % 3600) / 60);

    let text = `*NullClaw Platform Status*\n\n`;
    text += `*Uptime:* ${hours}h ${minutes}m\n`;
    text += `*Messages Processed:* ${usage.totalMessages}\n`;
    text += `*Searches:* ${usage.totalSearches}\n`;
    text += `*AI Calls:* ${usage.totalAICalls}\n`;
    text += `*Model:* ${CONFIG.openrouter.model}\n`;
    text += `*Active Conversations:* ${conversations.size}\n\n`;
    
    if (Object.keys(usage.byAgent).length > 0) {
      text += `*Agent Usage:*\n`;
      for (const [agent, count] of Object.entries(usage.byAgent)) {
        text += `  ${agent}: ${count}\n`;
      }
    }

    bot.sendMessage(msg.chat.id, text, { parse_mode: 'Markdown' });
  });

  // Handle all other messages (main AI conversation)
  bot.on('message', async (msg) => {
    // Skip commands
    if (msg.text && msg.text.startsWith('/')) return;
    if (!msg.text) return;

    const chatId = msg.chat.id;
    const userMessage = msg.text;

    bot.sendChatAction(chatId, 'typing');

    // Check if user has a preferred agent
    const preferredAgent = conversations.get(`${chatId}_agent`);
    
    // Route to agent
    let agentKey, agent;
    if (preferredAgent && AGENTS[preferredAgent]) {
      agentKey = preferredAgent;
      agent = AGENTS[preferredAgent];
    } else {
      ({ agentKey, agent } = routeToAgent(userMessage));
    }

    trackUsage(agentKey);

    // Check if search is needed for research agent
    let searchContext = '';
    if (agentKey === 'research' || userMessage.toLowerCase().includes('search for') || userMessage.toLowerCase().includes('look up')) {
      const searchResults = await webSearch(userMessage, 3);
      if (searchResults.length > 0) {
        searchContext = '\n\n[Web Search Results]:\n' + searchResults.map(r => `- ${r.title}: ${r.snippet}`).join('\n');
        usage.totalSearches++;
      }
    }

    // Build messages
    const history = getConversation(chatId);
    const messages = [
      { role: 'system', content: agent.systemPrompt + (searchContext ? `\n\nUse these search results to help answer:\n${searchContext}` : '') },
      ...history,
      { role: 'user', content: userMessage }
    ];

    // Call AI
    usage.totalAICalls++;
    const response = await callAI(messages);

    // Save to history
    addToConversation(chatId, 'user', userMessage);
    addToConversation(chatId, 'assistant', response);

    // Send response (handle Telegram 4096 char limit)
    const maxLen = CONFIG.platform.maxResponseLength;
    if (response.length > maxLen) {
      const parts = response.match(new RegExp(`.{1,${maxLen}}`, 'gs'));
      for (const part of parts) {
        await bot.sendMessage(chatId, part).catch(() => {});
      }
    } else {
      bot.sendMessage(chatId, response, { parse_mode: 'Markdown' }).catch(() => {
        // Fallback without markdown
        bot.sendMessage(chatId, response);
      });
    }
  });

  // Error handling
  bot.on('polling_error', (error) => {
    console.error('Telegram polling error:', error.message);
  });

  return bot;
}

// ============================================
// HEALTH CHECK SERVER (for deployment)
// ============================================

function startHealthServer() {
  const app = express();

  app.get('/', (req, res) => {
    res.json({
      name: CONFIG.platform.name,
      version: CONFIG.platform.version,
      status: 'running',
      uptime: process.uptime(),
      agents: Object.keys(AGENTS).length,
      stats: usage
    });
  });

  app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
  });

  app.get('/agents', (req, res) => {
    const agentList = Object.entries(AGENTS).map(([key, agent]) => ({
      key,
      name: agent.name,
      description: agent.description,
      subAgents: agent.subAgents
    }));
    res.json(agentList);
  });

  // Simple search API endpoint
  app.get('/search', async (req, res) => {
    const query = req.query.q;
    if (!query) {
      return res.status(400).json({ error: 'Query parameter "q" is required' });
    }
    const results = await webSearch(query);
    res.json({ query, results });
  });

  // AI chat API endpoint
  app.get('/chat', async (req, res) => {
    const message = req.query.message || req.query.m;
    if (!message) {
      return res.status(400).json({ error: 'Message parameter is required' });
    }
    const { agentKey, agent } = routeToAgent(message);
    const messages = [
      { role: 'system', content: agent.systemPrompt },
      { role: 'user', content: message }
    ];
    const response = await callAI(messages);
    res.json({ agent: agentKey, response });
  });

  app.listen(CONFIG.platform.port, () => {
    console.log(`Health server running on port ${CONFIG.platform.port}`);
  });

  return app;
}

// ============================================
// MAIN STARTUP
// ============================================

console.log(`
============================================
  NullClaw AI Multi-Agent Platform v${CONFIG.platform.version}
============================================
`);

console.log('Configuration:');
console.log(`  Telegram Bot: ${CONFIG.telegram.token ? 'Configured' : 'NOT SET'}`);
console.log(`  OpenRouter AI: ${CONFIG.openrouter.apiKey ? 'Configured' : 'NOT SET'}`);
console.log(`  AI Model: ${CONFIG.openrouter.model}`);
console.log(`  Fallback Model: ${CONFIG.openrouter.fallbackModel}`);
console.log(`  Agents: ${Object.keys(AGENTS).length}`);
console.log(`  Port: ${CONFIG.platform.port}`);
console.log('');

// Start health check server
startHealthServer();

// Start Telegram bot
const bot = startBot();

if (bot) {
  console.log('\nNullClaw is running! Send /start to your Telegram bot.');
} else {
  console.log('\nRunning in API-only mode. Endpoints:');
  console.log(`  GET http://localhost:${CONFIG.platform.port}/ - Status`);
  console.log(`  GET http://localhost:${CONFIG.platform.port}/health - Health check`);
  console.log(`  GET http://localhost:${CONFIG.platform.port}/agents - List agents`);
  console.log(`  GET http://localhost:${CONFIG.platform.port}/search?q=<query> - Web search`);
  console.log(`  GET http://localhost:${CONFIG.platform.port}/chat?m=<message> - AI chat`);
}

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\nShutting down NullClaw...');
  if (bot) bot.stopPolling();
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('\nShutting down NullClaw...');
  if (bot) bot.stopPolling();
  process.exit(0);
});
