import chromadb
import numpy as np
from typing import List, Dict
import os

class VectorStore:
    def __init__(self, persist_directory: str = "./data/vector_db"):
        os.makedirs(persist_directory, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = None
    
    def get_or_create_collection(self, name: str = "university_docs"):
        try:
            self.collection = self.client.get_collection(name)
        except:
            self.collection = self.client.create_collection(name)
        return self.collection
    
    def delete_collection(self, name: str = "university_docs"):
        try:
            self.client.delete_collection(name)
        except:
            pass
    
    def add_documents(self, chunks: List[Dict], embeddings: List[np.ndarray]):
        if not self.collection:
            self.get_or_create_collection()
        
        batch_size = 50
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            batch_emb = embeddings[i:i+batch_size]
            self.collection.add(
                ids=[c['id'] for c in batch],
                embeddings=[emb.tolist() for emb in batch_emb],
                documents=[c['content'] for c in batch],
                metadatas=[c['metadata'] for c in batch]
            )
        print(f" {len(chunks)} chunks indexés")
    
    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Dict]:
        if not self.collection:
            return []
        
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )
        
        formatted = []
        if results['ids'] and results['ids'][0]:
            for i in range(len(results['ids'][0])):
                formatted.append({
                    'id': results['ids'][0][i],
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'score': 1 - results['distances'][0][i] if results.get('distances') else 0.5
                })
        return formatted