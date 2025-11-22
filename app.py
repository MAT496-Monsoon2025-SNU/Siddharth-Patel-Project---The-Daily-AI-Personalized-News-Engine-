"""
The Daily AI - Streamlit Application
A personalized news generation engine that transforms news into engaging content.
"""

import streamlit as st
from src.state import NewsState
from src.graph.workflow import news_workflow
from src.utils.formatters import content_formatter
import os

# Page configuration
st.set_page_config(
    page_title="The Daily AI",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Input Styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 0.5rem 1rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Example Pills */
    .example-pill {
        display: inline-block;
        background-color: #f7fafc;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
        font-size: 0.9rem;
        color: #4a5568;
        transition: all 0.2s;
    }
    
    .example-pill:hover {
        background-color: #ebf4ff;
        border-color: #667eea;
        color: #5a67d8;
    }
    
    /* Footer Styling */
    .footer {
        text-align: center;
        color: #718096;
        padding: 2rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 3rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <div class="header-title">📰 The Daily AI</div>
    <div class="header-subtitle">Transform news into engaging stories in your preferred format</div>
</div>
""", unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Check for API keys
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    has_tavily = bool(os.getenv("TAVILY_API_KEY"))
    
    if has_openai:
        st.success("✅ OpenAI API Key configured")
    else:
        st.error("❌ OpenAI API Key missing")
        st.info("Add OPENAI_API_KEY to your .env file")
    
    if has_tavily:
        st.success("✅ Tavily API Key configured")
    else:
        st.error("❌ Tavily API Key missing")
        st.info("Add TAVILY_API_KEY to your .env file")
    
    st.divider()
    
    st.header("🎛️ Settings")
    creativity = st.slider(
        "Creativity Level",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        help="Higher values make the content more creative, lower values make it more factual."
    )
    
    st.divider()
    
    st.header("📚 About")
    st.markdown("""
    **The Daily AI** uses advanced AI agents to:
    - 🔍 Research latest news
    - 📝 Select interesting angles
    - ✍️ Write engaging content
    - ✅ Fact-check for accuracy
    
    Built with **LangGraph** for MAT496.
    """)

# Main content area
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.markdown("### 🎯 What would you like to read about?")
    
    # Example topics
    example_topics = ["Latest AI Breakthroughs", "SpaceX Starship", "Global Climate Summit", "Premier League Highlights"]
    
    # Create columns for example buttons
    cols = st.columns(len(example_topics))
    selected_example = None
    
    # This is a workaround to make "pill" buttons that update the input
    # We use session state to track if an example was clicked
    if 'topic_input' not in st.session_state:
        st.session_state.topic_input = ""
        
    def set_topic(t):
        st.session_state.topic_input = t
    
    # Display example buttons
    st.markdown('<div style="margin-bottom: 10px; font-size: 0.9rem; color: #666;">Try these:</div>', unsafe_allow_html=True)
    ex_cols = st.columns(len(example_topics))
    for i, ex in enumerate(example_topics):
        if ex_cols[i].button(ex, key=f"ex_{i}", use_container_width=True):
            st.session_state.topic_input = ex

    topic = st.text_input(
        "Enter a news topic",
        value=st.session_state.topic_input,
        placeholder="e.g., Latest AI developments, Climate summit, SpaceX launch...",
        help="Enter any news topic you're interested in",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("### 🎨 Choose your format")
    format_type = st.selectbox(
        "Content format",
        options=["blog", "vintage", "professional", "social_thread"],
        format_func=lambda x: {
            "blog": "📝 Blog Post",
            "vintage": "📜 Vintage Newspaper",
            "professional": "📊 Professional Report",
            "social_thread": "🧵 Social Thread"
        }[x],
        help="Choose how you want the news presented",
        label_visibility="collapsed"
    )

# Generate button
st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 Generate News Story", type="primary", use_container_width=True):
    if not topic:
        st.warning("⚠️ Please enter a news topic first!")
    elif not has_openai or not has_tavily:
        st.error("❌ Please configure your API keys in the .env file")
    else:
        try:
            # Initialize state
            initial_state = NewsState(
                topic=topic,
                format_type=format_type
            )
            
            # Use st.status for a better loading experience
            with st.status("🤖 AI Agents at work...", expanded=True) as status:
                st.write("🔧 Initializing workflow...")
                
                # Execute workflow
                final_state = None
                for state in news_workflow.stream(initial_state):
                    # Update status based on which node completed
                    if "research" in state:
                        st.write("🔍 **Researcher Agent**: Analyzing news sources...")
                    elif "editor" in state:
                        st.write("📝 **Editor Agent**: Selecting the best angle...")
                    elif "journalist" in state:
                        st.write("✍️ **Journalist Agent**: Drafting the story...")
                    elif "fact_check" in state:
                        st.write("✅ **Fact-Checker Agent**: Verifying accuracy...")
                    
                    # Get the latest state
                    state_value = list(state.values())[0]
                    if isinstance(state_value, dict):
                        final_state = NewsState(**state_value)
                    else:
                        final_state = state_value
                
                status.update(label="✨ Story Ready!", state="complete", expanded=False)
            
            # Display results
            if final_state and hasattr(final_state, 'generated_content') and final_state.generated_content:
                st.success("🎉 Your personalized news story is ready!")
                
                # Use tabs to organize content
                tab1, tab2, tab3 = st.tabs(["📖 The Story", "🔍 Behind the Scenes", "📥 Download"])
                
                with tab1:
                    formatted_content = content_formatter.format_for_display(final_state.generated_content)
                    st.markdown(formatted_content, unsafe_allow_html=True)
                    
                    # Feedback buttons
                    st.markdown("---")
                    st.markdown("### How was this story?")
                    fb_col1, fb_col2, _ = st.columns([1, 1, 10])
                    with fb_col1:
                        st.button("👍 Great")
                    with fb_col2:
                        st.button("👎 Needs Work")
                
                with tab2:
                    st.markdown("### 📚 Sources Used")
                    sources_text = content_formatter.format_sources(final_state.generated_content.sources_used)
                    st.markdown(sources_text)
                    
                    st.divider()
                    
                    st.markdown("### ✅ Fact-Check Report")
                    if final_state.fact_check:
                        fc = final_state.fact_check
                        if fc.is_accurate:
                            st.success(f"Content verified as accurate (Confidence: {fc.confidence_score:.0%})")
                        else:
                            st.warning(f"Some issues detected (Confidence: {fc.confidence_score:.0%})")
                        
                        if fc.issues_found:
                            st.markdown("**Issues Found:**")
                            for issue in fc.issues_found:
                                st.markdown(f"- {issue}")
                
                with tab3:
                    st.markdown("### 📥 Download Story")
                    st.markdown("Get a copy of your story in Markdown format.")
                    st.download_button(
                        label="Download Markdown File",
                        data=formatted_content,
                        file_name=f"{topic.replace(' ', '_')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
            
            elif final_state and hasattr(final_state, 'error_message') and final_state.error_message:
                st.error(f"❌ Error: {final_state.error_message}")
            else:
                st.error("❌ Something went wrong. Please try again.")
        
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.exception(e)

# Footer
st.markdown("""
<div class="footer">
    Built with ❤️ using LangGraph, OpenAI, and Streamlit | MAT496 Capstone Project
</div>
""", unsafe_allow_html=True)
