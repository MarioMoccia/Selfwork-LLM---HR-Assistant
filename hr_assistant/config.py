# config.py
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DOCUMENTS_DIR = "resumes"
    COLLECTION_NAME = "CVs"
    PERSISTENT_DIR = "data/chromadb"

    # Versione 100% locale con Ollama (avanzamento 4): nessuna chiave richiesta.
    OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
    EMBEDDING_MODEL = "nomic-embed-text"
    LLM_MODEL = "llama3.2"
    AI_API_URL = f"{OLLAMA_URL}/v1"
    AI_API_KEY = "ollama"  # valore fittizio richiesto dal client OpenAI, ignorato da Ollama

    # Per tornare a OpenAI (avanzamento 3): commenta il blocco Ollama sopra, scommenta
    # questo e imposta OPENAI_API_KEY nel file .env.
    # MODEL_NAME = "text-embedding-3-small"
    # OPENAI_KEY = os.environ["OPENAI_API_KEY"]
    # LLM_MODEL = "gpt-4o-mini"
    # AI_API_URL = "https://api.openai.com/v1/"
    # AI_API_KEY = OPENAI_KEY
