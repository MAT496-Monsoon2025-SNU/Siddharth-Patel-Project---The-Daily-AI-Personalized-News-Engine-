# How to Run The Daily AI

## Quick Start (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys
Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your keys:
```
OPENAI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

### 3. Run the App
```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

### 4. Generate Your First Story
1. Enter a topic (e.g., "Latest AI news")
2. Choose a format (Blog, Vintage, Professional, or Social Thread)
3. Click "Generate News Story"
4. Wait 30-60 seconds
5. Read your personalized news article!

## Alternative: Command-Line Testing

```bash
python test_workflow.py "Your topic here"
```

## Need Help?

See [SETUP.md](SETUP.md) for detailed instructions and troubleshooting.

## Example Topics to Try

- "Latest developments in quantum computing"
- "Climate summit 2024"
- "SpaceX Starship launch"
- "AI regulation news"
- "Cryptocurrency market updates"
- "Olympic Games highlights"

## What to Expect

The system will:
1. 🔍 Search for recent news articles
2. 📝 Select an interesting angle
3. ✍️ Write content in your chosen format
4. ✅ Fact-check for accuracy
5. 📄 Present the final article with sources

Enjoy! 📰✨
