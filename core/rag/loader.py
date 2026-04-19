# core/rag/loader.py

import os
from langchain_text_splitters import MarkdownHeaderTextSplitter
from ..config import settings
from ..utils.logger import logger

def load_and_chunk_playbook(path: str = settings.PLAYBOOK_PATH):
    """Reads the playbook and chunks it by headers to preserve strategy context."""
    if not os.path.exists(path):
        logger.error(f"Playbook path {path} does not exist.")
        return []
        
    try:
        with open(path, 'r', encoding='utf-8') as f:
            markdown_document = f.read()
            
        headers_to_split_on = [
            ("#", "Section"),
            ("##", "Topic"),
            ("###", "Strategy")
        ]
        
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        return markdown_splitter.split_text(markdown_document)
        
    except Exception as e:
        logger.error(f"Error loading playbook: {e}")
        return []
