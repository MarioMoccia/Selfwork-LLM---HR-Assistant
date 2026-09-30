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
   Database", vedi `cl.Action`/`cl.action_callback`) e risolve il secondo esercizio di
   `ESERCIZI.md`: elimina la chiamata separata al modello per il nome del candidato,
   passando le prime righe del CV direttamente nel prompt principale, che ora genera anche
   una sezione "contatti" (nome, email, telefono).
6. **Avanzamento 6:** introduce il chunking semantico (vedi "Chunking semantico" più sotto),
   in sostituzione dello split meccanico su `### `. Ripristina anche la doppia chiamata al
   modello per il nome del candidato, tornando sui suoi passi rispetto all'avanzamento 5.
7. **Avanzamento 7:** refactoring dello stesso chunking semantico, da funzioni statiche a una
   classe con metodi dedicati (`SemanticChunking`), nessun cambio di comportamento.
8. **Avanzamento 8:** gli embedding diventano intercambiabili tra OpenAI, un modello locale
   (`SentenceTransformer`) e Ollama, scelti da un solo parametro in `config.py`
   (`Config.EMBEDDING_PROVIDER`, vedi `custom_embedding.py`). Di serie usa embedding locali e
   chat via Ollama: è l'unico avanzamento eseguibile senza alcuna chiave API.
9. **Avanzamento 9:** l'LLM classifica ogni messaggio dell'utente come ricerca di un nuovo CV
   o domanda di approfondimento su un CV già trovato, e la chat mantiene il contesto
   dell'ultimo CV individuato per rispondere alle domande di follow-up.

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

## Chunking semantico (dall'avanzamento 6)

Invece di dividere il testo in modo meccanico (per esempio ogni 500 caratteri, o su un
separatore fisso come `### `), il chunking semantico usa l'intelligenza artificiale per capire
dove il significato del testo cambia. Analizza ogni frase nel suo contesto, calcola l'embedding
di ciascuna e misura quanto due frasi consecutive sono semanticamente diverse (distanza
coseno). Quando trova un punto dove questa differenza è particolarmente alta (sopra un
percentile configurabile), lo usa come confine per creare un nuovo chunk. Questo mantiene
insieme le parti di testo semanticamente correlate, invece di tagliarle a metà per un limite di
caratteri arbitrario.

`resumes/mit.txt` (il saggio "Why to Not Not Start a Startup" di Paul Graham) è incluso
apposta: è un testo lungo e in inglese, utile per osservare il chunking semantico su un
documento più corposo dei singoli CV.

Dall'avanzamento 8 il modello di embedding usato per il chunking è configurabile allo stesso
modo di quello del database vettoriale (OpenAI, locale o Ollama), tramite `custom_embedding.py`.
