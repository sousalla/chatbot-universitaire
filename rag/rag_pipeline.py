import os
from typing import List, Dict, Optional
from rag.document_loader import DocumentLoader
from rag.text_splitter import TextSplitter
from rag.embedding_service import EmbeddingService
from rag.vector_store import VectorStore
from rag.retriever import Retriever

class RAGPipeline:
    def __init__(self):
        self.is_indexed = False
        self.document_loader = DocumentLoader()
        self.text_splitter = TextSplitter(chunk_size=500, chunk_overlap=50)
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore(persist_directory='./data/vector_db')
        self.retriever = None

    def index_documents(self, documents_path: str) -> bool:
        if not os.path.exists(documents_path):
            return False
        docs = self.document_loader.load_directory(documents_path)
        if not docs:
            return False
        chunks = self.text_splitter.split_documents(docs)
        if not chunks:
            return False

        # 1. Entraîner le TF‑IDF sur tous les chunks
        texts = [c['content'] for c in chunks]
        self.embedding_service.fit(texts)

        # 2. Calculer les embeddings
        embeddings = self.embedding_service.embed_batch(texts)

        # 3. Stocker dans ChromaDB
        self.vector_store.get_or_create_collection()
        self.vector_store.add_documents(chunks, embeddings)

        self.retriever = Retriever(self.vector_store, self.embedding_service)
        self.is_indexed = True
        return True

    def search(self, question: str, top_k: int = 3) -> List[Dict]:
        if not self.is_indexed or not self.retriever:
            return []
        return self.retriever.search(question, top_k=top_k)

    def get_context(self, question: str, top_k: int = 3) -> Optional[str]:
        chunks = self.search(question, top_k)
        if chunks:
            return "\n\n".join([c['content'] for c in chunks])
        return None