const axios = require('axios');
const cheerio = require('cheerio');

// Free web search using DuckDuckGo HTML interface (no API key needed)
async function search(query, limit = 10) {
  try {
    const response = await axios.get('https://html.duckduckgo.com/html/', {
      params: { q: query },
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });

    const $ = cheerio.load(response.data);
    const results = [];

    $('.result').each((i, el) => {
      if (i >= limit) return;
      
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
    throw error;
  }
}

// Example usage
(async () => {
  const query = process.argv[2] || 'Node.js tutorials';
  console.log(`Searching for: "${query}"\n`);
  
  const results = await search(query);
  
  results.forEach((r, i) => {
    console.log(`${i + 1}. ${r.title}`);
    console.log(`   ${r.url}`);
    console.log(`   ${r.snippet}\n`);
  });
})();
