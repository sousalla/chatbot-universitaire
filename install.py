# install_simple.py
import subprocess
import sys

print(" Installation des dépendances...")

# Installer torch en premier (version CPU)
subprocess.run([sys.executable, "-m", "pip", "install", "torch==2.2.0", "--index-url", "https://download.pytorch.org/whl/cpu"])

# Installer les autres packages un par un
packages = [
    "transformers==4.36.0",
    "accelerate==0.26.0",
    "sentencepiece==0.1.99",
    "sentence-transformers==2.2.2",
    "chromadb==0.4.22",
    "Flask==2.3.3",
    "Flask-CORS==4.0.0",
    "python-dotenv==1.0.0",
    "pandas==2.1.3",
    "numpy==1.24.3",
    "PyPDF2==3.0.1",
    "huggingface-hub==0.34.0"
]

for package in packages:
    print(f"Installation de {package}...")
    subprocess.run([sys.executable, "-m", "pip", "install", package])

print(" Installation terminée!")