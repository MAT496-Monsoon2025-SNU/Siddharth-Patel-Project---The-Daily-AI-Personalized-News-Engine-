"""
Editor agent - selects editorial angle and tone for the story.
This demonstrates PROMPTING and STRUCTURED OUTPUT.
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.config import Config
from src.state import NewsState, EditorialAngle
from src.utils.prompts import EDITOR_SYSTEM_PROMPT, EDITOR_USER_PROMPT


class EditorAgent:
    """
    Agent responsible for choosing the editorial angle.
    Analyzes research results and determines the best way to present the story.
    """
    
    def __init__(self):
        """Initialize the editor agent."""
        self.llm = ChatOpenAI(
            model=Config.OPENAI_MODEL,
            temperature=Config.TEMPERATURE,
            api_key=Config.OPENAI_API_KEY
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", EDITOR_SYSTEM_PROMPT),
            ("user", EDITOR_USER_PROMPT)
        ])
    
    def select_angle(self, state: NewsState) -> NewsState:
        """
        Select the best editorial angle for the story.
        
        Args:
            state: Current NewsState with research results
            
        Returns:
            Updated NewsState with editorial angle
        """
        if not state.research_results:
            state.error_message = "No research results available"
            return state
        
        print(f"📝 Selecting editorial angle for: {state.topic}")
        
        # Prepare input for the editor
        research = state.research_results
        key_facts_text = "\n".join(f"- {fact}" for fact in research.key_facts)
        
        # Invoke the LLM to select an angle
        chain = self.prompt | self.llm
        
        response = chain.invoke({
            "topic": state.topic,
            "key_facts": key_facts_text,
            "summary": research.summary,
            "format_type": state.format_type
        })
        
        # Parse the response to extract editorial angle
        angle, reasoning, tone, key_points = self._parse_response(response.content)
        
        # Create structured editorial angle (STRUCTURED OUTPUT)
        editorial_angle = EditorialAngle(
            angle=angle,
            reasoning=reasoning,
            target_tone=tone,
            key_points=key_points
        )
        
        state.editorial_angle = editorial_angle
        print(f"✅ Editorial angle selected: {angle[:60]}...")
        
        return state
    
    def _parse_response(self, response: str) -> tuple[str, str, str, list[str]]:
        """
        Parse LLM response to extract editorial components.
        
        Returns:
            Tuple of (angle, reasoning, tone, key_points)
        """
        lines = response.split('\n')
        
        angle = ""
        reasoning = ""
        tone = ""
        key_points = []
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            # Detect sections
            if 'angle' in line.lower() and ':' in line:
                current_section = 'angle'
                # Try to extract angle from same line
                parts = line.split(':', 1)
                if len(parts) > 1:
                    angle = parts[1].strip()
                continue
            elif 'reasoning' in line.lower() and ':' in line:
                current_section = 'reasoning'
                parts = line.split(':', 1)
                if len(parts) > 1:
                    reasoning = parts[1].strip()
                continue
            elif 'tone' in line.lower() and ':' in line:
                current_section = 'tone'
                parts = line.split(':', 1)
                if len(parts) > 1:
                    tone = parts[1].strip()
                continue
            elif 'key point' in line.lower() or 'points to emphasize' in line.lower():
                current_section = 'points'
                continue
            
            # Extract content based on current section
            if not line:
                continue
                
            if current_section == 'angle' and not angle:
                angle = line
            elif current_section == 'reasoning':
                reasoning += " " + line
            elif current_section == 'tone' and not tone:
                tone = line
            elif current_section == 'points':
                # Remove bullet points and numbering
                point = line.lstrip('•-*123456789. ')
                if point:
                    key_points.append(point)
        
        # Fallback values
        if not angle:
            angle = f"Exploring the latest developments in {response[:50]}"
        if not reasoning:
            reasoning = "This angle provides a fresh perspective on the topic"
        if not tone:
            tone = "informative and engaging"
        if not key_points:
            key_points = ["Main developments", "Key implications", "Future outlook"]
        
        return angle.strip(), reasoning.strip(), tone.strip(), key_points[:5]


# Create singleton instance
editor_agent = EditorAgent()
