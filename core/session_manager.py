import uuid
from typing import Dict
from datetime import datetime, timedelta

class SessionManager:
    def __init__(self, session_timeout: int = 1800):
        self.session_timeout = session_timeout
        self.sessions: Dict[str, Dict] = {}
    
    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            'created_at': datetime.now(),
            'last_activity': datetime.now(),
            'data': {}
        }
        return session_id
    
    def get_session(self, session_id: str) -> Dict:
        return self.sessions.get(session_id)
    
    def update_activity(self, session_id: str) -> None:
        if session_id in self.sessions:
            self.sessions[session_id]['last_activity'] = datetime.now()
    
    def is_valid(self, session_id: str) -> bool:
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        if datetime.now() - session['last_activity'] > timedelta(seconds=self.session_timeout):
            del self.sessions[session_id]
            return False
        
        self.update_activity(session_id)
        return True
    
    def clear_session(self, session_id: str) -> None:
        if session_id in self.sessions:
            del self.sessions[session_id]