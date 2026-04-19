# core/rag/embedding.py

from langchain_huggingface import HuggingFaceEmbeddings
from ..config import settings

def get_embedding_model():
    """Initializes and returns the HuggingFace embedding model."""
    return HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
