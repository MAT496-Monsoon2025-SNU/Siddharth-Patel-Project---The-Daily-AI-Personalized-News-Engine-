"""
Researcher agent - searches for news and extracts key information.
This demonstrates TOOL CALLING and STRUCTURED OUTPUT.
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.config import Config
from src.state import NewsState, ResearchResults, NewsArticle
from src.tools.tavily_search import tavily_search
from src.utils.prompts import RESEARCHER_SYSTEM_PROMPT, RESEARCHER_USER_PROMPT
from typing import List


class ResearcherAgent:
    """
    Agent responsible for researching news topics.
    Uses Tavily search tool to find relevant articles.
    """
    
    def __init__(self):
        """Initialize the researcher agent."""
        self.llm = ChatOpenAI(
            model=Config.OPENAI_MODEL,
            temperature=Config.TEMPERATURE,
            api_key=Config.OPENAI_API_KEY
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", RESEARCHER_SYSTEM_PROMPT),
            ("user", RESEARCHER_USER_PROMPT)
        ])
    
    def research(self, state: NewsState) -> NewsState:
        """
        Research a topic using Tavily search.
        
        Args:
            state: Current NewsState
            
        Returns:
            Updated NewsState with research results
        """
        topic = state.topic
        
        print(f"🔍 Researching topic: {topic}")
        
        # Step 1: Search for news articles using Tavily (TOOL CALLING)
        articles = tavily_search.search_news(topic)
        
        if not articles:
            state.error_message = "No articles found for this topic"
            return state
        
        print(f"📰 Found {len(articles)} articles")
        
        # Step 2: Format search results for LLM analysis
        search_results_text = self._format_articles(articles)
        
        # Step 3: Use LLM to extract key facts and summarize
        chain = self.prompt | self.llm
        
        response = chain.invoke({
            "topic": topic,
            "search_results": search_results_text
        })
        
        # Step 4: Parse the response to extract structured information
        key_facts, summary = self._parse_response(response.content)
        
        # Step 5: Create structured research results (STRUCTURED OUTPUT)
        research_results = ResearchResults(
            topic=topic,
            articles=articles,
            key_facts=key_facts,
            summary=summary
        )
        
        state.research_results = research_results
        print(f"✅ Research complete. Found {len(key_facts)} key facts")
        
        return state
    
    def _format_articles(self, articles: List[NewsArticle]) -> str:
        """Format articles for LLM consumption."""
        formatted = []
        for idx, article in enumerate(articles, 1):
            formatted.append(f"""
Article {idx}:
Title: {article.title}
Source: {article.source or 'Unknown'}
URL: {article.url}
Published: {article.published_date or 'Unknown'}

Content:
{article.content}

---
""")
        return "\n".join(formatted)
    
    def _parse_response(self, response: str) -> tuple[List[str], str]:
        """
        Parse LLM response to extract key facts and summary.
        
        Returns:
            Tuple of (key_facts, summary)
        """
        # Simple parsing - look for key facts and summary sections
        lines = response.split('\n')
        key_facts = []
        summary = ""
        
        in_facts_section = False
        in_summary_section = False
        
        for line in lines:
            line = line.strip()
            
            # Detect sections
            if 'key fact' in line.lower() or 'facts:' in line.lower():
                in_facts_section = True
                in_summary_section = False
                continue
            elif 'summary' in line.lower():
                in_summary_section = True
                in_facts_section = False
                continue
            
            # Extract content
            if in_facts_section and line:
                # Remove bullet points and numbering
                fact = line.lstrip('•-*123456789. ')
                if fact:
                    key_facts.append(fact)
            elif in_summary_section and line:
                summary += line + " "
        
        # Fallback: if parsing failed, use the whole response
        if not key_facts:
            # Try to extract any bullet points or numbered items
            for line in lines:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or 
                           (len(line) > 2 and line[0].isdigit() and line[1] in '.)')):
                    fact = line.lstrip('•-*123456789. ')
                    if fact:
                        key_facts.append(fact)
        
        if not summary:
            # Use first few sentences as summary
            summary = ' '.join(lines[:3])
        
        return key_facts[:10], summary.strip()  # Limit to 10 facts


# Create singleton instance
researcher_agent = ResearcherAgent()
