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
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');
            
            .blog-container {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 3rem;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                margin: 2rem 0;
            }
            .blog-content {
                background: white;
                padding: 3rem;
                border-radius: 15px;
                font-family: 'Lora', Georgia, serif;
                line-height: 1.8;
                color: #2d3748;
                max-width: 800px;
                margin: 0 auto;
            }
            .blog-title {
                color: #667eea;
                font-size: 3rem;
                font-weight: 900;
                margin-bottom: 1rem;
                font-family: 'Playfair Display', serif;
                line-height: 1.2;
            }
            .blog-subtitle {
                color: #718096;
                font-size: 1.3rem;
                font-style: italic;
                margin-bottom: 2rem;
                font-weight: 400;
            }
            .blog-text {
                font-size: 1.1rem;
                margin-bottom: 1.5rem;
            }
            .blog-meta {
                color: #718096;
                font-size: 0.95rem;
                font-style: italic;
                border-top: 2px solid #e2e8f0;
                padding-top: 1.5rem;
                margin-top: 3rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            </style>
            """
        
        elif format_type == "vintage":
            return """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=EB+Garamond:ital,wght@0,400;0,600;0,700;1,400&display=swap');
            
            .vintage-page {
                background: linear-gradient(to bottom, 
                    #f5e6d3 0%, 
                    #f0dcc4 20%, 
                    #ead5b8 40%, 
                    #e8d3b5 60%, 
                    #e5d0b0 80%, 
                    #e0cab0 100%);
                padding: 2rem;
                box-shadow: 0 0 100px rgba(0,0,0,0.3);
                position: relative;
            }
            .vintage-page::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-image: 
                    repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.03) 2px, rgba(0,0,0,0.03) 4px),
                    repeating-linear-gradient(90deg, transparent, transparent 2px, rgba(0,0,0,0.03) 2px, rgba(0,0,0,0.03) 4px);
                pointer-events: none;
                opacity: 0.3;
            }
            .vintage-container {
                background: rgba(255, 250, 240, 0.95);
                border: 8px double #3e2723;
                padding: 2rem;
                position: relative;
                box-shadow: inset 0 0 30px rgba(0,0,0,0.1);
            }
            .vintage-masthead {
                text-align: center;
                border-bottom: 4px double #3e2723;
                padding-bottom: 1rem;
                margin-bottom: 1.5rem;
            }
            .vintage-paper-name {
                font-family: 'Playfair Display', serif;
                font-size: 3rem;
                font-weight: 900;
                letter-spacing: 3px;
                color: #1a1a1a;
                text-transform: uppercase;
                margin-bottom: 0.5rem;
            }
            .vintage-date {
                font-family: 'EB Garamond', serif;
                font-size: 0.9rem;
                color: #5d4037;
                font-style: italic;
            }
            .vintage-headline {
                font-family: 'Playfair Display', serif;
                font-size: 2.8rem;
                font-weight: 900;
                text-align: center;
                letter-spacing: 1px;
                line-height: 1.1;
                margin: 1.5rem 0;
                color: #1a1a1a;
                text-transform: uppercase;
                border-top: 2px solid #3e2723;
                border-bottom: 2px solid #3e2723;
                padding: 1rem 0;
            }
            .vintage-columns {
                column-count: 2;
                column-gap: 2rem;
                column-rule: 1px solid #8b7355;
                font-family: 'EB Garamond', serif;
                font-size: 1.05rem;
                line-height: 1.6;
                text-align: justify;
                color: #2c2c2c;
            }
            .vintage-columns p {
                margin-bottom: 1rem;
                text-indent: 1.5rem;
            }
            .vintage-columns p:first-child::first-letter {
                font-size: 4rem;
                font-weight: bold;
                float: left;
                line-height: 0.8;
                margin: 0.1rem 0.5rem 0 0;
                font-family: 'Playfair Display', serif;
            }
            .vintage-footer {
                text-align: center;
                font-size: 0.85rem;
                color: #5d4037;
                font-style: italic;
                border-top: 1px solid #8b7355;
                padding-top: 1rem;
                margin-top: 1.5rem;
            }
            </style>
            """
        
        elif format_type == "professional":
            return """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
            
            .professional-container {
                background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
                padding: 3rem;
                border-radius: 10px;
                box-shadow: 0 15px 50px rgba(0,0,0,0.2);
                margin: 2rem 0;
            }
            .professional-content {
                background: white;
                padding: 3rem;
                border-radius: 8px;
                border-left: 5px solid #3b82f6;
                font-family: 'Inter', Arial, sans-serif;
                line-height: 1.7;
                color: #1f2937;
            }
            .professional-header {
                border-bottom: 3px solid #3b82f6;
                padding-bottom: 1.5rem;
                margin-bottom: 2rem;
            }
            .professional-title {
                color: #1e40af;
                font-size: 2.2rem;
                font-weight: 800;
                margin-bottom: 0.5rem;
                font-family: 'Inter', sans-serif;
            }
            .professional-subtitle {
                color: #6b7280;
                font-size: 1.1rem;
                font-weight: 600;
            }
            .professional-text {
                font-size: 1.05rem;
                margin-bottom: 1.5rem;
            }
            .professional-meta {
                background: #f3f4f6;
                padding: 1.5rem;
                border-radius: 5px;
                border-left: 3px solid #3b82f6;
                margin-top: 2rem;
                font-size: 0.95rem;
                color: #4b5563;
            }
            </style>
            """
        
        elif format_type == "social_thread":
            return """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            
            .social-container {
                background: linear-gradient(135deg, #1da1f2 0%, #0c7abf 100%);
                padding: 2.5rem;
                border-radius: 20px;
                box-shadow: 0 15px 40px rgba(0,0,0,0.3);
                margin: 2rem 0;
            }
            .social-content {
                background: white;
                padding: 2rem;
                border-radius: 15px;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                line-height: 1.5;
                color: #14171a;
            }
            .social-title {
                color: #1da1f2;
                font-size: 1.8rem;
                font-weight: 700;
                margin-bottom: 1.5rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            .social-post {
                background: #f7f9f9;
                padding: 1.2rem 1.5rem;
                border-radius: 12px;
                margin-bottom: 1rem;
                border-left: 3px solid #1da1f2;
                transition: all 0.2s;
                font-size: 1.05rem;
            }
            .social-post:hover {
                background: #e8f5fe;
                transform: translateX(5px);
                box-shadow: 0 2px 8px rgba(29,161,242,0.2);
            }
            .social-post strong {
                color: #1da1f2;
                font-weight: 600;
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
        import re
        
        # Process content
        text = content.content
        
        # Convert markdown bold to HTML
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Convert markdown italic to HTML
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        
        # Split content into paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # Format paragraphs
        formatted_paragraphs = ""
        for para in paragraphs:
            if para.startswith('#'):
                # It's a heading
                heading_text = para.lstrip("#").strip()
                formatted_paragraphs += f'<h2 style="color: #667eea; font-size: 1.8rem; margin-top: 2rem; margin-bottom: 1rem; font-weight: 700;">{heading_text}</h2>'
            else:
                formatted_paragraphs += f'<p class="blog-text">{para}</p>'
        
        return f"""{css}
<div class="blog-container">
    <div class="blog-content">
        <div class="blog-title">{content.title}</div>
        <div class="blog-subtitle">A fresh perspective on today's news</div>
        {formatted_paragraphs}
        <div class="blog-meta">
            <span>📝 {content.word_count} words</span>
            <span>⏱️ {max(1, content.word_count // 200)} min read</span>
        </div>
    </div>
</div>
"""
    
    @staticmethod
    def _format_vintage(content: GeneratedContent, css: str) -> str:
        """Format as an authentic vintage newspaper with columns."""
        from datetime import datetime
        import re
        
        # Get current date in vintage format
        today = datetime.now()
        vintage_date = today.strftime("%A, %B %d, %Y")
        
        # Clean and process content
        text = content.content
        
        # Convert markdown bold (**text**) to HTML bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        
        # Split content into paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip() and not p.startswith('#')]
        
        # Format paragraphs for columns
        formatted_text = ""
        for para in paragraphs:
            # Clean up any remaining markdown
            para = para.replace('**', '')
            formatted_text += f'<p>{para}</p>'
        
        return f"""{css}
<div class="vintage-page">
    <div class="vintage-container">
        <div class="vintage-masthead">
            <div class="vintage-paper-name">📰 The Daily AI</div>
            <div class="vintage-date">{vintage_date} • Price: 5 Cents</div>
        </div>
        
        <div class="vintage-headline">
            {content.title.upper()}
        </div>
        
        <div class="vintage-columns">
            {formatted_text}
        </div>
        
        <div class="vintage-footer">
            Published by The Daily AI Press • {content.word_count} words
        </div>
    </div>
</div>
"""
    
    @staticmethod
    def _format_professional(content: GeneratedContent, css: str) -> str:
        """Format as a professional report."""
        import re
        
        # Process content
        text = content.content
        
        # Convert markdown bold to HTML
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        
        # Split content into paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        formatted_paragraphs = ""
        for para in paragraphs:
            if para.startswith('#'):
                formatted_paragraphs += f'<h3 style="color: #1e40af; font-size: 1.5rem; margin-top: 2rem; margin-bottom: 1rem; font-weight: 700;">{para.lstrip("#").strip()}</h3>'
            else:
                formatted_paragraphs += f'<p class="professional-text">{para}</p>'
        
        return f"""{css}
<div class="professional-container">
    <div class="professional-content">
        <div class="professional-header">
            <div class="professional-title">📊 {content.title}</div>
            <div class="professional-subtitle">Executive Brief</div>
        </div>
        {formatted_paragraphs}
        <div class="professional-meta">
            <strong>Document Information</strong><br>
            Word Count: {content.word_count} | Sources Referenced: {len(content.sources_used)} | Classification: Public
        </div>
    </div>
</div>
"""
    
    @staticmethod
    def _format_social_thread(content: GeneratedContent, css: str) -> str:
        """Format as a social media thread."""
        import re
        
        # Process content
        text = content.content
        
        # Convert markdown bold to HTML
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Convert markdown italic to HTML
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        
        # Split content into thread posts
        lines = text.split('\n')
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
            💬 Thread length: {len(thread_posts)} posts
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
