import numpy as np
from typing import List

# Liste manuelle de stop words français (simplifiée)
FRENCH_STOP_WORDS = [
    'le', 'la', 'les', 'un', 'une', 'de', 'du', 'des', 'et', 'ou', 'mais', 'donc', 'or', 'ni', 'car',
    'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles', 'me', 'te', 'se', 'lui', 'leur', 'y', 'en',
    'est', 'sont', 'suis', 'es', 'sommes', 'êtes', 'ai', 'as', 'a', 'avons', 'avez', 'ont',
    'comment', 'pourquoi', 'quand', 'où', 'quel', 'quelle', 'quels', 'quelles', 'très', 'trop', 'peu',
    'assez', 'presque', 'environ', 'ce', 'cet', 'cette', 'ces', 'mon', 'ton', 'son', 'notre', 'votre', 'leur'
]

class EmbeddingService:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = None
        self.fallback = None
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
            self.dimension = self.model.get_sentence_embedding_dimension()
            print(f" Sentence-Transformers chargé (dim: {self.dimension})")
        except ImportError as e:
            print(f" Sentence-Transformers non disponible : {e}")
            print("   → Utilisation du fallback TF-IDF")
            self._init_fallback()
        except Exception as e:
            print(f" Erreur de chargement du modèle : {e}")
            self._init_fallback()

    def _init_fallback(self):
        from sklearn.feature_extraction.text import TfidfVectorizer
        self.fallback = True
        # Utilisation d'une liste de stop words français
        self.vectorizer = TfidfVectorizer(max_features=384, stop_words=FRENCH_STOP_WORDS)
        self.is_fitted = False
        self.dimension = 384

    def fit(self, texts: List[str]):
        """Entraîne le vectoriseur (obligatoire pour le fallback)."""
        if self.fallback and not self.is_fitted:
            self.vectorizer.fit(texts)
            self.is_fitted = True

    def embed_text(self, text: str) -> np.ndarray:
        if self.model is not None:
            return self.model.encode(text)
        else:
            if not self.is_fitted:
                raise RuntimeError("Fallback TF‑IDF non entraîné. Appelez fit() d'abord.")
            return self.vectorizer.transform([text]).toarray()[0]

    def embed_batch(self, texts: List[str]) -> np.ndarray:
        if self.model is not None:
            return self.model.encode(texts)
        else:
            if not self.is_fitted:
                raise RuntimeError("Fallback TF‑IDF non entraîné.")
            return self.vectorizer.transform(texts).toarray()