# UniBot - Chatbot Universitaire Intelligent

## Développement d'un Chatbot basé sur le Traitement Automatique du Langage Naturel

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![Gemma](https://img.shields.io/badge/Gemma-2b--it-orange.svg)](https://huggingface.co/google/gemma-2b-it)

---

##  Table des matières

- [Présentation](#présentation-du-projet)
- [Fonctionnalités](#fonctionnalités)
- [Architecture technique](#architecture-technique)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [API](#api)
- [Dépannage](#dépannage)
- [Auteur](#auteur)

---

##  Présentation du projet

UniBot est un chatbot intelligent conçu pour assister les étudiants de la Faculté Polydisciplinaire de Béni Mellal. Il utilise l'architecture RAG (Retrieval-Augmented Generation) avec le modèle Gemma-2b-it pour fournir des réponses précises et pertinentes.

### Contexte

- Saturation des services administratifs (scolarité, bibliothèque, relations internationales)
- Délais de réponse pouvant atteindre plusieurs semaines
- Disponibilité limitée (horaires restreints 9h-16h)
- Questions répétitives représentant 70% des demandes

### Objectifs

| Objectif | Description |
|----------|-------------|
| **Automatisation** | Répondre aux questions fréquentes 24h/24 |
| **Désengorgement** | Réduire la charge des services administratifs |
| **Précision** | Fournir des réponses sourcées et fiables |
| **Accessibilité** | Interface intuitive et responsive |

---

##  Fonctionnalités

###  Pour les étudiants

-  **Poser une question** en langage naturel
-  **Recevoir une réponse** pertinente avec score de confiance
-  **Créer un compte** et s'authentifier
-  **Consulter l'historique** des conversations
-  **Interface responsive** (mobile, tablette, desktop)

###  Pour l'administrateur

-  **Dashboard administrateur** complet
-  **Gérer la base de connaissances** (ajout/suppression de documents)
-  **Consulter les statistiques** d'utilisation
-  **Gérer les utilisateurs** (suppression)

###  Technologies IA

-  **Modèle Gemma-2b-it** (Google) pour la génération
-  **Architecture RAG** pour la recherche contextuelle
-  **ChromaDB** pour la base vectorielle
-  **Sentence-Transformers** pour les embeddings

---

##  Architecture technique

```text
┌──────────────────────────────────────────────────────────────┐
│                         UTILISATEURS                         │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    COUCHE PRÉSENTATION                      │
│              HTML5 • CSS3 • Bootstrap 5 • JS               │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    COUCHE APPLICATION                       │
│                     Flask (API REST)                        │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                     COUCHE TRAITEMENT                       │
│                                                            │
│  • Pipeline RAG                                            │
│  • ChromaDB (Recherche vectorielle)                        │
│  • Gemma-2b-it (Génération de réponses)                    │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                      COUCHE DONNÉES                         │
│                                                            │
│  • Documents sources                                       │
│  • Base vectorielle                                        │
│  • Logs système                                            │
└──────────────────────────────────────────────────────────────┘
```



### Pipeline RAG

| Phase | Description |
|-------|-------------|
| **Indexation (offline)** | Chargement → Découpage → Vectorisation → Stockage |
| **Génération (online)** | Question → Embedding → Recherche → Contexte → Gemma → Réponse |

### Stack technologique

| Composant | Technologie | Rôle |
|-----------|-------------|------|
| Frontend | Bootstrap 5 + JavaScript | Interface utilisateur |
| Backend | Flask (Python) | API REST |
| Modèle IA | Gemma-2b-it (Google) | Génération des réponses |
| Base vectorielle | ChromaDB | Stockage des embeddings |
| Embeddings | Sentence-Transformers | Vectorisation des textes |

---

##  Prérequis

| Élément | Configuration minimale |
|---------|----------------------|
| **Python** | 3.10 ou supérieur |
| **RAM** | 4 Go (8 Go recommandé) |
| **Espace disque** | 10 Go |
| **Système** | Windows  |

---

# Installation

## 1. Cloner le dépôt

```bash
git clone https://github.com/sousalla/chatbot-universitaire.git
cd chatbot-universitaire
```

## 2. Créer et activer l'environnement virtuel

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## 4. Configurer le token Hugging Face

1. Créer un compte sur Hugging Face.
2. Accepter les conditions d'utilisation du modèle **Gemma-2b-it**.
3. Générer un token d'accès.
4. Créer un fichier `.env` à la racine du projet :

```env
HF_TOKEN=votre_token_huggingface
```

## 5. Lancer l'application

```bash
python run.py
```

## 6. Accéder à l'application

Ouvrez votre navigateur :

```text
http://localhost:5000
```

---

# Dashboard Administrateur

Accédez à :

```text
http://localhost:5000/admin
```

### Identifiants par défaut

| Champ        | Valeur                                      |
| ------------ | ------------------------------------------- |
| Email        | [admin@usms.ac.ma](mailto:admin@usms.ac.ma) |
| Mot de passe | admin123                                    |

### Fonctionnalités

* Consultation des statistiques
* Gestion des utilisateurs
* Ajout et suppression de documents
* Réindexation de la base vectorielle RAG
* Suivi des conversations

---

# Structure du projet

```text
chatbot-universitaire/
│
├── app/                          # Application Flask
│   ├── __init__.py
│   ├── routes.py
│   └── config.py
│
├── core/                         # Cœur du système
│   ├── orchestrator.py
│   ├── conversation_manager.py
│   ├── session_manager.py
│   └── user_manager.py
│
├── rag/                          # Pipeline RAG
│   ├── document_loader.py
│   ├── text_splitter.py
│   ├── embedding_service.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── prompt_builder.py
│   ├── response_formatter.py
│   └── rag_pipeline.py
│
├── model/                        # Modèle IA
│   ├── model_interface.py
│   └── gemma_adapter.py
│
├── frontend/
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   └── admin.html
│   │
│   └── static/
│       ├── css/
│       └── js/
│
├── data/
│   ├── raw/
│   │   └── documents/
│   ├── users.json
│   ├── conversations.json
│   └── logs/
│
├── notebooks/
├── requirements.txt
├── .env
├── run.py
└── README.md
```

---

# API Endpoints

| Méthode | Endpoint                | Description                             |
| ------- | ----------------------- | --------------------------------------- |
| POST    | `/login`                | Connexion utilisateur                   |
| POST    | `/register`             | Inscription utilisateur                 |
| GET     | `/logout`               | Déconnexion                             |
| POST    | `/send`                 | Envoi d'un message via formulaire       |
| POST    | `/api/chat`             | API de conversation (JSON)              |
| GET     | `/api/status`           | État du système                         |
| GET     | `/api/admin/users`      | Liste des utilisateurs (Admin)          |
| DELETE  | `/api/admin/users/<id>` | Suppression d'un utilisateur            |
| GET     | `/health`               | Vérification de l'état de l'application |

---

# Exemple d'utilisation de l'API

### Requête

```http
POST /api/chat
Content-Type: application/json
```

```json
{
  "message": "Quels sont les modules du Master D3SI ?"
}
```

### Réponse

```json
{
  "response": "Les modules du Master D3SI sont ..."
}
```

---

# Auteur

**AALLA Soufiane**

Étudiant en Master D3SI
Faculté Polydisciplinaire de Béni Mellal
Université Sultan Moulay Slimane

---

# Encadrement

**Pr. Ismail KICH**

---

# Remerciements

* Pr. Ismail KICH pour son encadrement et ses précieux conseils.
* Pr. Abdelkrim MAARIR, chef de filière D3SI.
* L'ensemble des enseignants de la spécialité D3SI.
* La Faculté Polydisciplinaire de Béni Mellal.
* Ma famille et mes amis pour leur soutien.

---

# Contact

📧 [aallasoufiane.al@gmail.com](mailto:aallasoufiane.al@gmail.com)

