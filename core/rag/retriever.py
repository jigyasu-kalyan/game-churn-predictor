# core/rag/retriever.py

import os
import logging
from langchain_community.vectorstores import Chroma
from ..config import settings
from .embedding import get_embedding_model
from .loader import load_and_chunk_playbook
from ..utils.logger import logger

class EngagementRAG:
    def __init__(self, chroma_path: str = settings.CHROMA_PATH):
        """Initializes ChromaDB, building it from scratch if it doesn't exist."""
        self.chroma_path = chroma_path
        self.embeddings = get_embedding_model()
        self.vector_store = self._init_vector_store()

    def _init_vector_store(self):
        if os.path.exists(self.chroma_path):
            logger.info(f"Loading existing vector database from {self.chroma_path}")
            return Chroma(persist_directory=self.chroma_path, embedding_function=self.embeddings)
        else:
            logger.info("Building new vector database from playbook...")
            return self._build_vector_store()

    def _build_vector_store(self):
        docs = load_and_chunk_playbook()
        if not docs:
            logger.warning("No documents found to build vector store.")
            return None
            
        vector_store = Chroma.from_documents(
            documents=docs, 
            embedding=self.embeddings, 
            persist_directory=self.chroma_path
        )
        return vector_store

    def retrieve_strategies(self, player_issues: list, k: int = settings.RETRIEVAL_K) -> str:
        """Retrieves strategies based on risk factors, with graceful fallbacks."""
        if not self.vector_store:
            return "Fallback Strategy: System unavailable. Recommend standard engagement monitoring."

        query = " ".join(player_issues)
        
        try:
            results = self.vector_store.similarity_search(query, k=k)
            
            if not results:
                return "Fallback Strategy: No specific strategies found. Monitor player behavior."
                
            formatted_context = ""
            for i, doc in enumerate(results):
                formatted_context += f"--- Strategy {i+1} ---\n{doc.page_content}\n\n"
                
            return formatted_context.strip()
            
        except Exception as e:
            logger.error(f"Retrieval error: {e}")
            return "Fallback Strategy: Retrieval failed. Automatically reduce difficulty by 5%."
