from typing import List, Dict

class TextSplitter:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_text(self, text: str) -> List[str]:
        if not text or len(text) < 50:
            return []
        
        chunks = []
        words = text.split()
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_len = len(word) + 1
            if current_length + word_len <= self.chunk_size:
                current_chunk.append(word)
                current_length += word_len
            else:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = word_len
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        return chunks
    
    def split_documents(self, documents: List[Dict]) -> List[Dict]:
        chunks = []
        for doc in documents:
            text_chunks = self.split_text(doc['content'])
            for i, chunk in enumerate(text_chunks):
                chunks.append({
                    'id': f"{doc['id']}_chunk_{i}",
                    'content': chunk,
                    'metadata': {**doc['metadata'], 'chunk_index': i}
                })
        return chunks