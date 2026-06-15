from typing import List, Dict
from rag.embedding_service import EmbeddingService
from rag.vector_store import VectorStore

class Retriever:
    def __init__(self, vector_store: VectorStore, embedding_service: EmbeddingService):
        self.vector_store = vector_store
        self.embedding_service = embedding_service
    
    def search(self, question: str, top_k: int = 3) -> List[Dict]:
        query_embedding = self.embedding_service.embed_text(question)
        results = self.vector_store.search(query_embedding, top_k=top_k)
        if results:
            results.sort(key=lambda x: x.get('score', 0), reverse=True)
        return results