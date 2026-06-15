from typing import List, Dict

class PromptBuilder:
    def build(self, question: str, context_chunks: List[Dict]) -> str:
        context = ""
        for i, chunk in enumerate(context_chunks):
            source = chunk['metadata'].get('source', 'inconnu')
            context += f"[Source {i+1} - {source}]: {chunk['content']}\n\n"
        
        prompt = f"""Contexte universitaire:
{context}

Question: {question}

Réponse:"""
        return prompt