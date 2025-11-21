# Course Topics Coverage - MAT496

This document demonstrates how The Daily AI project covers all required MAT496 topics.

## 1. Prompting ✅

### Location
- `src/utils/prompts.py`

### Implementation
The project uses sophisticated prompting techniques:

#### System Prompts
Each agent has a specialized system prompt defining its role:
- **Researcher**: Extracts facts from search results
- **Editor**: Selects interesting angles
- **Journalist**: Writes in specific styles
- **Fact-Checker**: Verifies accuracy

#### Style-Specific Prompts
Different prompts for each output format:
```python
JOURNALIST_SYSTEM_PROMPTS = {
    "blog": "You are a creative blog writer...",
    "vintage": "You are a vintage newspaper journalist from the 1920s-1940s...",
    "professional": "You are a professional analyst...",
    "social_thread": "You are a social media expert..."
}
```

#### Dynamic Prompt Construction
Prompts are dynamically constructed with context:
```python
def get_journalist_prompt(format_type, topic, angle, tone, key_points, source_material):
    # Combines format-specific system prompt with dynamic user prompt
```

### Demonstration
Run the app and try different formats to see how prompts affect output style.

---

## 2. Structured Output ✅

### Location
- `src/state.py`

### Implementation
Extensive use of Pydantic models for type-safe, structured data:

#### State Models
```python
class NewsState(BaseModel):
    topic: str
    format_type: Literal["blog", "vintage", "professional", "social_thread"]
    research_results: Optional[ResearchResults]
    editorial_angle: Optional[EditorialAngle]
    generated_content: Optional[GeneratedContent]
    fact_check: Optional[FactCheckResult]
    # ... more fields
```

#### Agent Output Models
Each agent returns structured output:
- `ResearchResults`: Articles, key facts, summary
- `EditorialAngle`: Angle, reasoning, tone, key points
- `GeneratedContent`: Title, content, format, word count, sources
- `FactCheckResult`: Accuracy, issues, suggestions, confidence

### Benefits
- Type safety throughout the pipeline
- Clear data contracts between agents
- Easy validation and error handling
- Self-documenting code

---

## 3. Semantic Search ✅

### Location
- `src/rag/vector_store.py`

### Implementation
ChromaDB-based vector store for semantic search:

```python
class VectorStore:
    def semantic_search(self, query: str, n_results: int = 3) -> List[dict]:
        """Perform semantic search to find relevant articles."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return formatted_results
```

### Use Cases
1. **Storing Articles**: Research results are embedded and stored
2. **Finding Context**: Semantic search retrieves relevant articles
3. **Refinement**: Uses similar articles to improve content

### Demonstration
The vector store automatically:
- Embeds article content
- Performs similarity search
- Returns most relevant results

---

## 4. RAG (Retrieval Augmented Generation) ✅

### Location
- `src/rag/vector_store.py`
- `src/graph/workflow.py` (refinement node)

### Implementation

#### Context Retrieval
```python
def get_context_for_topic(self, topic: str, query: Optional[str] = None, 
                         n_results: int = 5) -> str:
    """Get relevant context for a topic to augment generation (RAG)."""
    results = self.semantic_search(search_query, n_results)
    # Format context for LLM consumption
    return formatted_context
```

#### RAG in Refinement
```python
def refinement_node(state: NewsState) -> NewsState:
    """Uses RAG to get additional context and refine content."""
    additional_context = vector_store.get_context_for_topic(
        state.topic, 
        query, 
        n_results=3
    )
    # Use context to improve content
```

### Benefits
- Grounds generation in retrieved facts
- Improves accuracy
- Provides additional context
- Enables fact-checking

---

## 5. Tool Calling & MCP ✅

### Location
- `src/tools/tavily_search.py`
- `src/agents/researcher.py`

### Implementation

#### Tavily Tool Wrapper
```python
class TavilySearchTool:
    def search_news(self, query: str, max_results: int = None) -> List[NewsArticle]:
        """Search for news articles using Tavily."""
        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
            topic="news"
        )
        # Convert to structured NewsArticle objects
        return articles
```

#### Tool Usage in Agent
```python
def research(self, state: NewsState) -> NewsState:
    """Research a topic using Tavily search."""
    articles = tavily_search.search_news(topic)  # Tool calling
    # Process results with LLM
    return updated_state
```

### Features
- Real-time news search
- Advanced search depth
- News-specific filtering
- Structured result parsing

---

## 6. LangGraph: State, Nodes, Graph ✅

### Location
- `src/graph/workflow.py`

### Implementation

#### State Definition
```python
workflow = StateGraph(NewsState)
```

#### Nodes
Six specialized nodes:
1. **research**: Searches for news
2. **store_vectors**: Stores in vector DB
3. **editor**: Selects angle
4. **journalist**: Writes content
5. **fact_check**: Verifies accuracy
6. **refine**: Improves content with RAG

#### Graph Structure
```python
workflow.add_node("research", research_node)
workflow.add_node("store_vectors", store_in_vector_db_node)
workflow.add_node("editor", editor_node)
workflow.add_node("journalist", journalist_node)
workflow.add_node("fact_check", fact_check_node)
workflow.add_node("refine", refinement_node)
```

#### Conditional Edges
```python
workflow.add_conditional_edges(
    "research",
    should_continue_after_research,
    {"continue": "store_vectors", "end": END}
)

workflow.add_conditional_edges(
    "fact_check",
    should_refine,
    {"refine": "refine", "end": END}
)
```

#### Workflow Execution
```python
for state in news_workflow.stream(initial_state):
    # Process each node's output
    final_state = list(state.values())[0]
```

### Features
- State management across nodes
- Conditional routing
- Error handling
- Iterative refinement
- Complete workflow orchestration

---

## Summary

| Topic | Implementation | Files | Complexity |
|-------|---------------|-------|------------|
| Prompting | Style-specific system & user prompts | `prompts.py` | ⭐⭐⭐⭐ |
| Structured Output | Pydantic models for all data | `state.py` | ⭐⭐⭐⭐ |
| Semantic Search | ChromaDB vector search | `vector_store.py` | ⭐⭐⭐⭐ |
| RAG | Context retrieval for generation | `vector_store.py`, `workflow.py` | ⭐⭐⭐⭐⭐ |
| Tool Calling | Tavily API integration | `tavily_search.py` | ⭐⭐⭐ |
| LangGraph | Complete workflow orchestration | `workflow.py` | ⭐⭐⭐⭐⭐ |

**Total Coverage: 100%** ✅

All six MAT496 topics are comprehensively implemented with production-quality code.

---

## How to Verify

1. **Prompting**: Check `src/utils/prompts.py` and try different formats in the UI
2. **Structured Output**: Review `src/state.py` Pydantic models
3. **Semantic Search**: See `semantic_search()` in `src/rag/vector_store.py`
4. **RAG**: Check `get_context_for_topic()` and `refinement_node()`
5. **Tool Calling**: Review `src/tools/tavily_search.py` and its usage
6. **LangGraph**: Study `src/graph/workflow.py` for complete workflow

Run the application to see all topics working together in a real-world use case!
