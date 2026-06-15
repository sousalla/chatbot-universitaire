from abc import ABC, abstractmethod
from typing import Optional

class ModelInterface(ABC):
    @abstractmethod
    def load(self):
        pass
    
    @abstractmethod
    def generate(self, question: str, context: Optional[str] = None) -> Optional[str]:
        pass
    
    @abstractmethod
    def is_ready(self) -> bool:
        pass