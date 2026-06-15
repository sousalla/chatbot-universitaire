# app/routes.py
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from core.orchestrator import orchestrator
from core.user_manager import user_manager
import uuid

bp = Blueprint('main', __name__)

import os
from datetime import datetime


DOCUMENTS_DIR = "data/raw/documents"

@bp.route('/admin/api/documents', methods=['GET'])
def admin_get_documents():
    user = session.get('user')
    if not user or user.get('role') != 'admin':
        return jsonify({'error': 'Non autorisé'}), 401
    
    documents = []
    if os.path.exists(DOCUMENTS_DIR):
        for filename in os.listdir(DOCUMENTS_DIR):
            filepath = os.path.join(DOCUMENTS_DIR, filename)
            if os.path.isfile(filepath):
                stat = os.stat(filepath)
                documents.append({
                    'id': filename,
                    'name': filename,
                    'filename': filename,
                    'date': datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
    return jsonify({'documents': documents})

@bp.route('/admin/api/upload', methods=['POST'])
def admin_upload_document():
    user = session.get('user')
    if not user or user.get('role') != 'admin':
        return jsonify({'error': 'Non autorisé'}), 401
    
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nom de fichier vide'}), 400
    
    filename = file.filename
    filepath = os.path.join(DOCUMENTS_DIR, filename)
    file.save(filepath)
    
    orchestrator.rag_pipeline.index_documents(DOCUMENTS_DIR)
    
    return jsonify({'message': 'Document ajouté et indexé avec succès'})

@bp.route('/admin/api/documents/<doc_id>', methods=['DELETE'])
def admin_delete_document(doc_id):
    user = session.get('user')
    if not user or user.get('role') != 'admin':
        return jsonify({'error': 'Non autorisé'}), 401
    
    filepath = os.path.join(DOCUMENTS_DIR, doc_id)
    if os.path.exists(filepath):
        os.remove(filepath)
        orchestrator.rag_pipeline.index_documents(DOCUMENTS_DIR)
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Fichier non trouvé'}), 404

@bp.route('/admin/api/reindex', methods=['POST'])
def admin_reindex():
    user = session.get('user')
    if not user or user.get('role') != 'admin':
        return jsonify({'error': 'Non autorisé'}), 401
    
    orchestrator.rag_pipeline.index_documents(DOCUMENTS_DIR)
    return jsonify({'message': 'Réindexation terminée'})

def get_simple_response(message: str) -> str:
    msg = message.lower().strip()
    
    # Salutations et aides
    simple_responses = {
        'bonjour': 'Bonjour ! Comment puis-je vous aider ?',
        'salut': 'Salut ! Comment puis-je vous aider ?',
        'merci': 'Je vous en prie !',
        'au revoir': 'Au revoir ! À bientôt.',
        'ça va': 'Je vais très bien, merci !',
        'qui es-tu': 'Je suis UniBot, votre assistant universitaire.',
        'aide': 'Je peux répondre à vos questions sur les inscriptions, examens, bibliothèque, bourses...'
    }
    for key, response in simple_responses.items():
        if key in msg:
            return response
    
    # Formations
    if "formation" in msg and ("existe" in msg or "quelles" in msg or "liste" in msg):
        return """🎓 **Formations disponibles à la Faculté Polydisciplinaire de Béni Mellal** :

- **Licences** : 
  • DFA (Droit Financier et des Affaires)
  • CMI (Chimie et Matériaux pour l'Industrie)
  • BGE (Biotechnologie et Génie Ecologique)
  • ABS (Agro Biosciences)
  • SBA (Sciences Biomédicales Appliquées)
  • MPM (Matériaux et Physique Moderne)
  • ISE (Ingénierie des Systèmes Electriques)
  • IEM (Ingénierie Energétique et Mécanique)
  • MIACSD (Mathématiques et Informatique Appliquées à la Cybersécurité et Sciences des Données)

- **Licences d'excellence** : Impression 3D & IA, IoT & Robotique, Data Science & Cybersécurité
- **Masters** : Télécoms & réseaux, Physique moderne, Droit des affaires, Biomolécules & santé

  Consultez le site de l'université pour plus de détails."""
    
    # Inscription
    if "inscrire" in msg or "inscription" in msg:
        return """ **Procédure d'inscription** :

1. **Pré-inscription en ligne** sur l'espace étudiant de l'université du 1er juin au 30 septembre.
2. **Constituer le dossier** : baccalauréat, CNI, photos, justificatif de domicile, certificat de naissance.
3. **Déposer le dossier** au secrétariat pédagogique.

"""
    
    return None

@bp.route('/')
def index():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')

@bp.route('/admin')
def admin_page():
    user = session.get('user')
    if not user or user.get('role') != 'admin':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('main.index'))
    return render_template('admin.html')

@bp.route('/about')
def about_page():
    return render_template('about.html')

@bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if email == 'admin@usms.ac.ma' and password == 'admin123':
        session['user'] = {'id': 'admin_001', 'name': 'Administrateur', 'email': email, 'role': 'admin'}
        session['chat_history'] = []
        flash('Connexion réussie !', 'success')
        return redirect(url_for('main.index'))
    
    user = user_manager.get_user_by_email(email)
    if user and user_manager.verify_password(password, user['password']):
        session['user'] = user
        session['chat_history'] = user_manager.get_conversations(user['id'])
        flash(f'Bienvenue {user["name"]} !', 'success')
        return redirect(url_for('main.index'))
    
    flash('Email ou mot de passe incorrect', 'danger')
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not name or not email or not password:
        flash('Tous les champs sont requis', 'danger')
        return redirect(url_for('main.index'))
    
    if len(password) < 6:
        flash('Mot de passe trop court (min 6 caractères)', 'danger')
        return redirect(url_for('main.index'))
    
    if user_manager.get_user_by_email(email):
        flash('Email déjà utilisé', 'danger')
        return redirect(url_for('main.index'))
    
    user_manager.create_user(name, email, password)
    flash('Compte créé avec succès ! Connectez-vous.', 'success')
    return redirect(url_for('main.index'))

@bp.route('/logout')
def logout():
    session.clear()
    flash('Déconnecté', 'info')
    return redirect(url_for('main.index'))

@bp.route('/send', methods=['POST'])
def send_message():
    if 'user' not in session:
        return redirect(url_for('main.index'))
    
    message = request.form.get('message', '').strip()
    if not message:
        return redirect(url_for('main.index'))
    
    simple_response = get_simple_response(message)
    if simple_response:
        answer = simple_response
        source = 'automatic'
        confidence = 1.0
    else:
        response = orchestrator.process_question(message)
        answer = response['answer']
        source = response['source']
        confidence = response['confidence']
    
    if 'chat_history' not in session:
        session['chat_history'] = []
    session['chat_history'].append({'user': message, 'bot': answer, 'confidence': confidence})
    
    user_manager.save_conversation(
        session['user']['id'],
        session.get('session_id', 'default'),
        message,
        answer,
        confidence,
        source
    )
    
    return redirect(url_for('main.index'))

@bp.route('/clear')
def clear_history():
    user = session.get('user')
    if user:
        user_manager.clear_conversations(user['id'])
        session['chat_history'] = []
        flash('Historique effacé', 'info')
    return redirect(url_for('main.index'))

@bp.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json()
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({'error': 'Message vide'}), 400
    
    simple_response = get_simple_response(message)
    if simple_response:
        return jsonify({'response': simple_response, 'confidence': 1.0, 'success': True})
    
    response = orchestrator.process_question(message)
    return jsonify({
        'response': response['answer'],
        'confidence': response['confidence'],
        'source': response['source'],
        'success': True
    })

@bp.route('/api/status', methods=['GET'])
def api_status():
    stats = user_manager.get_stats()
    return jsonify({
        'status': 'ok',
        'indexed': orchestrator.rag_pipeline.is_indexed,
        'gemma_loaded': orchestrator.gemma.is_ready() if orchestrator.gemma else False,
        'total_questions': stats['total_questions'],
        'avg_confidence': stats['avg_confidence']
    })

@bp.route('/api/admin/users', methods=['GET'])
def admin_get_users():
    user = session.get('user')
    if not user or user.get('role') != 'admin':
        return jsonify({'error': 'Non autorisé'}), 401
    return jsonify({'users': user_manager.get_all_users()})

@bp.route('/api/admin/users/<user_id>', methods=['DELETE'])
def admin_delete_user(user_id):
    user = session.get('user')
    if not user or user.get('role') != 'admin':
        return jsonify({'error': 'Non autorisé'}), 401
    user_manager.delete_user(user_id)
    return jsonify({'success': True})

@bp.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'gemma_loaded': orchestrator.gemma.is_ready() if orchestrator.gemma else False,
        'rag_indexed': orchestrator.rag_pipeline.is_indexed
    })