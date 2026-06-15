from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__, 
                template_folder='../frontend/templates',
                static_folder='../frontend/static')
    app.secret_key = os.getenv('SECRET_KEY', 'unibot_secret_key_2026')
    CORS(app)
    
    # Configuration
    app.config['CHUNK_SIZE'] = int(os.getenv('CHUNK_SIZE', 500))
    app.config['CHUNK_OVERLAP'] = int(os.getenv('CHUNK_OVERLAP', 50))
    app.config['TOP_K'] = int(os.getenv('TOP_K', 3))
    app.config['DOCUMENTS_PATH'] = os.getenv('DOCUMENTS_PATH', 'data/raw/documents')
    app.config['VECTOR_DB_PATH'] = os.getenv('VECTOR_DB_PATH', 'data/vector_db')
    app.config['USE_LLM'] = os.getenv('USE_LLM', 'True').lower() == 'true'
    app.config['HUGGING_FACE_TOKEN'] = os.getenv('HUGGING_FACE_TOKEN')
    
    # Initialiser l'orchestrateur
    from core.orchestrator import orchestrator
    app.orchestrator = orchestrator
    
    # Enregistrer les routes
    from app.routes import bp
    app.register_blueprint(bp)
    
    return app