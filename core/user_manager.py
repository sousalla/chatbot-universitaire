import os
import json
import uuid
import secrets
import hashlib
from datetime import datetime

USERS_FILE = 'data/users.json'
CONVERSATIONS_FILE = 'data/conversations.json'

class UserManager:
    def __init__(self):
        self.ensure_files()
    
    def ensure_files(self):
        os.makedirs('data', exist_ok=True)
        if not os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'w') as f:
                json.dump([], f)
        if not os.path.exists(CONVERSATIONS_FILE):
            with open(CONVERSATIONS_FILE, 'w') as f:
                json.dump([], f)
    
    def hash_password(self, password: str) -> str:
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256((password + salt).encode())
        return f"{salt}:{hash_obj.hexdigest()}"
    
    def verify_password(self, password: str, hashed: str) -> bool:
        try:
            salt, hash_value = hashed.split(':')
            hash_obj = hashlib.sha256((password + salt).encode())
            return hash_obj.hexdigest() == hash_value
        except:
            return False
    
    def get_user_by_email(self, email):
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
        for user in users:
            if user['email'] == email:
                return user
        return None
    
    def create_user(self, name, email, password):
        user_id = str(uuid.uuid4())
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
        
        users.append({
            'id': user_id,
            'name': name,
            'email': email,
            'password': self.hash_password(password),
            'role': 'user',
            'created_at': datetime.now().isoformat()
        })
        
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
        return user_id
    
    def get_all_users(self):
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
        
        admin_exists = any(u.get('email') == 'admin@usms.ac.ma' for u in users)
        if not admin_exists:
            users.insert(0, {
                'id': 'admin_001',
                'name': 'Administrateur',
                'email': 'admin@usms.ac.ma',
                'role': 'admin',
                'created_at': datetime.now().isoformat(),
                'conversations': 0
            })
        
        return users
    
    def delete_user(self, user_id):
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
        users = [u for u in users if u['id'] != user_id]
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
    
    def save_conversation(self, user_id, session_id, question, answer, confidence, source):
        conv = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'session_id': session_id,
            'question': question,
            'answer': answer,
            'confidence': confidence,
            'source': source,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(CONVERSATIONS_FILE, 'r') as f:
            convs = json.load(f)
        convs.append(conv)
        with open(CONVERSATIONS_FILE, 'w') as f:
            json.dump(convs, f, indent=2)
    
    def get_conversations(self, user_id, limit=50):
        with open(CONVERSATIONS_FILE, 'r') as f:
            convs = json.load(f)
        user_convs = [c for c in convs if c.get('user_id') == user_id]
        user_convs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return user_convs[:limit]
    
    def clear_conversations(self, user_id):
        with open(CONVERSATIONS_FILE, 'r') as f:
            convs = json.load(f)
        convs = [c for c in convs if c.get('user_id') != user_id]
        with open(CONVERSATIONS_FILE, 'w') as f:
            json.dump(convs, f, indent=2)
    
    def get_stats(self):
        with open(CONVERSATIONS_FILE, 'r') as f:
            convs = json.load(f)
        
        total = len(convs)
        confidences = [c.get('confidence', 0) for c in convs if c.get('confidence')]
        avg_conf = sum(confidences) / len(confidences) if confidences else 0
        
        return {'total_questions': total, 'avg_confidence': round(avg_conf, 2)}

user_manager = UserManager()