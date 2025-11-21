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
    
    /* Card Styling */
    .css-1r6slb0 {
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
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
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
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
    
    st.header("📚 About")
    st.markdown("""
    **The Daily AI** uses advanced AI agents to:
    - 🔍 Research latest news
    - 📝 Select interesting angles
    - ✍️ Write engaging content
    - ✅ Fact-check for accuracy
    
    Built with **LangGraph** for MAT496.
    """)
    
    st.divider()
    
    st.header("🎓 Course Topics Covered")
    st.markdown("""
    - ✅ Prompting
    - ✅ Structured Output
    - ✅ Semantic Search
    - ✅ RAG
    - ✅ Tool Calling
    - ✅ LangGraph
    """)

# Main content area
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.markdown("### 🎯 What would you like to read about?")
    topic = st.text_input(
        "Enter a news topic",
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
        # Create progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Initialize state
            status_text.markdown("**🔧 Initializing...**")
            progress_bar.progress(10)
            
            initial_state = NewsState(
                topic=topic,
                format_type=format_type
            )
            
            # Run the workflow
            status_text.markdown("**🔍 Researching news articles...**")
            progress_bar.progress(25)
            
            # Execute workflow
            final_state = None
            for state in news_workflow.stream(initial_state):
                # Update progress based on which node completed
                if "research" in state:
                    status_text.markdown("**📰 Analyzing research results...**")
                    progress_bar.progress(40)
                elif "editor" in state:
                    status_text.markdown("**📝 Selecting editorial angle...**")
                    progress_bar.progress(60)
                elif "journalist" in state:
                    status_text.markdown("**✍️ Writing content...**")
                    progress_bar.progress(80)
                elif "fact_check" in state:
                    status_text.markdown("**✅ Fact-checking...**")
                    progress_bar.progress(90)
                
                # Get the latest state - convert dict to NewsState if needed
                state_value = list(state.values())[0]
                if isinstance(state_value, dict):
                    final_state = NewsState(**state_value)
                else:
                    final_state = state_value
            
            progress_bar.progress(100)
            status_text.markdown("**✨ Complete!**")
            
            # Display results
            if final_state and hasattr(final_state, 'generated_content') and final_state.generated_content:
                st.success("🎉 Your personalized news story is ready!")
                
                # Display the content with HTML styling
                st.divider()
                formatted_content = content_formatter.format_for_display(final_state.generated_content)
                st.markdown(formatted_content, unsafe_allow_html=True)
                
                # Display sources in an expander
                with st.expander("📚 View Sources"):
                    sources_text = content_formatter.format_sources(final_state.generated_content.sources_used)
                    st.markdown(sources_text)
                
                # Display fact-check results
                if final_state.fact_check:
                    with st.expander("🔍 Fact-Check Results"):
                        fc = final_state.fact_check
                        
                        if fc.is_accurate:
                            st.success(f"✅ Content verified as accurate (Confidence: {fc.confidence_score:.0%})")
                        else:
                            st.warning(f"⚠️ Some issues detected (Confidence: {fc.confidence_score:.0%})")
                        
                        if fc.issues_found:
                            st.markdown("**Issues Found:**")
                            for issue in fc.issues_found:
                                st.markdown(f"- {issue}")
                        
                        if fc.suggestions:
                            st.markdown("**Suggestions:**")
                            for suggestion in fc.suggestions:
                                st.markdown(f"- {suggestion}")
                
                # Download button
                st.divider()
                col_download, _ = st.columns([1, 2])
                with col_download:
                    st.download_button(
                        label="📥 Download as Markdown",
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
