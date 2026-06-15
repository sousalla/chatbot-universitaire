import os
from typing import List, Dict

class DocumentLoader:
    @staticmethod
    def load_text(file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Erreur: {e}")
            return ""
    
    @staticmethod
    def load_pdf(file_path: str) -> str:
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Erreur PDF: {e}")
            return ""
    
    def load_directory(self, directory_path: str) -> List[Dict]:
        documents = []
        if not os.path.exists(directory_path):
            return documents
        
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            if filename.endswith('.txt'):
                content = self.load_text(file_path)
            elif filename.endswith('.pdf'):
                content = self.load_pdf(file_path)
            else:
                continue
            
            if content and len(content.strip()) > 50:
                documents.append({
                    'id': filename,
                    'content': content,
                    'metadata': {'source': filename}
                })
        return documents