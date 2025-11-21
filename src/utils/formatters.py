"""
Output formatters for different content types.
"""

from src.state import GeneratedContent


class ContentFormatter:
    """Formats generated content for display."""
    
    @staticmethod
    def format_for_display(content: GeneratedContent) -> str:
        """
        Format content for display in the UI.
        
        Args:
            content: GeneratedContent object
            
        Returns:
            Formatted string ready for display
        """
        format_type = content.format_type
        
        if format_type == "blog":
            return ContentFormatter._format_blog(content)
        elif format_type == "vintage":
            return ContentFormatter._format_vintage(content)
        elif format_type == "professional":
            return ContentFormatter._format_professional(content)
        elif format_type == "social_thread":
            return ContentFormatter._format_social_thread(content)
        else:
            return ContentFormatter._format_default(content)
    
    @staticmethod
    def _format_blog(content: GeneratedContent) -> str:
        """Format as a blog post."""
        return f"""
# {content.title}

{content.content}

---
*Word count: {content.word_count}*
"""
    
    @staticmethod
    def _format_vintage(content: GeneratedContent) -> str:
        """Format as a vintage newspaper article."""
        return f"""
# {content.title.upper()}

{content.content}

---
*Published in The Daily AI • {content.word_count} words*
"""
    
    @staticmethod
    def _format_professional(content: GeneratedContent) -> str:
        """Format as a professional report."""
        return f"""
# {content.title}

**Report Summary**

{content.content}

---
**Document Information**
- Word Count: {content.word_count}
- Sources Referenced: {len(content.sources_used)}
"""
    
    @staticmethod
    def _format_social_thread(content: GeneratedContent) -> str:
        """Format as a social media thread."""
        # Split content into thread posts
        lines = content.content.split('\n')
        thread_posts = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                thread_posts.append(line)
        
        # Format as numbered thread
        formatted = f"# 🧵 {content.title}\n\n"
        for idx, post in enumerate(thread_posts, 1):
            formatted += f"**{idx}.** {post}\n\n"
        
        formatted += f"---\n*Thread length: {len(thread_posts)} posts*"
        
        return formatted
    
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
        
        formatted = "**Sources:**\n\n"
        for idx, url in enumerate(sources, 1):
            formatted += f"{idx}. {url}\n"
        
        return formatted


# Singleton instance
content_formatter = ContentFormatter()
