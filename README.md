# The Daily AI: Personalized News Engine

Transform dry news articles into engaging content in multiple formats using AI agents.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

**The Daily AI** is an intelligent news generation system that transforms standard news articles into engaging content in your preferred format. Using a multi-agent architecture powered by LangGraph, it researches topics, selects interesting angles, and crafts compelling stories while maintaining factual accuracy.

### Key Features

- 🔍 **Real-time News Research** - Searches latest articles using Tavily API
- 📝 **Multiple Output Formats** - Blog posts, vintage newspaper, professional reports, social media threads
- 🤖 **Multi-Agent System** - Specialized AI agents for research, editing, writing, and fact-checking
- ✅ **Fact Verification** - Automated fact-checking with confidence scoring
- 🎨 **Style Transfer** - Maintains facts while adapting tone and style
- 💾 **Semantic Search** - ChromaDB vector store for context retrieval

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/MAT496-Monsoon2025-SNU/Siddharth-Patel-Project---The-Daily-AI-Personalized-News-Engine-.git
cd Siddharth-Patel-Project---The-Daily-AI-Personalized-News-Engine-

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env and add your OpenAI and Tavily API keys
```

### Running the Application

**Web Interface:**
```bash
streamlit run app.py
```
Open http://localhost:8501 in your browser.

**Command Line:**
```bash
python test_workflow.py "Your news topic here"
```

## 📖 Usage

1. **Enter a Topic** - Any news subject you're interested in
2. **Choose a Format**:
   - 📝 Blog Post - Casual and engaging
   - 📜 Vintage Newspaper - Classic 1920s-1940s style
   - 📊 Professional Report - Analytical and formal
   - 🧵 Social Media Thread - Concise tweets
3. **Generate** - Wait 30-60 seconds while AI agents work
4. **Read & Download** - View your personalized article with sources

## 🏗️ Architecture

### Multi-Agent System

```
┌─────────────┐    ┌──────────┐    ┌────────────┐    ┌──────────────┐
│  Researcher │ -> │  Editor  │ -> │ Journalist │ -> │ Fact-Checker │
└─────────────┘    └──────────┘    └────────────┘    └──────────────┘
      ↓                  ↓                ↓                   ↓
   Search            Select           Write              Verify
   News              Angle           Content            Accuracy
```

**Agents:**
- **Researcher** - Searches and analyzes news articles
- **Editor** - Selects interesting angles and tone
- **Journalist** - Writes in format-specific styles
- **Fact-Checker** - Verifies accuracy and suggests improvements

### Technology Stack

| Component | Technology |
|-----------|-----------|
| Workflow Orchestration | LangGraph |
| LLM Integration | LangChain |
| Language Model | OpenAI GPT-4o-mini |
| News Search | Tavily API |
| Vector Database | ChromaDB |
| Web Interface | Streamlit |
| Data Validation | Pydantic |

## 📁 Project Structure

```
.
├── app.py                      # Streamlit web application
├── test_workflow.py            # CLI test script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── src/
    ├── config.py              # Configuration management
    ├── state.py               # Pydantic state models
    ├── agents/                # Agent implementations
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

## 🔧 Configuration

### Required API Keys

- **OpenAI API Key** - Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Tavily API Key** - Get from [Tavily](https://tavily.com/)

### Optional Configuration

```bash
# LangSmith (for debugging)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=daily-ai-news

# Model settings
OPENAI_MODEL=gpt-4o-mini
TEMPERATURE=0.7
```

## 📚 Documentation

- [Setup Guide](SETUP.md) - Detailed installation and configuration
- [Quick Start](QUICKSTART.md) - Get running in 5 minutes
- [Course Topics](COURSE_TOPICS.md) - Technical implementation details
- [Examples](examples/) - Sample outputs in all formats

## 🎨 Example Outputs

See the [examples/](examples/) directory for sample outputs:
- [Blog Post](examples/example_blog.md)
- [Vintage Newspaper](examples/example_vintage.md)
- [Professional Report](examples/example_professional.md)
- [Social Media Thread](examples/example_social_thread.md)

## 🤝 Contributing

This is an academic project for MAT496. Contributions, issues, and feature requests are welcome!

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph) and [LangChain](https://github.com/langchain-ai/langchain)
- News search powered by [Tavily](https://tavily.com/)
- Vector database by [ChromaDB](https://www.trychroma.com/)
- UI built with [Streamlit](https://streamlit.io/)

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Made with ❤️ for MAT496 - Introduction to LLMS**
