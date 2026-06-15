# core/gemma_adapter.py
import torch
import re
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import Optional

class GemmaAdapter:
    def __init__(self, model_name: str = "google/gemma-2b-it", hf_token: str = None):
        self.model_name = model_name
        self.hf_token = hf_token
        self.model = None
        self.tokenizer = None
        self.device = None
        self.is_loaded = False
        
        self.generation_params = {
            'max_new_tokens': 200,
            'temperature': 0.7,
            'top_p': 0.9,
            'do_sample': True
        }
    
    def load(self):
        try:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            print(f" Device: {self.device}")
            
            print(" Chargement de Gemma-2b-it...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True,
                token=self.hf_token
            )
            
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Correction ici : torch_dtype -> dtype
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None,
                trust_remote_code=True,
                token=self.hf_token
            )
            
            if not torch.cuda.is_available():
                self.model = self.model.to(self.device)
            
            self.model.eval()
            self.generation_params['pad_token_id'] = self.tokenizer.pad_token_id
            self.is_loaded = True
            print(" Gemma-2b-it chargé!")
            
        except Exception as e:
            print(f" Erreur chargement Gemma: {e}")
            self.is_loaded = False
    
    def generate(self, question: str, context: Optional[str] = None) -> Optional[str]:
        if not self.is_loaded:
            return None
        
        if context:
            prompt = f"""Contexte: {context}

Question: {question}

Réponse:"""
        else:
            prompt = f"""Tu es un assistant universitaire. Réponds précisément à la question.

Question: {question}

Réponse:"""
        
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    **self.generation_params
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = response[len(prompt):].strip()
            response = re.sub(r'\s+', ' ', response)
            
            return response if response and len(response) > 10 else None
        except Exception as e:
            print(f" Erreur génération: {e}")
            return None
    
    def is_ready(self) -> bool:
        return self.is_loaded