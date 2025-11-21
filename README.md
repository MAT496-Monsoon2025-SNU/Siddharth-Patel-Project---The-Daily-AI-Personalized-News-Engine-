# The Daily AI: Personalized News Engine

## Overview
"The Daily AI" is a personalized news generation agent designed to make reading news interesting again. Instead of dry, static reports, this tool allows users to search for a topic, and the AI agent—acting as a dynamic editorial team—researches the latest events and crafts an engaging story in the user's preferred format (e.g., a witty blog post, vintage newspaper article, professional report, or social media thread). It solves the problem of "boring news" by injecting style, context, and narrative flair into current events.

## Reason for picking up this project
This project aligns perfectly with the MAT496 course content by transforming a standard "search and summarize" task into a creative, multi-step agentic workflow:

- **LangGraph**: Models the editorial pipeline: `Research` → `Store in Vector DB` → `Angle Selection` → `Drafting` → `Fact-Checking` → `Refinement`
- **Tool Calling**: Uses live search tools (Tavily) to fetch real-time news, which is critical for a news assistant
- **Structured Output**: Uses Pydantic models to ensure consistent data flow between agents (NewsState, ResearchResults, EditorialAngle, GeneratedContent, FactCheckResult)
- **Prompting**: Heavy use of "Style Transfer" prompting to make content engaging across different formats (blog, vintage, professional, social thread)
- **Semantic Search**: ChromaDB integration for finding relevant context from stored articles
- **RAG (Retrieval Augmented Generation)**: Uses vector store to retrieve relevant context during fact-checking and refinement
- **Creativity**: Addresses real-world information overload by focusing on *engagement* and *personalization*

## Architecture

### Multi-Agent System
The system uses four specialized agents:

1. **Researcher Agent** (`src/agents/researcher.py`)
   - Searches for news using Tavily API
   - Extracts key facts and summarizes findings
   - Demonstrates: Tool Calling, Structured Output

2. **Editor Agent** (`src/agents/editor.py`)
   - Analyzes research results
   - Selects interesting editorial angles
   - Determines appropriate tone
   - Demonstrates: Prompting, Structured Output

3. **Journalist Agent** (`src/agents/journalist.py`)
   - Writes content in the selected format
   - Applies style-specific prompts
   - Demonstrates: Advanced Prompting, Style Transfer

4. **Fact-Checker Agent** (`src/agents/fact_checker.py`)
   - Verifies content accuracy
   - Suggests improvements
   - Demonstrates: RAG, Semantic Search

### LangGraph Workflow
```
START → Research → Store in Vector DB → Editor → Journalist → Fact Check
                                                                    ↓
                                                    [Needs Refinement?]
                                                                    ↓
                                                    Refine ← (uses RAG)
                                                                    ↓
                                                              Journalist
                                                                    ↓
                                                                  END
```

### Technology Stack
- **LangGraph**: Workflow orchestration
- **LangChain**: LLM integration
- **OpenAI**: Language model (GPT-4o-mini)
- **Tavily**: Real-time news search
- **ChromaDB**: Vector database for semantic search
- **Streamlit**: Web interface
- **Pydantic**: Data validation and structured output

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Siddharth-Patel-Project---The-Daily-AI-Personalized-News-Engine-
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

**Getting API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Tavily: https://tavily.com/

### 4. Run the Application

**Option A: Web Interface (Recommended)**
```bash
streamlit run app.py
```
Then open your browser to http://localhost:8501

**Option B: Command-Line Test**
```bash
python test_workflow.py "Your news topic here"
```

## Usage Guide

### Using the Web Interface

1. **Enter a Topic**: Type any news topic you're interested in
   - Examples: "Latest AI developments", "Climate summit 2024", "SpaceX launch"

2. **Choose a Format**:
   - 📝 **Blog Post**: Casual, engaging, conversational
   - 📜 **Vintage Newspaper**: Classic 1920s-1940s journalism style
   - 📊 **Professional Report**: Analytical, data-driven, formal
   - 🧵 **Social Media Thread**: Concise, punchy, thread format

3. **Click "Generate News Story"**: Watch the progress as agents work:
   - 🔍 Researching articles
   - 📝 Selecting editorial angle
   - ✍️ Writing content
   - ✅ Fact-checking

