# The Daily AI: Personalized News Engine

Transform dry news articles into engaging content in multiple formats using AI agents.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview
**The Daily AI** is an intelligent, multi-agent news generation system designed to transform how we consume information. In an era of information overload, this project leverages advanced Large Language Models (LLMs) to not just summarize news, but to re-contextualize and present it in engaging, personalized formats.

Using a sophisticated architecture powered by **LangGraph**, the system orchestrates a team of specialized AI agents—a **Researcher** 🔍, an **Editor** 📝, a **Journalist** ✍️, and a **Fact-Checker** ✅—to autonomously research topics, select compelling angles, write high-quality narratives, and verify facts. Whether you want your news delivered as a **1920s vintage newspaper** 📜, a **casual blog post** 💻, a **professional executive summary** 📊, or a **viral social media thread** 🧵, The Daily AI adapts the content while maintaining strict factual accuracy.

## 💡 Reason for picking up this project
This project was chosen because it perfectly encapsulates and applies the advanced concepts learned in **MAT496**. It moves beyond simple chatbot interactions to build a complex, autonomous system.

*   **🕸️ LangGraph & Multi-Agent Orchestration**: The core of the project is a cyclic graph managing the state between multiple agents. This demonstrates mastery of `State`, `Nodes`, and `Graph` concepts, specifically how to handle complex workflows with conditional edges (e.g., sending an article back for revision if fact-checking fails).
*   **🛠️ Tool Calling (MCP)**: The Researcher agent actively uses external tools (**Tavily API**) to fetch real-time data from the web, showcasing the ability of LLMs to interact with the outside world.
*   **📋 Structured Output**: To ensure the agents communicate effectively, strict **Pydantic** models are used. This enforces structured output (JSON) from the LLMs, which is critical for reliable system performance.
*   **🧠 Retrieval Augmented Generation (RAG)**: The system utilizes **ChromaDB** for semantic search, allowing it to retrieve relevant context and historical data to enrich the news stories, ensuring the content is not just current but also contextual.
*   **🎭 Prompting**: Advanced prompting techniques, including persona adoption and chain-of-thought reasoning, are implemented to guide each agent's specific behavior (e.g., the "Vintage Journalist" persona).
*   **✨ Creativity**: This project addresses a real-world problem—boring news—with a creative solution. It pushes the boundaries of what's possible by "outsourcing" the entire editorial process to a team of AI agents, something that would be impossible with traditional software engineering.

## 📋 Plan
I planned to execute these steps to complete my project. Each step represents a significant unit of work in building this system.

*   ✅ **[DONE] Step 1: Project Initialization & Environment Setup**
    *   Initialized the Git repository and set up the Python environment with necessary dependencies (`langgraph`, `langchain`, `streamlit`, `chromadb`). Configured secure environment variable handling for OpenAI and Tavily API keys.
*   ✅ **[DONE] Step 2: Architecture & State Design**
    *   Designed the global `AgentState` using Pydantic to track the flow of data (news topic, raw research, drafts, critique) between agents. Defined the graph topology including the feedback loops for quality control.
*   ✅ **[DONE] Step 3: Semantic Search Infrastructure (RAG)**
    *   Implemented the vector store using ChromaDB. Created utility functions to embed text and perform semantic retrieval, enabling the system to find related historical context for any given news topic.
*   ✅ **[DONE] Step 4: Researcher Agent Implementation**
    *   Built the Researcher node capable of utilizing the Tavily Search API. Implemented logic to parse raw search results and synthesize them into a comprehensive briefing document for the Editor.
*   ✅ **[DONE] Step 5: Editor Agent Development**
    *   Developed the Editor agent responsible for analyzing the research brief. Engineered prompts to have the Editor select the most engaging "angle" or "hook" for the story based on the user's requested format.
*   ✅ **[DONE] Step 6: Journalist Agent & Style Transfer Engine**
    *   Created the Journalist agent with dynamic prompt templates. Implemented the logic to swap writing styles (Vintage, Professional, Blog, Social Media) based on user input, ensuring the tone matches the desired output.
*   ✅ **[DONE] Step 7: Fact-Checker Agent & Verification Loop**
    *   Implemented a critical safety layer: the Fact-Checker agent. This agent compares the generated draft against the original research citations. If discrepancies are found, it triggers a conditional edge in the graph to send the draft back to the Journalist for revision.
*   ✅ **[DONE] Step 8: Graph Construction & Orchestration**
    *   Assembled the LangGraph workflow, connecting all nodes (Researcher -> Editor -> Journalist -> Fact-Checker). Defined the conditional routing logic to handle the "Approve" vs. "Revise" paths.
*   ✅ **[DONE] Step 9: Streamlit Web Interface**
    *   Built a responsive frontend using Streamlit. Created input forms for topic selection and format preferences, and implemented real-time status updates to show the user which agent is currently working.
*   ✅ **[DONE] Step 10: Testing & Refinement**
    *   Conducted extensive testing with various news topics to ensure robustness. Refined agent prompts to reduce hallucinations and improve the distinctiveness of the different writing styles.
*   ✅ **[DONE] Step 11: Documentation & Final Polish**
    *   Completed the project documentation, including setup guides and this comprehensive report. Cleaned up the codebase and ensured all type hints and comments were up to standard.

## 🏁 Conclusion
I had planned to achieve a fully autonomous news agency that could mimic human editorial processes. I think I have achieved the conclusion satisfactorily. The system not only functions technically—successfully routing state between agents and calling external tools—but it also delivers on the creative promise. The "Vintage Newspaper" mode, in particular, demonstrates how LLMs can be used to completely reimagine content presentation. The inclusion of the self-correcting fact-check loop ensures that the creativity does not come at the cost of accuracy, fulfilling the rigorous requirements of a modern AI application.

## 🚀 Installation & Usage Instructions
To replicate the results of this project, a specific environment configuration is required.

### 📦 Prerequisites
*   🐍 Python 3.8+
*   🔑 OpenAI API Key (for GPT-4o-mini)
*   🌐 Tavily API Key (for real-time news search)

### 🛠️ Setup Steps
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/MAT496-Monsoon2025-SNU/Siddharth-Patel-Project---The-Daily-AI-Personalized-News-Engine-.git
    cd Siddharth-Patel-Project---The-Daily-AI-Personalized-News-Engine-
    ```
2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Environment Configuration**
    Create a `.env` file in the root directory:
    ```bash
    cp .env.example .env
    ```
    Populate it with your credentials:
    ```
    OPENAI_API_KEY=sk-...
    TAVILY_API_KEY=tvly-...
    ```

### ▶️ Running the Application
**Option 1: Streamlit Web Interface (Recommended)**
This launches the full interactive UI where you can visualize the agent workflow.
```bash
streamlit run app.py
```

**Option 2: Command Line Interface**
For quick testing of the agent graph without the UI overhead.
```bash
python test_workflow.py "Your News Topic"
```

## 🙏 Acknowledgments
*   **🎓 Course Instructor**: For the guidance on Agentic AI and LangGraph concepts.
*   **🦜🔗 LangChain & LangGraph**: For the robust orchestration framework.
*   **🔍 Tavily**: For the search API.
*   **👑 Streamlit**: For the rapid UI development framework.
