"""
Fact checker agent - verifies accuracy and suggests improvements.
This demonstrates RAG (using stored context for verification).
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.config import Config
from src.state import NewsState, FactCheckResult
from src.utils.prompts import FACT_CHECKER_SYSTEM_PROMPT, FACT_CHECKER_USER_PROMPT


class FactCheckerAgent:
    """
    Agent responsible for fact-checking generated content.
    Ensures accuracy while maintaining creative style.
    """
    
    def __init__(self):
        """Initialize the fact checker agent."""
        self.llm = ChatOpenAI(
            model=Config.OPENAI_MODEL,
            temperature=0.3,  # Lower temperature for more consistent fact-checking
            api_key=Config.OPENAI_API_KEY
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", FACT_CHECKER_SYSTEM_PROMPT),
            ("user", FACT_CHECKER_USER_PROMPT)
        ])
    
    def check_facts(self, state: NewsState) -> NewsState:
        """
        Verify the accuracy of generated content.
        
        Args:
            state: Current NewsState with generated content
            
        Returns:
            Updated NewsState with fact-check results
        """
        if not state.generated_content or not state.research_results:
            state.error_message = "Missing generated content or research results"
            return state
        
        print(f"🔍 Fact-checking content...")
        
        # Prepare source material for comparison
        source_material = self._prepare_source_material(state)
        
        # Prepare generated content
        generated_text = f"""
Title: {state.generated_content.title}

Content:
{state.generated_content.content}
"""
        
        # Invoke fact-checker
        chain = self.prompt | self.llm
        
        response = chain.invoke({
            "generated_content": generated_text,
            "source_material": source_material
        })
        
        # Parse fact-check results
        is_accurate, issues, suggestions, confidence = self._parse_response(response.content)
        
        # Create structured fact-check result
        fact_check = FactCheckResult(
            is_accurate=is_accurate,
            issues_found=issues,
            suggestions=suggestions,
            confidence_score=confidence
        )
        
        state.fact_check = fact_check
        
        # Determine if refinement is needed
        if not is_accurate or confidence < 0.7:
            state.needs_refinement = True
            print(f"⚠️  Issues found. Refinement needed. Confidence: {confidence:.2f}")
        else:
            state.needs_refinement = False
            state.is_complete = True
            print(f"✅ Fact-check passed. Confidence: {confidence:.2f}")
        
        return state
    
    def _prepare_source_material(self, state: NewsState) -> str:
        """Prepare source material for fact-checking."""
        research = state.research_results
        
        # Format key facts
        facts_text = "\n".join(f"- {fact}" for fact in research.key_facts)
        
        # Format articles (abbreviated)
        articles_text = []
        for idx, article in enumerate(research.articles[:3], 1):  # Limit to top 3
            articles_text.append(f"""
Source {idx}: {article.title}
{article.content[:500]}...
""")
        
        source_material = f"""
KEY FACTS FROM RESEARCH:
{facts_text}

SUMMARY:
{research.summary}

SOURCE ARTICLES (abbreviated):
{''.join(articles_text)}
"""
        return source_material
    
    def _parse_response(self, response: str) -> tuple[bool, list[str], list[str], float]:
        """
        Parse fact-check response.
        
        Returns:
            Tuple of (is_accurate, issues, suggestions, confidence_score)
        """
        lines = response.split('\n')
        
        is_accurate = True
        issues = []
        suggestions = []
        confidence = 0.8  # Default
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            # Check for accuracy determination
            if 'accurate' in line.lower() and ':' in line:
                if 'false' in line.lower() or 'not accurate' in line.lower() or 'no' in line.lower():
                    is_accurate = False
                elif 'true' in line.lower() or 'yes' in line.lower():
                    is_accurate = True
                continue
            
            # Detect sections
            if 'issue' in line.lower() and ('found' in line.lower() or ':' in line):
                current_section = 'issues'
                continue
            elif 'suggestion' in line.lower() and ':' in line:
                current_section = 'suggestions'
                continue
            elif 'confidence' in line.lower() and ':' in line:
                # Try to extract confidence score
                try:
                    # Look for numbers
                    parts = line.split(':')
                    if len(parts) > 1:
                        score_text = parts[1].strip()
                        # Extract first number
                        import re
                        numbers = re.findall(r'0?\.\d+|\d+\.?\d*', score_text)
                        if numbers:
                            score = float(numbers[0])
                            # Normalize to 0-1 range if needed
                            if score > 1:
                                score = score / 100
                            confidence = max(0.0, min(1.0, score))
                except:
                    pass
                continue
            
            # Extract content
            if not line:
                continue
            
            if current_section == 'issues':
                issue = line.lstrip('•-*123456789. ')
                if issue and len(issue) > 5:
                    issues.append(issue)
            elif current_section == 'suggestions':
                suggestion = line.lstrip('•-*123456789. ')
                if suggestion and len(suggestion) > 5:
                    suggestions.append(suggestion)
        
        # If no issues found, assume accurate
        if not issues:
            is_accurate = True
            confidence = max(confidence, 0.85)
        
        return is_accurate, issues[:5], suggestions[:5], confidence


# Create singleton instance
fact_checker_agent = FactCheckerAgent()
