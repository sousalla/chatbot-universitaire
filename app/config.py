import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'unibot_secret_key_2026')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))
    
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 500))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 50))
    TOP_K = int(os.getenv('TOP_K', 3))
    DOCUMENTS_PATH = os.getenv('DOCUMENTS_PATH', 'data/raw/documents')
    VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', 'data/vector_db')
    USE_LLM = os.getenv('USE_LLM', 'True').lower() == 'true'
    HUGGING_FACE_TOKEN = os.getenv('HUGGING_FACE_TOKEN')