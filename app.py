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
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📰 The Daily AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Transform news into engaging stories in your preferred format</div>', unsafe_allow_html=True)

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
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎯 What would you like to read about?")
    topic = st.text_input(
        "Enter a news topic",
        placeholder="e.g., Latest AI developments, Climate summit, SpaceX launch...",
        help="Enter any news topic you're interested in"
    )

with col2:
    st.header("🎨 Choose your format")
    format_type = st.selectbox(
        "Content format",
        options=["blog", "vintage", "professional", "social_thread"],
        format_func=lambda x: {
            "blog": "📝 Blog Post (Casual & Engaging)",
            "vintage": "📜 Vintage Newspaper (Classic Style)",
            "professional": "📊 Professional Report (Analytical)",
            "social_thread": "🧵 Social Media Thread (Concise)"
        }[x],
        help="Choose how you want the news presented"
    )

# Generate button
st.divider()

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
            status_text.text("🔧 Initializing...")
            progress_bar.progress(10)
            
            initial_state = NewsState(
                topic=topic,
                format_type=format_type
            )
            
            # Run the workflow
            status_text.text("🔍 Researching news articles...")
            progress_bar.progress(25)
            
            # Execute workflow
            final_state = None
            for state in news_workflow.stream(initial_state):
                # Update progress based on which node completed
                if "research" in state:
                    status_text.text("📰 Analyzing research results...")
                    progress_bar.progress(40)
                elif "editor" in state:
                    status_text.text("📝 Selecting editorial angle...")
                    progress_bar.progress(60)
                elif "journalist" in state:
                    status_text.text("✍️ Writing content...")
                    progress_bar.progress(80)
                elif "fact_check" in state:
                    status_text.text("✅ Fact-checking...")
                    progress_bar.progress(90)
                
                # Get the latest state - convert dict to NewsState if needed
                state_value = list(state.values())[0]
                if isinstance(state_value, dict):
                    final_state = NewsState(**state_value)
                else:
                    final_state = state_value
            
            progress_bar.progress(100)
            status_text.text("✨ Complete!")
            
            # Display results
            if final_state and hasattr(final_state, 'generated_content') and final_state.generated_content:
                st.success("🎉 Your personalized news story is ready!")
                
                # Display the content
                st.divider()
                formatted_content = content_formatter.format_for_display(final_state.generated_content)
                st.markdown(formatted_content)
                
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
                st.download_button(
                    label="📥 Download as Markdown",
                    data=formatted_content,
                    file_name=f"{topic.replace(' ', '_')}.md",
                    mime="text/markdown"
                )
            
            elif final_state and hasattr(final_state, 'error_message') and final_state.error_message:
                st.error(f"❌ Error: {final_state.error_message}")
            else:
                st.error("❌ Something went wrong. Please try again.")
        
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.exception(e)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    Built with ❤️ using LangGraph, OpenAI, and Streamlit | MAT496 Capstone Project
</div>
""", unsafe_allow_html=True)
