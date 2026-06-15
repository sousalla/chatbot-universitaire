from typing import Dict, List
from datetime import datetime
import json

class ConversationManager:
    def __init__(self, max_history: int = 100):
        self.max_history = max_history
        self.conversations: Dict[str, List[Dict]] = {}
    
    def get_or_create_conversation(self, session_id: str) -> List[Dict]:
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        return self.conversations[session_id]
    
    def add_message(self, session_id: str, role: str, content: str) -> None:
        conversation = self.get_or_create_conversation(session_id)
        message = {'role': role, 'content': content, 'timestamp': datetime.now().isoformat()}
        conversation.append(message)
        
        if len(conversation) > self.max_history:
            self.conversations[session_id] = conversation[-self.max_history:]
    
    def get_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        conversation = self.get_or_create_conversation(session_id)
        return conversation[-limit:] if limit else conversation
    
    def clear_conversation(self, session_id: str) -> None:
        if session_id in self.conversations:
            self.conversations[session_id] = []