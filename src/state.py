"""
State definitions for The Daily AI using Pydantic.
This demonstrates STRUCTURED OUTPUT - one of the key MAT496 topics.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class NewsArticle(BaseModel):
    """Represents a single news article from search results."""
    title: str
    url: str
    content: str
    published_date: Optional[str] = None
    source: Optional[str] = None


class ResearchResults(BaseModel):
    """Structured output from the Researcher agent."""
    topic: str
    articles: List[NewsArticle]
    key_facts: List[str] = Field(description="Key facts extracted from articles")
    summary: str = Field(description="Brief summary of findings")


class EditorialAngle(BaseModel):
    """Structured output from the Editor agent."""
    angle: str = Field(description="The chosen editorial angle/hook for the story")
    reasoning: str = Field(description="Why this angle is interesting")
    target_tone: str = Field(description="Suggested tone for the article")
    key_points: List[str] = Field(description="Key points to emphasize")


class GeneratedContent(BaseModel):
    """Structured output from the Journalist agent."""
    title: str
    content: str
    format_type: Literal["blog", "vintage", "professional", "social_thread"]
    word_count: int
    sources_used: List[str] = Field(description="URLs of sources referenced")


class FactCheckResult(BaseModel):
    """Structured output from the Fact Checker agent."""
    is_accurate: bool
    issues_found: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    confidence_score: float = Field(ge=0.0, le=1.0)


class NewsState(BaseModel):
    """
    Main state object for the LangGraph workflow.
    This is passed between all nodes in the graph.
    """
    # Input
    topic: str = Field(description="The news topic to research")
    format_type: Literal["blog", "vintage", "professional", "social_thread"] = Field(
        default="blog",
        description="Desired output format"
    )
    
    # Research phase
    research_results: Optional[ResearchResults] = None
    
    # Editorial phase
    editorial_angle: Optional[EditorialAngle] = None
    
    # Writing phase
    generated_content: Optional[GeneratedContent] = None
    
    # Fact-checking phase
    fact_check: Optional[FactCheckResult] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    iteration_count: int = Field(default=0, description="Number of refinement iterations")
    
    # Control flow
    needs_refinement: bool = Field(default=False)
    is_complete: bool = Field(default=False)
    error_message: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True
