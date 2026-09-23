# Selfwork LLM - HR Assistant

Assistente HR in chat (Chainlit) che recupera dai CV disponibili il profilo più adatto a una
richiesta dell'utente, tramite RAG (ChromaDB + embedding OpenAI) e generazione con LLM.

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
   senza bisogno di alcuna chiave API. Non fa parte della sequenza ufficiale del corso: è un
   passo aggiuntivo, non una sostituzione. Per questo motivo il numero riprende da 4 anche
   nell'avanzamento successivo: nella storia del repository trovi due commit chiamati
   "avanzamento 4" (questo bonus e la sincronizzazione dei documenti qui sotto), volutamente.
4. **Avanzamento 4 (sincronizzazione documenti):** riprende l'architettura OpenAI
   dell'avanzamento 3 e aggiunge il tracciamento dei CV nel database vettoriale (vedi
   "Sincronizzazione dei documenti" più sotto).
5. **Avanzamento 5:** aggiunge due azioni in chat ("Statistiche Database" e "Reindex
   Database") e risolve il secondo esercizio di `ESERCIZI.md`, eliminando la doppia chiamata
   al modello per estrarre nome e contatti del candidato.

## Installazione Poetry

- https://python-poetry.org/

## Setup

```bash
poetry install
```

### Versione con OpenAI (avanzamenti 2, 3, 4, 5)

Copia `.env.example` in `.env` e inserisci la tua chiave OpenAI:

```bash
cp .env.example .env
```

### Versione locale con Ollama (avanzamento 4, bonus)

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

## Sincronizzazione dei documenti (dall'avanzamento 4)

La soluzione si basa su tre concetti principali:

1. **Tracciamento dei file**
   - Per ogni file viene calcolato un hash MD5 del contenuto
   - Questo hash funziona come una "impronta digitale" del file
   - Vengono anche memorizzati il nome del file e la data di ultima modifica
   - Queste informazioni vengono salvate nel database insieme ai contenuti

2. **Processo di sincronizzazione**
   - All'avvio del sistema, viene fatto un confronto tra:
     - I file attualmente presenti nella cartella dei curriculum
     - I file tracciati nel database
   - Il sistema identifica automaticamente tre categorie:
     - File nuovi (presenti nella cartella ma non nel database)
     - File modificati (presenti in entrambi ma con hash diverso)
     - File eliminati (presenti nel database ma non più nella cartella)

3. **Gestione dei contenuti**
   - Per i file nuovi: vengono divisi in frammenti (chunks) e ogni frammento viene aggiunto
     al database con i relativi metadati
   - Per i file modificati: prima vengono rimossi tutti i vecchi frammenti dal database, poi
     vengono aggiunti i nuovi frammenti del file aggiornato
   - Per i file eliminati: vengono rimossi tutti i frammenti associati dal database

Il vantaggio: evita duplicazioni nel database, minimizza le operazioni di scrittura, mantiene
il database sempre sincronizzato con i file reali ed è efficiente perché processa solo ciò che
è effettivamente cambiato.

La cartella `resumes/` cambia composizione a ogni avanzamento apposta, per dimostrare dal vivo
add/update/remove della sincronizzazione.
