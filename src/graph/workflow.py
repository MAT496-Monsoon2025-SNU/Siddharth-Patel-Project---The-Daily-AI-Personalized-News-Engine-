"""
LangGraph workflow implementation.
This demonstrates LANGGRAPH: State, Nodes, Graph - a key MAT496 topic.
"""

from typing import Literal
from langgraph.graph import StateGraph, END
from src.state import NewsState
from src.agents.researcher import researcher_agent
from src.agents.editor import editor_agent
from src.agents.journalist import journalist_agent
from src.agents.fact_checker import fact_checker_agent
from src.rag.vector_store import vector_store


# Node functions
def research_node(state: NewsState) -> NewsState:
    """Research node - searches for news and extracts facts."""
    return researcher_agent.research(state)


def store_in_vector_db_node(state: NewsState) -> NewsState:
    """Store research results in vector database for RAG."""
    if state.research_results:
        print("💾 Storing articles in vector database...")
        vector_store.add_articles(
            state.research_results.articles,
            state.topic
        )
    return state


def editor_node(state: NewsState) -> NewsState:
    """Editor node - selects editorial angle."""
    return editor_agent.select_angle(state)


def journalist_node(state: NewsState) -> NewsState:
    """Journalist node - writes the content."""
    return journalist_agent.write_content(state)


def fact_check_node(state: NewsState) -> NewsState:
    """Fact-check node - verifies accuracy."""
    return fact_checker_agent.check_facts(state)


def refinement_node(state: NewsState) -> NewsState:
    """
    Refinement node - uses RAG to get additional context and refine content.
    This demonstrates RAG (Retrieval Augmented Generation).
    """
    print("🔄 Refining content with additional context...")
    
    # Get relevant context from vector store
    if state.fact_check and state.fact_check.issues_found:
        # Use issues to guide retrieval
        query = f"{state.topic} {' '.join(state.fact_check.issues_found[:2])}"
    else:
        query = state.topic
    
    additional_context = vector_store.get_context_for_topic(state.topic, query, n_results=3)
    
    # For now, just mark for re-writing
    # In a more advanced version, we could pass the context to the journalist
    state.iteration_count += 1
    
    # Prevent infinite loops
    if state.iteration_count >= 2:
        print("⚠️  Max refinement iterations reached. Accepting current version.")
        state.needs_refinement = False
        state.is_complete = True
    
    return state


# Conditional edge functions
def should_continue_after_research(state: NewsState) -> Literal["continue", "end"]:
    """Decide whether to continue after research."""
    if state.error_message or not state.research_results:
        return "end"
    return "continue"


def should_refine(state: NewsState) -> Literal["refine", "end"]:
    """Decide whether content needs refinement."""
    if state.needs_refinement and state.iteration_count < 2:
        return "refine"
    return "end"


# Build the graph
def create_workflow() -> StateGraph:
    """
    Create the LangGraph workflow.
    
    Workflow:
    START → Research → Store in Vector DB → Editor → Journalist → Fact Check → [Refine or END]
                                                                        ↓
                                                                    Journalist (if refine)
    """
    # Initialize the graph with NewsState
    workflow = StateGraph(NewsState)
    
    # Add nodes
    workflow.add_node("research", research_node)
    workflow.add_node("store_vectors", store_in_vector_db_node)
    workflow.add_node("editor", editor_node)
    workflow.add_node("journalist", journalist_node)
    workflow.add_node("fact_check", fact_check_node)
    workflow.add_node("refine", refinement_node)
    
    # Set entry point
    workflow.set_entry_point("research")
    
    # Add edges
    workflow.add_conditional_edges(
        "research",
        should_continue_after_research,
        {
            "continue": "store_vectors",
            "end": END
        }
    )
    
    workflow.add_edge("store_vectors", "editor")
    workflow.add_edge("editor", "journalist")
    workflow.add_edge("journalist", "fact_check")
    
    workflow.add_conditional_edges(
        "fact_check",
        should_refine,
        {
            "refine": "refine",
            "end": END
        }
    )
    
    workflow.add_edge("refine", "journalist")
    
    # Compile the graph
    return workflow.compile()


# Create the compiled workflow
news_workflow = create_workflow()
