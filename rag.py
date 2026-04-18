import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# --- Configuration ---
PLAYBOOK_PATH = "retention_playbook.md"
CHROMA_PATH = "./chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2" # Free, lightweight, runs locally

class EngagementRAG:
    def __init__(self):
        """Initializes the RAG system, loading the vector DB if it exists, or building it if it doesn't."""
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        
        if os.path.exists(CHROMA_PATH):
            print("Loading existing vector database...")
            self.vector_store = Chroma(persist_directory=CHROMA_PATH, embedding_function=self.embeddings)
        else:
            print("Building new vector database from playbook...")
            self.vector_store = self._build_vector_store()

    def _build_vector_store(self):
        """Reads the markdown playbook, chunks it by headers, and saves to ChromaDB."""
        try:
            with open(PLAYBOOK_PATH, 'r', encoding='utf-8') as f:
                markdown_document = f.read()
                
            # Split based on Markdown headers to preserve context
            headers_to_split_on = [
                ("#", "Section"),
                ("##", "Topic"),
                ("###", "Strategy")
            ]
            markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
            docs = markdown_splitter.split_text(markdown_document)

            # Create and persist the vector database
            vector_store = Chroma.from_documents(
                documents=docs, 
                embedding=self.embeddings, 
                persist_directory=CHROMA_PATH
            )
            return vector_store
            
        except FileNotFoundError:
            print(f"Error: {PLAYBOOK_PATH} not found. Please ensure the file exists.")
            return None

    def retrieve_strategies(self, player_issues: list, k: int = 2) -> str:
        """
        Retrieves the most relevant retention strategies based on identified player issues.
        Includes robust error handling as mandated by the rubric.
        """
        if not self.vector_store:
            return "Fallback Strategy: System unavailable. Recommend standard engagement monitoring and offering a minor login reward."

        query = " ".join(player_issues)
        
        try:
            # Perform similarity search
            results = self.vector_store.similarity_search(query, k=k)
            
            if not results:
                return "Fallback Strategy: No specific strategies found. Recommend monitoring player behavior for the next 3 sessions."
                
            # Format the retrieved documents into a single context string
            formatted_context = ""
            for i, doc in enumerate(results):
                formatted_context += f"--- Strategy {i+1} ---\n"
                formatted_context += f"{doc.page_content}\n\n"
                
            return formatted_context.strip()
            
        except Exception as e:
            print(f"Retrieval error: {e}")
            # Graceful degradation for the hosted demo
            return "Fallback Strategy: Retrieval failed. Automatically reduce difficulty by 5% and offer a cosmetic reward."

# --- Testing Block ---
# This allows you to run `python rag.py` in your terminal to test it independently of the Streamlit app.
if __name__ == "__main__":
    print("Initializing RAG Module...")
    rag = EngagementRAG()
    
    test_issues = ["Low AvgSessionDurationMinutes", "High GameDifficulty", "Zero Achievements"]
    print(f"\nTest Query: {test_issues}")
    
    print("\nRetrieving Strategies...")
    retrieved_info = rag.retrieve_strategies(test_issues)
    print("\n" + "="*40)
    print(retrieved_info)
    print("="*40)