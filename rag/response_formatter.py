from typing import List, Dict

class ResponseFormatter:
    def format(self, raw_response: str, sources: List[Dict], question: str) -> Dict:
        answer = raw_response.strip()
        if not answer or len(answer) < 10:
            answer = "Je suis désolé, je n'ai pas trouvé d'information pertinente."
        
        formatted_sources = []
        for src in sources:
            formatted_sources.append({
                'source': src['metadata'].get('source', 'inconnu'),
                'content': src['content'][:200] + "...",
                'score': src.get('score', 0)
            })
        
        confidence = sum([s.get('score', 0) for s in sources]) / len(sources) if sources else 0.5
        
        return {
            'answer': answer,
            'sources': formatted_sources,
            'confidence': round(confidence, 2),
            'question': question
        }