4. **Review Results**: 
   - Read the generated content
   - Check sources
   - View fact-check results
   - Download as Markdown

### Example Outputs

**Topic**: "Latest developments in quantum computing"

**Blog Format**:
```
# Quantum Leap: The Race to Build the Ultimate Computer

Hey there, tech enthusiasts! 🚀 Let me tell you about something that's 
absolutely mind-blowing happening in the world of computing right now...
```

**Vintage Format**:
```
QUANTUM COMPUTING BREAKTHROUGH ANNOUNCED

In a development that promises to revolutionize the field of computational 
science, researchers at leading institutions have achieved remarkable 
progress in the realm of quantum computing...
```

## Project Structure
```
.
├── app.py                      # Streamlit web application
├── test_workflow.py            # CLI test script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
└── src/
    ├── config.py              # Configuration management
    ├── state.py               # Pydantic state models
    ├── agents/
    │   ├── researcher.py      # Research agent
    │   ├── editor.py          # Editorial agent
    │   ├── journalist.py      # Writing agent
    │   └── fact_checker.py    # Fact-checking agent
    ├── graph/
    │   └── workflow.py        # LangGraph workflow
    ├── rag/
    │   └── vector_store.py    # ChromaDB integration
    ├── tools/
    │   └── tavily_search.py   # Tavily API wrapper
    └── utils/
        ├── prompts.py         # Prompt templates
        └── formatters.py      # Output formatters
```

## Plan

I plan to execute these steps to complete my project.

- [DONE] Step 1: Project initialization. Setup git, environment, and define the `NewsState` for the agent.
- [DONE] Step 2: Implement the "News Room" Agents. Create the `Researcher` (finds facts) and the `Editor` (chooses the angle).
- [DONE] Step 3: Implement the "Journalist" Node. This node will take the facts and the chosen angle to write the content in the specific format (Blog/Article/Vintage/Social).
- [DONE] Step 4: Build the LangGraph. Connect the workflow: Search → Analyze → Write → Refine.
- [DONE] Step 5: Build the UI. A Streamlit app where users enter a topic (e.g., "SpaceX Launch") and pick a style (e.g., "Excited Blog").
- [TODO] Step 6: Testing & Verification. Verify the "fun factor" of the output and ensure facts remain accurate despite the stylistic flair.

## Course Topics Coverage

### ✅ Prompting
- Multiple style-specific prompts in `src/utils/prompts.py`
- System prompts for each agent role
- Format-specific journalist prompts (blog, vintage, professional, social)

### ✅ Structured Output
- Pydantic models in `src/state.py`:
  - `NewsState`: Main workflow state
  - `ResearchResults`: Research agent output
  - `EditorialAngle`: Editor agent output
  - `GeneratedContent`: Journalist agent output
  - `FactCheckResult`: Fact-checker agent output

### ✅ Semantic Search
- ChromaDB integration in `src/rag/vector_store.py`
- `semantic_search()` method for finding relevant articles
- Vector embeddings for news content

### ✅ RAG (Retrieval Augmented Generation)
- `get_context_for_topic()` in vector store
- Refinement node uses RAG to improve content
- Fact-checker retrieves context for verification

### ✅ Tool Calling & MCP
- Tavily API integration in `src/tools/tavily_search.py`
- Real-time news search functionality
- External API integration pattern

### ✅ LangGraph: State, Nodes, Graph
- Complete workflow in `src/graph/workflow.py`
- 6 nodes: research, store_vectors, editor, journalist, fact_check, refine
- Conditional edges for dynamic routing
- State management throughout pipeline

## Conclusion
[To be filled upon completion of Step 6]

I had planned to achieve an autonomous multi-agent news generation system that covers all MAT496 topics while being creative and practical. I think I have/have-not achieved the conclusion satisfactorily. The reason for your satisfaction/unsatisfaction.

## Future Enhancements
- Add more output formats (podcast script, infographic text, etc.)
- Implement user preferences and history
- Add multi-language support
- Create API endpoints for programmatic access
- Add image generation for articles
- Implement caching for faster responses

## License
MIT License - Created for MAT496 Capstone Project

## Acknowledgments
- Course: MAT496 - Advanced Topics in AI
- Instructor: [Your Instructor's Name]
- Tools: LangGraph, LangChain, OpenAI, Tavily, ChromaDB, Streamlit
