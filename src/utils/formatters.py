"""
Output formatters for different content types with beautiful styling.
"""

from src.state import GeneratedContent


class ContentFormatter:
    """Formats generated content for display with custom styling."""
    
    @staticmethod
    def get_format_css(format_type: str) -> str:
        """Get CSS styling for the specific format."""
        
        if format_type == "blog":
            return """
            <style>
            .blog-container {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 3rem;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                margin: 2rem 0;
            }
            .blog-content {
                background: white;
                padding: 2.5rem;
                border-radius: 15px;
                font-family: 'Georgia', serif;
                line-height: 1.8;
                color: #2d3748;
            }
            .blog-title {
                color: #667eea;
                font-size: 2.5rem;
                font-weight: bold;
                margin-bottom: 1.5rem;
                font-family: 'Helvetica Neue', sans-serif;
            }
            .blog-meta {
                color: #718096;
                font-size: 0.9rem;
                font-style: italic;
                border-top: 2px solid #e2e8f0;
                padding-top: 1rem;
                margin-top: 2rem;
            }
            </style>
            """
        
        elif format_type == "vintage":
            return """
            <style>
            .vintage-container {
                background: linear-gradient(to bottom, #f4e4c1 0%, #e8d4a8 100%);
                padding: 3rem;
                border: 3px solid #8b7355;
                box-shadow: inset 0 0 50px rgba(0,0,0,0.1), 0 10px 30px rgba(0,0,0,0.3);
                margin: 2rem 0;
                position: relative;
            }
            .vintage-container::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y="50" font-size="100" opacity="0.02">📰</text></svg>');
                pointer-events: none;
            }
            .vintage-content {
                background: rgba(255, 255, 245, 0.9);
                padding: 2.5rem;
                border: 1px solid #8b7355;
                font-family: 'Times New Roman', serif;
                line-height: 1.6;
                color: #3e2723;
                position: relative;
            }
            .vintage-title {
                font-size: 2.2rem;
                font-weight: bold;
                text-align: center;
                border-bottom: 3px double #8b7355;
                padding-bottom: 1rem;
                margin-bottom: 1.5rem;
                letter-spacing: 2px;
                text-transform: uppercase;
                color: #1a1a1a;
            }
            .vintage-meta {
                text-align: center;
                font-size: 0.85rem;
                color: #5d4037;
                font-style: italic;
                border-top: 1px solid #8b7355;
                padding-top: 1rem;
                margin-top: 2rem;
            }
            </style>
            """
        
        elif format_type == "professional":
            return """
            <style>
            .professional-container {
                background: linear-gradient(to right, #1e3a8a 0%, #1e40af 100%);
                padding: 3rem;
                border-radius: 10px;
                box-shadow: 0 15px 50px rgba(0,0,0,0.2);
                margin: 2rem 0;
            }
            .professional-content {
                background: white;
                padding: 2.5rem;
                border-radius: 8px;
                border-left: 5px solid #3b82f6;
                font-family: 'Arial', sans-serif;
                line-height: 1.7;
                color: #1f2937;
            }
            .professional-title {
                color: #1e40af;
                font-size: 2rem;
                font-weight: bold;
                margin-bottom: 1rem;
                font-family: 'Helvetica', sans-serif;
                border-bottom: 3px solid #3b82f6;
                padding-bottom: 0.5rem;
            }
            .professional-meta {
                background: #f3f4f6;
                padding: 1rem;
                border-radius: 5px;
                border-left: 3px solid #3b82f6;
                margin-top: 2rem;
                font-size: 0.9rem;
                color: #4b5563;
            }
            </style>
            """
        
        elif format_type == "social_thread":
            return """
            <style>
            .social-container {
                background: linear-gradient(135deg, #1da1f2 0%, #14171a 100%);
                padding: 2.5rem;
                border-radius: 20px;
                box-shadow: 0 15px 40px rgba(0,0,0,0.3);
                margin: 2rem 0;
            }
            .social-content {
                background: white;
                padding: 2rem;
                border-radius: 15px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                line-height: 1.5;
                color: #14171a;
            }
            .social-title {
                color: #1da1f2;
                font-size: 1.8rem;
                font-weight: bold;
                margin-bottom: 1.5rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            .social-post {
                background: #f7f9f9;
                padding: 1rem 1.5rem;
                border-radius: 12px;
                margin-bottom: 1rem;
                border-left: 3px solid #1da1f2;
                transition: all 0.2s;
            }
            .social-post:hover {
                background: #e8f5fe;
                transform: translateX(5px);
            }
            .social-meta {
                color: #657786;
                font-size: 0.9rem;
                text-align: center;
                margin-top: 1.5rem;
                padding-top: 1rem;
                border-top: 1px solid #e1e8ed;
            }
            </style>
            """
        
        return ""
    
    @staticmethod
    def format_for_display(content: GeneratedContent) -> str:
        """
        Format content for display in the UI with beautiful styling.
        
        Args:
            content: GeneratedContent object
            
        Returns:
            Formatted HTML string ready for display
        """
        format_type = content.format_type
        css = ContentFormatter.get_format_css(format_type)
        
        if format_type == "blog":
            return ContentFormatter._format_blog(content, css)
        elif format_type == "vintage":
            return ContentFormatter._format_vintage(content, css)
        elif format_type == "professional":
            return ContentFormatter._format_professional(content, css)
        elif format_type == "social_thread":
            return ContentFormatter._format_social_thread(content, css)
        else:
            return ContentFormatter._format_default(content)
    
    @staticmethod
    def _format_blog(content: GeneratedContent, css: str) -> str:
        """Format as a beautiful blog post."""
        return f"""{css}
<div class="blog-container">
    <div class="blog-content">
        <div class="blog-title">✨ {content.title}</div>
        <div style="margin-top: 1.5rem;">
            {content.content.replace(chr(10), '<br><br>')}
        </div>
        <div class="blog-meta">
            📝 {content.word_count} words • ⏱️ {max(1, content.word_count // 200)} min read
        </div>
    </div>
</div>
"""
    
    @staticmethod
    def _format_vintage(content: GeneratedContent, css: str) -> str:
        """Format as a vintage newspaper article."""
        return f"""{css}
<div class="vintage-container">
    <div class="vintage-content">
        <div class="vintage-title">📰 {content.title.upper()}</div>
        <div style="margin-top: 1.5rem; text-align: justify;">
            {content.content.replace(chr(10), '<br><br>')}
        </div>
        <div class="vintage-meta">
            Published in The Daily AI • {content.word_count} words
        </div>
    </div>
</div>
"""
    
    @staticmethod
    def _format_professional(content: GeneratedContent, css: str) -> str:
        """Format as a professional report."""
        return f"""{css}
<div class="professional-container">
    <div class="professional-content">
        <div class="professional-title">📊 {content.title}</div>
        <div style="margin-top: 1.5rem;">
            {content.content.replace(chr(10), '<br><br>')}
        </div>
        <div class="professional-meta">
            <strong>Document Information</strong><br>
            Word Count: {content.word_count} | Sources Referenced: {len(content.sources_used)}
        </div>
    </div>
</div>
"""
    
    @staticmethod
    def _format_social_thread(content: GeneratedContent, css: str) -> str:
        """Format as a social media thread."""
        # Split content into thread posts
        lines = content.content.split('\n')
        thread_posts = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                thread_posts.append(line)
        
        # Format as numbered thread
        posts_html = ""
        for idx, post in enumerate(thread_posts, 1):
            posts_html += f'<div class="social-post"><strong>{idx}.</strong> {post}</div>\n'
        
        return f"""{css}
<div class="social-container">
    <div class="social-content">
        <div class="social-title">🧵 {content.title}</div>
        {posts_html}
        <div class="social-meta">
            Thread length: {len(thread_posts)} posts
        </div>
    </div>
</div>
"""
    
    @staticmethod
    def _format_default(content: GeneratedContent) -> str:
        """Default formatting."""
        return f"""
# {content.title}

{content.content}

---
*{content.word_count} words*
"""
    
    @staticmethod
    def format_sources(sources: list[str]) -> str:
        """Format source URLs for display."""
        if not sources:
            return "*No sources available*"
        
        formatted = "**📚 Sources:**\n\n"
        for idx, url in enumerate(sources, 1):
            formatted += f"{idx}. {url}\n"
        
        return formatted


# Singleton instance
content_formatter = ContentFormatter()
