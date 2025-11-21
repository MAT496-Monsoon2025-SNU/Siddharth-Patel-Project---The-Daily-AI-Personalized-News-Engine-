"""
Journalist agent - writes content in various formats.
This demonstrates advanced PROMPTING and STRUCTURED OUTPUT.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.config import Config
from src.state import NewsState, GeneratedContent
from src.utils.prompts import get_journalist_prompt


class JournalistAgent:
    """
    Agent responsible for writing the actual content.
    Adapts writing style based on the desired format.
    """
    
    def __init__(self):
        """Initialize the journalist agent."""
        self.llm = ChatOpenAI(
            model=Config.OPENAI_MODEL,
            temperature=Config.TEMPERATURE,
            api_key=Config.OPENAI_API_KEY
        )
    
    def write_content(self, state: NewsState) -> NewsState:
        """
        Write content based on research and editorial angle.
        
        Args:
            state: Current NewsState with research and editorial angle
            
        Returns:
            Updated NewsState with generated content
        """
        if not state.research_results or not state.editorial_angle:
            state.error_message = "Missing research results or editorial angle"
            return state
        
        print(f"✍️  Writing {state.format_type} content...")
        
        # Prepare source material
        source_material = self._prepare_source_material(state)
        
        # Get format-specific prompts
        system_prompt, user_prompt = get_journalist_prompt(
            format_type=state.format_type,
            topic=state.topic,
            angle=state.editorial_angle.angle,
            tone=state.editorial_angle.target_tone,
            key_points=state.editorial_angle.key_points,
            source_material=source_material
        )
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_prompt)
        ])
        
        # Generate content
        chain = prompt | self.llm
        response = chain.invoke({})
        
        # Parse the generated content
        title, content = self._parse_content(response.content, state.format_type)
        
        # Extract source URLs
        source_urls = [article.url for article in state.research_results.articles]
        
        # Create structured output
        generated_content = GeneratedContent(
            title=title,
            content=content,
            format_type=state.format_type,
            word_count=len(content.split()),
            sources_used=source_urls
        )
        
        state.generated_content = generated_content
        print(f"✅ Content written: {len(content.split())} words")
        
        return state
    
    def _prepare_source_material(self, state: NewsState) -> str:
        """Prepare source material from research results."""
        research = state.research_results
        
        # Format articles
        articles_text = []
        for idx, article in enumerate(research.articles, 1):
            articles_text.append(f"""
Article {idx}: {article.title}
Source: {article.source or 'Unknown'}
URL: {article.url}

{article.content}

---
""")
        
        # Combine everything
        source_material = f"""
TOPIC: {research.topic}

KEY FACTS:
{chr(10).join(f"- {fact}" for fact in research.key_facts)}

SUMMARY:
{research.summary}

DETAILED ARTICLES:
{''.join(articles_text)}
"""
        return source_material
    
    def _parse_content(self, response: str, format_type: str) -> tuple[str, str]:
        """
        Parse the generated content to extract title and body.
        
        Returns:
            Tuple of (title, content)
        """
        lines = response.split('\n')
        title = ""
        content_lines = []
        
        # Try to find title
        for idx, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Look for title indicators
            if not title and line_stripped:
                # Check for explicit title markers
                if 'title:' in line_stripped.lower():
                    title = line_stripped.split(':', 1)[1].strip()
                    continue
                # Check for markdown headers
                elif line_stripped.startswith('#'):
                    title = line_stripped.lstrip('#').strip()
                    continue
                # If it's the first substantial line and looks like a title
                elif idx < 3 and len(line_stripped) > 10 and not line_stripped.endswith('.'):
                    title = line_stripped
                    continue
            
            # Add to content if we have a title
            if title or idx > 2:
                content_lines.append(line)
        
        # If no title found, use first line
        if not title and lines:
            title = lines[0].strip()
            content_lines = lines[1:]
        
        # Clean up title
        title = title.strip('"\'#*- ')
        
        # Join content
        content = '\n'.join(content_lines).strip()
        
        # If content is empty, use the whole response
        if not content:
            content = response
        
        return title, content


# Create singleton instance
journalist_agent = JournalistAgent()
