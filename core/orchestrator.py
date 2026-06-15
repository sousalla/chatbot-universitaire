from rag.rag_pipeline import RAGPipeline
import os

class Orchestrator:
    def __init__(self):
        self.rag_pipeline = RAGPipeline()
        docs_path = os.getenv('DOCUMENTS_PATH', 'data/raw/documents')
        self.rag_pipeline.index_documents(docs_path)

    def process_question(self, question: str) -> dict:
        context = self.rag_pipeline.get_context(question)
        if context:
            return {
                'answer': context[:500],
                'confidence': 0.7,
                'source': 'rag'
            }
        return {
            'answer': "Je n'ai pas trouvé de réponse dans la base de connaissances.",
            'confidence': 0.0,
            'source': 'fallback'
        }

orchestrator = Orchestrator()