# Setup Guide for The Daily AI

This guide will walk you through setting up The Daily AI on your local machine.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- OpenAI API key
- Tavily API key

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Siddharth-Patel-Project---The-Daily-AI-Personalized-News-Engine-
```

### 2. Create a Virtual Environment (Recommended)

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- langchain & langchain-openai
- langgraph
- tavily-python
- streamlit
- chromadb
- python-dotenv
- pydantic
- langsmith
- tiktoken
- beautifulsoup4
- lxml
- requests

### 4. Get API Keys

#### OpenAI API Key
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (you won't be able to see it again!)

#### Tavily API Key
1. Go to https://tavily.com/
2. Sign up for an account
3. Get your API key from the dashboard
4. Copy the key

### 5. Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit the `.env` file and add your API keys:
```
OPENAI_API_KEY=sk-your-actual-openai-key-here
TAVILY_API_KEY=tvly-your-actual-tavily-key-here
```

**Optional LangSmith Configuration (for debugging):**
```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-key-here
LANGCHAIN_PROJECT=daily-ai-news
```

### 6. Verify Installation

Run a quick test to ensure everything is set up correctly:

```bash
python -c "import langchain, langgraph, streamlit, chromadb; print('All dependencies installed successfully!')"
```

### 7. Run the Application

**Option A: Web Interface (Recommended)**
```bash
streamlit run app.py
```

The application will open in your browser at http://localhost:8501

**Option B: Command-Line Test**
```bash
python test_workflow.py "Latest AI developments"
```

## Troubleshooting

### Issue: "Module not found" errors

**Solution:** Make sure you've activated your virtual environment and installed all dependencies:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: "API key not found" errors

**Solution:** 
1. Check that your `.env` file exists in the project root
2. Verify that the API keys are correctly set (no quotes, no extra spaces)
3. Make sure the `.env` file is not in `.gitignore` (it should be, but you need to create it locally)

### Issue: ChromaDB errors

**Solution:** ChromaDB will create a local database automatically. If you encounter issues:
```bash
rm -rf chroma_db/  # Delete the database
# Then run the app again
```

### Issue: Streamlit port already in use

**Solution:** Use a different port:
```bash
streamlit run app.py --server.port 8502
```

### Issue: OpenAI rate limits

**Solution:** 
- Wait a few moments and try again
- Consider upgrading your OpenAI plan
- Use a different model in `.env`: `OPENAI_MODEL=gpt-3.5-turbo`

## Testing the Application

### Quick Test
1. Open the web interface
2. Enter a simple topic: "Latest tech news"
3. Select "Blog Post" format
4. Click "Generate News Story"
5. Wait for the agents to complete their work (30-60 seconds)

### Expected Behavior
- Progress bar should update through different stages
- You should see status messages for each agent
- Final output should include:
  - A formatted article
  - Source links
  - Fact-check results

## Project Structure

```
.
├── app.py                  # Main Streamlit application
├── test_workflow.py        # CLI testing script
├── requirements.txt        # Python dependencies
├── .env                    # Your API keys (create this!)
├── .env.example           # Template for .env
├── README.md              # Main documentation
├── SETUP.md               # This file
└── src/
    ├── config.py          # Configuration
    ├── state.py           # State definitions
    ├── agents/            # Agent implementations
    ├── graph/             # LangGraph workflow
    ├── rag/               # Vector store
    ├── tools/             # External tools
    └── utils/             # Utilities
```

## Next Steps

1. Try different topics and formats
2. Explore the source code to understand how it works
3. Review the fact-check results
4. Check the sources used
5. Download outputs as Markdown

## Getting Help

If you encounter issues:
1. Check the error message carefully
2. Review this setup guide
3. Check the main README.md for more information
4. Verify your API keys are valid
5. Ensure you have internet connectivity (needed for API calls)

## Development Tips

- Use LangSmith for debugging (set `LANGCHAIN_TRACING_V2=true`)
- Check the terminal output for detailed logs
- The ChromaDB database persists between runs
- You can clear the vector database by deleting the `chroma_db/` folder

## Success Criteria

You'll know everything is working when:
- ✅ Streamlit app opens without errors
- ✅ You can enter a topic and select a format
- ✅ The workflow completes without errors
- ✅ You receive a formatted article with sources
- ✅ Fact-check results are displayed

Enjoy using The Daily AI! 📰✨
