# Selfwork LLM - HR Assistant

Assistente HR in chat (Chainlit) che recupera dai CV disponibili il profilo più adatto a una
richiesta dell'utente, tramite RAG (ChromaDB + embedding OpenAI) e generazione con LLM
(OpenAI o Ollama locale).

Il progetto è stato costruito per avanzamenti successivi, ognuno con il proprio commit:

1. **Avanzamento 1:** scheletro del progetto Poetry con Chainlit; un bot che fa solo eco al
   messaggio ricevuto.
2. **Avanzamento 2:** prima versione funzionante, in un unico file: lettura e chunking dei CV,
   embedding e ricerca per similarità in ChromaDB (in memoria), estrazione del nome del
   candidato ed elaborazione della risposta.
3. **Avanzamento 3:** stessa logica, refactorizzata in moduli (`config.py`, `database.py`,
   `document_processor.py`, `utils.py`) e con database vettoriale persistente su disco.
4. **Avanzamento 4 (bonus):** stessa architettura dell'avanzamento 3, ma completamente
   locale: embedding e chat passano da OpenAI a Ollama (`nomic-embed-text` e `llama3.2`),
   senza bisogno di alcuna chiave API. Gli avanzamenti 1-3 restano fedeli al corso originale;
   questo è un passo aggiuntivo, non una sostituzione.

## Installazione Poetry

- https://python-poetry.org/

## Setup

```bash
poetry install
```

### Versione con OpenAI (avanzamenti 2 e 3)

Copia `.env.example` in `.env` e inserisci la tua chiave OpenAI:

```bash
cp .env.example .env
```

### Versione locale con Ollama (avanzamento 4, default di questo repository)

Nessuna chiave richiesta: scarica i due modelli e avvia il server Ollama.

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
ollama serve
```

## Per eseguire l'applicazione

```bash
eval $(poetry env activate)
chainlit run hr_assistant/__init__.py -w
```
