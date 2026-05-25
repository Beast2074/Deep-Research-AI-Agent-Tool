from langchain_core.tools import Tool
from duckduckgo_search import DDGS
import re

def _search(query: str) -> str:
    """Run a DuckDuckGo search and return cleaned results."""
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            results.append(f"Title: {r['title']}\nSummary: {r['body']}\nURL: {r['href']}")
    combined = "\n\n---\n\n".join(results)
    return _clean(combined)

def _clean(text: str) -> str:
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text.strip()

# LangChain Tool object — plug directly into any agent
search_tool = Tool(
    name="web_search",
    func=_search,
    description=(
        "Search the web for information on any topic. "
        "Input should be a specific search query string. "
        "Returns titles, summaries, and sources."
    )
) 