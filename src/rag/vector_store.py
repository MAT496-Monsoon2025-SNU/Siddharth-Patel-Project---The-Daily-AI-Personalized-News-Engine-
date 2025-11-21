"""
Vector store implementation using ChromaDB.
This demonstrates SEMANTIC SEARCH and RAG - key MAT496 topics.
"""

import chromadb
from chromadb.config import Settings
from typing import List, Optional
from src.config import Config
from src.state import NewsArticle


class VectorStore:
    """
    ChromaDB-based vector store for semantic search over news articles.
    Enables RAG (Retrieval Augmented Generation) by storing and retrieving relevant context.
    """
    
    def __init__(self):
        """Initialize ChromaDB client and collection."""
        self.client = chromadb.PersistentClient(
            path=Config.CHROMA_PERSIST_DIR,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=Config.COLLECTION_NAME,
            metadata={"description": "News articles for The Daily AI"}
        )
    
    def add_articles(self, articles: List[NewsArticle], topic: str) -> None:
        """
        Add news articles to the vector store.
        
        Args:
            articles: List of NewsArticle objects to store
            topic: The topic these articles are related to
        """
        if not articles:
            return
        
        documents = []
        metadatas = []
        ids = []
        
        for idx, article in enumerate(articles):
            # Create document text
            doc_text = f"Title: {article.title}\n\nContent: {article.content}"
            documents.append(doc_text)
            
            # Create metadata
            metadata = {
                "title": article.title,
                "url": article.url,
                "topic": topic,
                "source": article.source or "unknown",
                "published_date": article.published_date or "unknown"
            }
            metadatas.append(metadata)
            
            # Create unique ID
            ids.append(f"{topic}_{idx}_{hash(article.url)}")
        
        # Add to collection
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def semantic_search(self, query: str, n_results: int = 3) -> List[dict]:
        """
        Perform semantic search to find relevant articles.
        This demonstrates SEMANTIC SEARCH capability.
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            List of relevant documents with metadata
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        if results["documents"] and results["documents"][0]:
            for idx, doc in enumerate(results["documents"][0]):
                result = {
                    "content": doc,
                    "metadata": results["metadatas"][0][idx] if results["metadatas"] else {},
                    "distance": results["distances"][0][idx] if results["distances"] else None
                }
                formatted_results.append(result)
        
        return formatted_results
    
    def get_context_for_topic(self, topic: str, query: Optional[str] = None, 
                             n_results: int = 5) -> str:
        """
        Get relevant context for a topic to augment generation (RAG).
        This demonstrates RAG (Retrieval Augmented Generation).
        
        Args:
            topic: The topic to get context for
            query: Optional specific query to refine search
            n_results: Number of results to retrieve
            
        Returns:
            Formatted context string
        """
        search_query = query if query else topic
        results = self.semantic_search(search_query, n_results)
        
        if not results:
            return ""
        
        # Format context
        context_parts = []
        for idx, result in enumerate(results, 1):
            metadata = result["metadata"]
            content = result["content"]
            
            context_part = f"""
Source {idx}: {metadata.get('title', 'Unknown')}
URL: {metadata.get('url', 'N/A')}
Published: {metadata.get('published_date', 'Unknown')}

{content}

---
"""
            context_parts.append(context_part)
        
        return "\n".join(context_parts)
    
    def clear_collection(self) -> None:
        """Clear all documents from the collection."""
        self.client.delete_collection(Config.COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(
            name=Config.COLLECTION_NAME,
            metadata={"description": "News articles for The Daily AI"}
        )
    
    def get_stats(self) -> dict:
        """Get statistics about the vector store."""
        count = self.collection.count()
        return {
            "total_documents": count,
            "collection_name": Config.COLLECTION_NAME
        }


# Singleton instance
vector_store = VectorStore()
