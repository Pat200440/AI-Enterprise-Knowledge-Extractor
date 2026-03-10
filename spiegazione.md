# Spiegazione Completa del Progetto: AI Enterprise Knowledge Extractor

## Indice

1. [Panoramica Generale del Progetto](#1-panoramica-generale-del-progetto)
2. [Flusso di Lavoro del Progetto](#2-flusso-di-lavoro-del-progetto)
3. [Architettura del Progetto](#3-architettura-del-progetto)
4. [Spiegazione del Codice File per File](#4-spiegazione-del-codice-file-per-file)
5. [Spiegazione Dettagliata del Codice](#5-spiegazione-dettagliata-del-codice)
6. [Concetti Tecnici Spiegati in Modo Semplice](#6-concetti-tecnici-spiegati-in-modo-semplice)
7. [Riassunto Finale](#7-riassunto-finale)

---

## 1. Panoramica Generale del Progetto

### Che cosa fa questo progetto?

Immagina di avere decine o centinaia di documenti aziendali (manuali, policy, report) e di dover cercare un'informazione specifica. Normalmente dovresti aprire ogni documento e leggere tutto. Questo progetto ti permette di:

1. **Caricare i tuoi documenti** (PDF o DOCX)
2. **Fare domande in linguaggio naturale** (es. "Qual è la policy sulle ferie?")
3. **Ricevere risposte precise** basate sul contenuto dei tuoi documenti
4. **Vedere da quale parte del documento proviene la risposta**

### Quale problema risolve?

Il problema principale è la **ricerca di informazioni in grandi volumi di testo**. Invece di cercare manualmente, il sistema:

- Capisce il **significato** della tua domanda (non solo le parole chiave)
- Trova le **parti più rilevanti** dei tuoi documenti
- Genera una **risposta naturale** usando l'intelligenza artificiale

### Cosa succede dall'upload del file fino alla risposta finale?

Facciamo un esempio concreto:

**Prima fase: Preparazione (upload e indicizzazione)**
1. Carichi il file "policy_aziendale.pdf"
2. Il sistema estrae tutto il testo dal PDF
3. Divide il testo in piccoli pezzi (chiamati "chunk")
4. Converte ogni pezzo in un **embedding** (un vettore di numeri che rappresenta il significato)
5. Salva tutti questi vettori in un database speciale chiamato FAISS

**Seconda fase: Ricerca e risposta (quando fai una domanda)**
1. Scrivi la domanda: "Quanti giorni di ferie ho?"
2. Il sistema converte la tua domanda in un embedding
3. Cerca nel database FAISS i pezzi di testo più simili alla tua domanda
4. Prende i 3 pezzi più rilevanti
5. Invia questi pezzi + la tua domanda a Gemini (l'intelligenza artificiale di Google)
6. Gemini legge i pezzi e genera una risposta in linguaggio naturale
7. Ti mostra la risposta + i pezzi di testo originali da cui proviene

---

## 2. Flusso di Lavoro del Progetto

### Step 1: Upload del Documento

**Cosa fa:**
L'utente carica uno o più file PDF o DOCX tramite l'interfaccia Streamlit.

**Perché serve:**
Dobbiamo avere i documenti sul nostro computer per poterli processare.

**Input:**
- File PDF o DOCX caricati dall'utente

**Output:**
- File salvati nella cartella `data/documents/`

---

### Step 2: Estrazione del Testo

**Cosa fa:**
Il sistema legge il contenuto del file e estrae tutto il testo.

**Perché serve:**
I file PDF e DOCX sono formati complessi. Dobbiamo estrarre solo il testo puro per poterlo analizzare.

**Come funziona:**
- Per i **PDF**: usa la libreria `pypdf` che sa come leggere i PDF
- Per i **DOCX**: usa la libreria `python-docx` che sa come leggere i file Word

**Input:**
- File PDF o DOCX salvato sul disco

**Output:**
- Una stringa di testo contenente tutto il contenuto del documento

**Esempio:**
```
Input: "policy_aziendale.pdf"
Output: "I dipendenti hanno diritto a 20 giorni di ferie all'anno. Le ferie devono essere richieste con almeno 2 settimane di anticipo..."
```

---

### Step 3: Chunking (Divisione in Pezzi)

**Cosa fa:**
Divide il testo lungo in pezzi più piccoli e gestibili.

**Perché serve:**
- I modelli di AI hanno un **limite di token** (non possono leggere testi infiniti)
- Pezzi più piccoli rendono la ricerca più **precisa**
- Se cerchiamo "policy ferie", vogliamo trovare solo il paragrafo sulle ferie, non tutto il documento

**Come funziona:**
Il testo viene diviso in "chunk" (pezzi) di 500 caratteri, con un **overlap** (sovrapposizione) di 50 caratteri.

**Perché l'overlap?**
Immagina di tagliare una frase a metà. L'overlap assicura che non perdiamo informazioni importanti ai bordi dei chunk.

**Input:**
- Testo completo del documento

**Output:**
- Lista di chunk (pezzi di testo)

**Esempio:**
```
Testo originale: "I dipendenti hanno diritto a 20 giorni di ferie all'anno. Le ferie devono essere richieste con almeno 2 settimane di anticipo. Il manager deve approvare la richiesta entro 5 giorni lavorativi."

Chunk 1: "I dipendenti hanno diritto a 20 giorni di ferie all'anno. Le ferie devono essere richieste con almeno 2 settimane di anticipo."

Chunk 2: "Le ferie devono essere richieste con almeno 2 settimane di anticipo. Il manager deve approvare la richiesta entro 5 giorni lavorativi."

(Nota: il chunk 2 inizia prima che finisca il chunk 1 - questo è l'overlap)
```

---

### Step 4: Generazione degli Embeddings

**Cosa fa:**
Converte ogni chunk di testo in un vettore di numeri (chiamato "embedding").

**Perché serve:**
I computer non capiscono il linguaggio umano direttamente. Gli embeddings sono rappresentazioni numeriche del **significato** del testo. Testi con significati simili hanno embeddings simili.

**Come funziona:**
Inviamo ogni chunk al modello Gemini (`gemini-embedding-001`) tramite API, e questo ci restituisce un vettore di 768 numeri.

**Input:**
- Lista di chunk di testo

**Output:**
- Lista di embeddings (vettori di 768 numeri ciascuno)

**Esempio concettuale:**
```
Chunk: "20 giorni di ferie"
Embedding: [0.123, -0.456, 0.789, ..., 0.321] (768 numeri)

Chunk simile: "20 giorni di vacanza"
Embedding simile: [0.125, -0.450, 0.792, ..., 0.318] (numeri molto simili!)
```

---

### Step 5: Salvataggio in FAISS

**Cosa fa:**
Salva tutti gli embeddings in un database vettoriale chiamato FAISS.

**Perché serve:**
FAISS è ottimizzato per cercare velocemente tra milioni di vettori. Quando faremo una domanda, dovremo trovare rapidamente i chunk più simili.

**Come funziona:**
1. Crea un "indice" FAISS (una struttura dati specializzata)
2. Aggiunge tutti gli embeddings all'indice
3. Salva l'indice su disco (`data/vector_store/faiss_index.bin`)
4. Salva anche i metadati (informazioni sui chunk) in un file JSON separato

**Input:**
- Lista di embeddings
- Lista di metadati (quale chunk, da quale file, testo originale)

**Output:**
- File `faiss_index.bin` (database vettoriale)
- File `metadata.json` (informazioni sui chunk)

---

### Step 6: Domanda dell'Utente

**Cosa fa:**
L'utente scrive una domanda nell'interfaccia.

**Perché serve:**
È il punto di partenza per la ricerca.

**Input:**
- Testo della domanda (es. "Quanti giorni di ferie ho?")

**Output:**
- La domanda viene passata al sistema di retrieval

---

### Step 7: Retrieval dei Chunk (Recupero)

**Cosa fa:**
Trova i chunk più rilevanti per rispondere alla domanda.

**Perché serve:**
Non possiamo inviare tutti i documenti a Gemini (sarebbe troppo lungo e costoso). Dobbiamo trovare solo i pezzi rilevanti.

**Come funziona:**

1. **Embedding della domanda:**
   - La domanda viene convertita in un embedding (stesso processo dello step 4)
   - Es. "Quanti giorni di ferie?" → [0.234, -0.567, 0.890, ...]

2. **Ricerca in FAISS:**
   - FAISS calcola la **distanza** tra l'embedding della domanda e tutti gli embeddings salvati
   - Trova i 3 chunk con la distanza più piccola (= più simili)
   - La distanza misura quanto sono "vicini" due embeddings nel loro spazio vettoriale

3. **Recupero dei metadati:**
   - Per ogni chunk trovato, recupera:
     - Il testo originale
     - Il nome del file sorgente
     - L'ID del chunk

**Input:**
- Embedding della domanda

**Output:**
- Lista di 3 risultati, ciascuno con:
  - Distanza (quanto è simile alla domanda)
  - Testo del chunk
  - Nome del file sorgente
  - ID del chunk

**Esempio:**
```
Domanda: "Quanti giorni di ferie ho?"

Risultati:
1. Distanza: 0.234
   File: policy_aziendale.pdf
   Chunk: "I dipendenti hanno diritto a 20 giorni di ferie all'anno..."

2. Distanza: 0.567
   File: contratto.pdf
   Chunk: "Le ferie non godute possono essere riportate all'anno successivo..."

3. Distanza: 0.789
   File: regolamento.pdf
   Chunk: "Durante le ferie il dipendente mantiene il diritto alla retribuzione..."
```

---

### Step 8: Costruzione del Contesto

**Cosa fa:**
Combina i chunk trovati in un unico testo da inviare a Gemini.

**Perché serve:**
Gemini ha bisogno di vedere sia la domanda che il contesto (i chunk rilevanti) per generare una risposta accurata.

**Come funziona:**
Crea una stringa di testo che contiene:
- I chunk trovati
- Le loro fonti
- Un'intestazione per ogni chunk

**Input:**
- Lista dei 3 chunk più rilevanti

**Output:**
- Una stringa di testo formattata

**Esempio:**
```
Source 1: policy_aziendale.pdf
Content:
I dipendenti hanno diritto a 20 giorni di ferie all'anno...

Source 2: contratto.pdf
Content:
Le ferie non godute possono essere riportate all'anno successivo...

Source 3: regolamento.pdf
Content:
Durante le ferie il dipendente mantiene il diritto alla retribuzione...
```

---

### Step 9: Generazione della Risposta con Gemini

**Cosa fa:**
Invia il contesto + la domanda a Gemini per generare la risposta finale.

**Perché serve:**
Gemini è un modello linguistico avanzato (LLM) che sa:
- Leggere e capire il contesto
- Estrarre le informazioni rilevanti
- Generare risposte in linguaggio naturale
- Rispondere in modo coerente e chiaro

**Come funziona:**

1. **Costruzione del prompt:**
   Crea un messaggio strutturato per Gemini che include:
   - Istruzioni su come comportarsi
   - Il contesto (i chunk trovati)
   - La domanda

2. **Invio a Gemini:**
   Invia il prompt al modello `gemini-2.5-flash` tramite API

3. **Ricezione della risposta:**
   Gemini genera una risposta basata SOLO sul contesto fornito

**Input:**
- Prompt contenente contesto + domanda

**Output:**
- Risposta in linguaggio naturale

**Esempio di prompt completo:**
```
You are an assistant that answers questions using the provided company documents.

Use only the context below to answer.
If the answer is not present in the context, say that the information was not found in the uploaded documents.

Context:
Source 1: policy_aziendale.pdf
Content:
I dipendenti hanno diritto a 20 giorni di ferie all'anno...

Source 2: contratto.pdf
Content:
Le ferie non godute possono essere riportate all'anno successivo...

Question:
Quanti giorni di ferie ho?
```

**Risposta di Gemini:**
```
Secondo la policy aziendale, hai diritto a 20 giorni di ferie all'anno. Le ferie non godute possono essere riportate all'anno successivo.
```

---

### Step 10: Visualizzazione della Risposta

**Cosa fa:**
Mostra all'utente:
- La risposta generata da Gemini
- I chunk originali utilizzati (con nome file e distanza)

**Perché serve:**
L'utente può:
- Leggere la risposta
- Verificare le fonti
- Capire da quale documento proviene l'informazione

**Input:**
- Risposta di Gemini
- Lista dei chunk utilizzati

**Output:**
- Visualizzazione nell'interfaccia Streamlit

---

## 3. Architettura del Progetto

### Panoramica dei File

Il progetto è organizzato in modo modulare. Ogni file ha una responsabilità specifica:

```
AI-Enterprise-Knowledge-Extractor/
│
├── app.py                    # 🎯 File principale - interfaccia Streamlit
├── config.py                 # ⚙️ Configurazione - API key e impostazioni
│
├── modules/
│   ├── document_loader.py    # 📄 Estrazione testo da PDF/DOCX
│   ├── text_splitter.py      # ✂️ Divisione testo in chunk
│   ├── embeddings.py         # 🧮 Generazione embeddings con Gemini
│   ├── vector_store.py       # 💾 Gestione database FAISS
│   └── chat_engine.py        # 🤖 Orchestrazione retrieval + generazione
│
└── data/
    ├── documents/            # 📁 Documenti caricati
    └── vector_store/         # 🗄️ Database FAISS + metadati
```

---

### Ruolo di Ogni File

#### 1. **app.py** - Il Direttore d'Orchestra

**Ruolo:** È il file principale che coordina tutto. Contiene l'interfaccia utente Streamlit.

**Responsabilità:**
- Creare l'interfaccia web
- Gestire l'upload dei file
- Chiamare le funzioni degli altri moduli
- Mostrare i risultati all'utente

**Non fa:**
- Non estrae testo dai documenti (lo fa `document_loader.py`)
- Non genera embeddings (lo fa `embeddings.py`)
- Non gestisce FAISS (lo fa `vector_store.py`)

**Analogia:** È come il regista di un film. Non recita, non fa la fotografia, non monta. Ma coordina tutti.

---

#### 2. **config.py** - Il Centro di Configurazione

**Ruolo:** Contiene tutte le impostazioni e costanti del progetto.

**Responsabilità:**
- Caricare la chiave API da `.env`
- Definire i nomi dei modelli Gemini da usare
- Definire le impostazioni dei chunk (dimensione e overlap)
- Definire i percorsi delle cartelle

**Perché è importante:**
Se vuoi cambiare qualcosa (es. la dimensione dei chunk), modifichi solo questo file e tutto il resto funziona automaticamente.

---

#### 3. **document_loader.py** - L'Estrattore di Testo

**Ruolo:** Legge i file PDF e DOCX ed estrae il testo.

**Responsabilità:**
- Leggere file PDF pagina per pagina
- Leggere file DOCX paragrafo per paragrafo
- Restituire tutto il testo come una singola stringa

**Non fa:**
- Non divide il testo in chunk (lo fa `text_splitter.py`)
- Non genera embeddings (lo fa `embeddings.py`)

---

#### 4. **text_splitter.py** - Il Taglierino

**Ruolo:** Divide il testo lungo in pezzi più piccoli.

**Responsabilità:**
- Prendere una stringa di testo
- Dividerla in chunk di dimensione fissa
- Creare un overlap tra i chunk
- Restituire una lista di chunk

**Non fa:**
- Non estrae il testo (lo fa `document_loader.py`)
- Non genera embeddings (lo fa `embeddings.py`)

---

#### 5. **embeddings.py** - Il Traduttore in Numeri

**Ruolo:** Converte il testo in embeddings (vettori numerici).

**Responsabilità:**
- Creare un client per comunicare con l'API Gemini
- Inviare testo a Gemini
- Ricevere gli embeddings
- Gestire sia singoli testi che liste di testi

**Non fa:**
- Non salva gli embeddings (lo fa `vector_store.py`)
- Non cerca nel database (lo fa `vector_store.py`)

---

#### 6. **vector_store.py** - Il Custode del Database

**Ruolo:** Gestisce il database vettoriale FAISS.

**Responsabilità:**
- Creare l'indice FAISS
- Salvare gli embeddings nell'indice
- Salvare i metadati su disco
- Caricare l'indice da disco
- Cercare i chunk più simili dato un embedding

**Non fa:**
- Non genera embeddings (lo fa `embeddings.py`)
- Non genera la risposta finale (lo fa `chat_engine.py`)

---

#### 7. **chat_engine.py** - L'Orchestratore Intelligente

**Ruolo:** Coordina il processo di risposta alla domanda.

**Responsabilità:**
- Embedare la domanda (usando `embeddings.py`)
- Cercare i chunk rilevanti (usando `vector_store.py`)
- Costruire il contesto dai chunk trovati
- Inviare il prompt a Gemini
- Restituire la risposta finale

**Non fa:**
- Non gestisce l'interfaccia (lo fa `app.py`)
- Non crea il database FAISS (lo fa `vector_store.py`)

---

### Come i File Comunicano Tra Loro

Ecco il flusso completo delle chiamate quando l'utente carica un documento:

```
1. app.py
   ↓ chiama
2. document_loader.load_document(file_path)
   → restituisce: testo completo
   ↓
3. text_splitter.split_text(testo)
   → restituisce: lista di chunk
   ↓
4. embeddings.embed_texts(chunk)
   → restituisce: lista di embeddings
   ↓
5. vector_store.add_embeddings_to_index(embeddings, metadata)
   → salva su disco
```

Ecco il flusso quando l'utente fa una domanda:

```
1. app.py
   ↓ chiama
2. chat_engine.answer_question(domanda)
   ↓ all'interno chiama:
   ├─→ embeddings.embed_text(domanda)
   │   → restituisce: embedding della domanda
   ├─→ vector_store.search_similar_chunks(embedding)
   │   → restituisce: 3 chunk più rilevanti
   └─→ Gemini API
       → restituisce: risposta finale
```

---

## 4. Spiegazione del Codice File per File

### File 1: config.py

#### Scopo del File
Questo file è il centro di configurazione del progetto. Contiene tutte le costanti e impostazioni che possono essere modificate in un unico posto.

#### Import e Caricamento Variabili d'Ambiente

```python
import os
from dotenv import load_dotenv

load_dotenv()
```

**Cosa fa:**
- `import os`: importa il modulo per interagire con il sistema operativo
- `from dotenv import load_dotenv`: importa la funzione per caricare variabili da `.env`
- `load_dotenv()`: cerca un file `.env` nella directory corrente e carica tutte le variabili

**Perché:**
Le chiavi API sono sensibili e non vanno mai inserite direttamente nel codice. Il file `.env` non viene caricato su GitHub (è nel `.gitignore`).

#### Variabili di Configurazione

```python
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
```

**Cosa fa:**
Legge la variabile d'ambiente `GEMINI_API_KEY` dal file `.env`.

**Come funziona il file .env:**
```
GEMINI_API_KEY=la_tua_chiave_qui
```

```python
GENERATION_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "gemini-embedding-001"
```

**Cosa fa:**
Definisce quali modelli Gemini usare:
- `gemini-2.5-flash`: modello per generare risposte (veloce ed efficiente)
- `gemini-embedding-001`: modello per generare embeddings

```python
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
```

**Cosa fa:**
Definisce come dividere il testo:
- Ogni chunk sarà lungo 500 caratteri
- Ci sarà un overlap di 50 caratteri tra chunk consecutivi

```python
DOCUMENTS_DIR = "data/documents"
VECTOR_STORE_DIR = "data/vector_store"
```

**Cosa fa:**
Definisce dove salvare:
- I documenti caricati
- Il database FAISS e i metadati

```python
FAISS_INDEX_FILE = os.path.join(VECTOR_STORE_DIR, "faiss_index.bin")
METADATA_FILE = os.path.join(VECTOR_STORE_DIR, "metadata.json")
```

**Cosa fa:**
Definisce i percorsi completi dei file:
- `os.path.join()` unisce le parti del percorso in modo corretto per il sistema operativo
- Risultato: `"data/vector_store/faiss_index.bin"` e `"data/vector_store/metadata.json"`

---

### File 2: document_loader.py

#### Scopo del File
Estrae il testo dai documenti PDF e DOCX.

#### Import

```python
from pypdf import PdfReader
from docx import Document
```

**Cosa fa:**
- `PdfReader`: classe per leggere file PDF
- `Document`: classe per leggere file DOCX (Word)

#### Funzione: load_pdf

```python
def load_pdf(file_path: str) -> str:
```

**Firma della funzione:**
- **Input:** `file_path` (stringa) - percorso del file PDF
- **Output:** stringa con tutto il testo del PDF

**Codice riga per riga:**

```python
text = []
```
Crea una lista vuota dove salvare il testo di ogni pagina.

```python
reader = PdfReader(file_path)
```
Crea un oggetto `PdfReader` che sa come leggere il PDF.

```python
for page in reader.pages:
```
Cicla su tutte le pagine del PDF. `reader.pages` è una lista di oggetti pagina.

```python
page_text = page.extract_text()
```
Estrae il testo dalla pagina corrente.

```python
if page_text:
    text.append(page_text)
```
Se la pagina contiene testo (non è vuota), lo aggiunge alla lista `text`.

```python
return "\n".join(text)
```
Unisce tutti i pezzi di testo con un "a capo" (`\n`) tra l'uno e l'altro, e restituisce la stringa finale.

#### Funzione: load_docx

```python
def load_docx(file_path: str) -> str:
```

**Firma della funzione:**
- **Input:** `file_path` (stringa) - percorso del file DOCX
- **Output:** stringa con tutto il testo del DOCX

**Codice riga per riga:**

```python
doc = Document(file_path)
```
Crea un oggetto `Document` che rappresenta il file Word.

```python
text = []
```
Lista vuota per salvare i paragrafi.

```python
for paragraph in doc.paragraphs:
```
Cicla su tutti i paragrafi del documento. `doc.paragraphs` è una lista di oggetti paragrafo.

```python
if paragraph.text.strip():
```
Controlla se il paragrafo contiene testo (`.strip()` rimuove spazi vuoti all'inizio e alla fine).

```python
text.append(paragraph.text)
```
Aggiunge il testo del paragrafo alla lista.

```python
return "\n".join(text)
```
Unisce tutti i paragrafi con un "a capo" e restituisce la stringa finale.

#### Funzione: load_document

```python
def load_document(file_path: str) -> str:
```

**Firma della funzione:**
- **Input:** `file_path` (stringa) - percorso del file
- **Output:** stringa con tutto il testo

**Scopo:**
Funzione "intelligente" che decide automaticamente se chiamare `load_pdf` o `load_docx` in base all'estensione del file.

**Codice riga per riga:**

```python
file_path_lower = file_path.lower()
```
Converte il percorso in minuscolo (così `.PDF` e `.pdf` sono trattati ugualmente).

```python
if file_path_lower.endswith(".pdf"):
    return load_pdf(file_path)
```
Se il file finisce con `.pdf`, chiama `load_pdf` e restituisce il risultato.

```python
if file_path_lower.endswith(".docx"):
    return load_docx(file_path)
```
Se il file finisce con `.docx`, chiama `load_docx` e restituisce il risultato.

```python
raise ValueError("Unsupported file format. Only PDF and DOCX are allowed.")
```
Se il file non è né PDF né DOCX, genera un errore con un messaggio chiaro.

---

### File 3: text_splitter.py

#### Scopo del File
Divide un testo lungo in chunk (pezzi) più piccoli con overlap.

#### Funzione: split_text

```python
def split_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50
) -> list[str]:
```

**Firma della funzione:**
- **Input:**
  - `text`: la stringa di testo da dividere
  - `chunk_size`: lunghezza di ogni chunk (default 500 caratteri)
  - `chunk_overlap`: quanti caratteri si sovrappongono tra un chunk e il successivo (default 50)
- **Output:** lista di stringhe (i chunk)

**Codice riga per riga:**

```python
if not text.strip():
    return []
```
Se il testo è vuoto o contiene solo spazi, restituisce una lista vuota (non c'è niente da dividere).

```python
chunks = []
start = 0
text_length = len(text)
```
- `chunks`: lista dove salvare i chunk
- `start`: posizione di inizio del chunk corrente (parte da 0)
- `text_length`: lunghezza totale del testo

```python
while start < text_length:
```
Continua finché non abbiamo processato tutto il testo.

```python
end = start + chunk_size
```
Calcola dove finisce il chunk corrente. Se `start=0` e `chunk_size=500`, allora `end=500`.

```python
chunk = text[start:end]
```
Estrae il pezzo di testo dalla posizione `start` a `end`. In Python, `text[0:500]` prende i primi 500 caratteri.

```python
chunks.append(chunk)
```
Aggiunge il chunk alla lista.

```python
start += chunk_size - chunk_overlap
```
Aggiorna la posizione di inizio per il prossimo chunk.

**Esempio numerico:**
- Primo chunk: `start=0`, `end=500`
- Secondo chunk: `start=450` (500-50), `end=950`
- Terzo chunk: `start=900` (950-50), `end=1400`

Nota come c'è un overlap di 50 caratteri: i caratteri 450-500 sono sia nel primo che nel secondo chunk.

```python
return chunks
```
Restituisce la lista di tutti i chunk.

---

### File 4: embeddings.py

#### Scopo del File
Genera embeddings (vettori numerici) dal testo usando l'API Gemini.

#### Import

```python
from google import genai
from config import GEMINI_API_KEY, EMBEDDING_MODEL
```

**Cosa fa:**
- `genai`: modulo ufficiale di Google per usare le API Gemini
- Importa la chiave API e il nome del modello da `config.py`

#### Funzione: get_genai_client

```python
def get_genai_client():
```

**Scopo:**
Crea e restituisce un client per comunicare con l'API Gemini.

**Codice riga per riga:**

```python
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing.")
```
Se la chiave API non è stata caricata (è `None` o vuota), genera un errore.

```python
client = genai.Client(api_key=GEMINI_API_KEY)
```
Crea un oggetto `Client` passando la chiave API. Questo oggetto sa come comunicare con i server di Google.

```python
return client
```
Restituisce il client.

#### Funzione: embed_text

```python
def embed_text(text: str) -> list[float]:
```

**Firma della funzione:**
- **Input:** `text` (stringa) - il testo da convertire in embedding
- **Output:** lista di numeri float (l'embedding)

**Codice riga per riga:**

```python
client = get_genai_client()
```
Ottiene il client per comunicare con Gemini.

```python
response = client.models.embed_content(
    model=EMBEDDING_MODEL,
    contents=text
)
```
Fa una chiamata API a Gemini:
- `.models.embed_content()`: metodo per generare embeddings
- `model=EMBEDDING_MODEL`: quale modello usare ("gemini-embedding-001")
- `contents=text`: il testo da embedare

**Cosa riceve:**
Un oggetto `response` che contiene gli embeddings.

```python
return response.embeddings[0].values
```
- `response.embeddings`: lista di embeddings (normalmente contiene un solo elemento)
- `[0]`: prendiamo il primo (e unico) embedding
- `.values`: i valori numerici dell'embedding
- Restituisce: lista di 768 numeri float

#### Funzione: embed_texts

```python
def embed_texts(texts: list[str]) -> list[list[float]]:
```

**Firma della funzione:**
- **Input:** `texts` (lista di stringhe) - i testi da convertire
- **Output:** lista di embeddings (lista di liste di float)

**Differenza con embed_text:**
Questa funzione gestisce **più testi contemporaneamente**, è più efficiente perché fa una sola chiamata API invece di tante chiamate separate.

**Codice riga per riga:**

```python
client = get_genai_client()
```
Ottiene il client.

```python
response = client.models.embed_content(
    model=EMBEDDING_MODEL,
    contents=texts
)
```
Invia una lista di testi. Gemini genera un embedding per ogni testo.

```python
return [item.values for item in response.embeddings]
```
Questa è una **list comprehension** (forma compatta di Python per creare liste).

Equivalente esteso:
```python
result = []
for item in response.embeddings:
    result.append(item.values)
return result
```

Restituisce: `[[...], [...], [...]]` - una lista di embeddings.

---

### File 5: vector_store.py

#### Scopo del File
Gestisce il database vettoriale FAISS: crea, salva, carica e cerca nel database.

#### Import

```python
import json
import os
import faiss
import numpy as np

from config import FAISS_INDEX_FILE, METADATA_FILE
```

**Cosa fa:**
- `json`: per salvare/caricare i metadati in formato JSON
- `os`: per operazioni sui file
- `faiss`: libreria per la ricerca vettoriale
- `numpy`: libreria per operazioni matematiche su array
- Importa i percorsi dei file da `config.py`

#### Funzione: create_faiss_index

```python
def create_faiss_index(dimension: int):
```

**Firma della funzione:**
- **Input:** `dimension` (int) - dimensione dei vettori (768 per Gemini)
- **Output:** oggetto indice FAISS

**Codice:**

```python
index = faiss.IndexFlatL2(dimension)
```
Crea un indice FAISS di tipo "IndexFlatL2":
- **Flat**: cerca esaminando tutti i vettori (ricerca esatta, non approssimata)
- **L2**: usa la distanza euclidea (L2) per misurare la similarità

**Come funziona la distanza L2:**
Dati due vettori `A` e `B`, la distanza L2 è:
```
distanza = sqrt((A₁-B₁)² + (A₂-B₂)² + ... + (Aₙ-Bₙ)²)
```
Distanza piccola = vettori simili.

```python
return index
```
Restituisce l'indice vuoto (senza dati).

#### Funzione: save_index

```python
def save_index(index, metadata: list[dict]):
```

**Firma della funzione:**
- **Input:**
  - `index`: l'indice FAISS da salvare
  - `metadata`: lista di dizionari con informazioni sui chunk
- **Output:** nessuno (salva su disco)

**Codice riga per riga:**

```python
os.makedirs(os.path.dirname(FAISS_INDEX_FILE), exist_ok=True)
```
Crea la cartella `data/vector_store/` se non esiste:
- `os.path.dirname()`: ottiene la cartella del percorso
- `exist_ok=True`: non genera errore se la cartella esiste già

```python
faiss.write_index(index, FAISS_INDEX_FILE)
```
Salva l'indice FAISS su disco in formato binario.

```python
with open(METADATA_FILE, "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)
```
Salva i metadati in formato JSON:
- `with open()`: apre il file (si chiude automaticamente alla fine)
- `"w"`: modalità scrittura
- `encoding="utf-8"`: supporta caratteri speciali
- `json.dump()`: scrive i dati in formato JSON
- `ensure_ascii=False`: mantiene i caratteri non-ASCII (es. accentate)
- `indent=2`: formatta il JSON in modo leggibile

#### Funzione: load_index

```python
def load_index():
```

**Firma della funzione:**
- **Input:** nessuno
- **Output:** tupla `(index, metadata)`

**Codice riga per riga:**

```python
if not os.path.exists(FAISS_INDEX_FILE):
    return None, []
```
Se il file dell'indice non esiste, restituisce `None` e lista vuota (non c'è niente da caricare).

```python
index = faiss.read_index(FAISS_INDEX_FILE)
```
Carica l'indice FAISS dal disco.

```python
metadata = []
if os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = json.load(f)
```
Carica i metadati dal file JSON se esiste:
- `"r"`: modalità lettura
- `json.load()`: legge il JSON e lo converte in strutture Python

```python
return index, metadata
```
Restituisce sia l'indice che i metadati.

#### Funzione: add_embeddings_to_index

```python
def add_embeddings_to_index(embeddings: list[list[float]], metadata: list[dict]):
```

**Firma della funzione:**
- **Input:**
  - `embeddings`: lista di embeddings
  - `metadata`: lista di metadati (un dizionario per ogni embedding)
- **Output:** nessuno (crea e salva l'indice)

**Codice riga per riga:**

```python
if not embeddings:
    raise ValueError("No embeddings provided.")
```
Controlla che ci siano embeddings, altrimenti genera errore.

```python
vectors = np.array(embeddings, dtype="float32")
```
Converte la lista di embeddings in un array NumPy:
- NumPy è più efficiente per calcoli matematici
- `dtype="float32"`: usa numeri float a 32 bit (FAISS li richiede)

```python
dimension = vectors.shape[1]
```
Ottiene la dimensione dei vettori:
- `.shape[1]`: seconda dimensione dell'array
- Se `vectors` ha forma `(100, 768)`, significa 100 vettori di 768 dimensioni
- `dimension` sarà 768

```python
index = create_faiss_index(dimension)
```
Crea un nuovo indice FAISS vuoto.

```python
index.add(vectors)
```
Aggiunge tutti i vettori all'indice. FAISS li organizza internamente per ricerche veloci.

```python
save_index(index, metadata)
```
Salva l'indice e i metadati su disco.

#### Funzione: search_similar_chunks

```python
def search_similar_chunks(query_embedding: list[float], top_k: int = 3):
```

**Firma della funzione:**
- **Input:**
  - `query_embedding`: l'embedding della domanda
  - `top_k`: quanti risultati restituire (default 3)
- **Output:** lista di risultati (dizionari con distanza e metadati)

**Codice riga per riga:**

```python
index, metadata = load_index()
```
Carica l'indice e i metadati dal disco.

```python
if index is None:
    return []
```
Se l'indice non esiste, restituisce lista vuota.

```python
query_vector = np.array([query_embedding], dtype="float32")
```
Converte l'embedding in array NumPy:
- Nota le doppie parentesi quadre `[[...]]`: FAISS richiede un array 2D
- Se l'embedding è `[0.1, 0.2, ...]`, diventa `[[0.1, 0.2, ...]]`

```python
distances, indices = index.search(query_vector, top_k)
```
Cerca i `top_k` vettori più simili:
- `distances`: array con le distanze (più piccola = più simile)
- `indices`: array con gli indici dei vettori trovati

**Esempio:**
```python
distances = [[0.234, 0.567, 0.789]]  # 3 distanze
indices = [[12, 45, 78]]              # chunk 12, 45 e 78
```

```python
results = []
```
Lista per salvare i risultati finali.

```python
for i, idx in enumerate(indices[0]):
```
Cicla sugli indici trovati:
- `indices[0]`: prende la prima (e unica) riga dell'array
- `enumerate()`: fornisce sia l'indice del ciclo (`i`) che il valore (`idx`)

```python
if idx == -1:
    continue
```
FAISS restituisce `-1` se non trova abbastanza risultati. Lo saltiamo.

```python
result = {
    "distance": float(distances[0][i]),
    "metadata": metadata[idx]
}
```
Crea un dizionario con:
- La distanza (convertita in float Python)
- I metadati del chunk (preso dalla lista `metadata` alla posizione `idx`)

```python
results.append(result)
```
Aggiunge il risultato alla lista.

```python
return results
```
Restituisce tutti i risultati.

---

### File 6: chat_engine.py

#### Scopo del File
Orchestrazione del processo di risposta: embed la domanda, cerca i chunk, costruisce il contesto, genera la risposta.

#### Import

```python
from google import genai

from config import GEMINI_API_KEY, GENERATION_MODEL
from modules.embeddings import embed_text
from modules.vector_store import search_similar_chunks
```

**Cosa fa:**
- Importa il modulo Gemini
- Importa configurazioni da `config.py`
- Importa funzioni dagli altri moduli

#### Funzione: get_genai_client

```python
def get_genai_client():
```

Stessa funzione di `embeddings.py`. Crea il client Gemini.

#### Funzione: build_context

```python
def build_context(results: list[dict]) -> str:
```

**Firma della funzione:**
- **Input:** `results` - lista di risultati da FAISS (distanza + metadati)
- **Output:** stringa di testo formattata (il contesto)

**Codice riga per riga:**

```python
context_parts = []
```
Lista per salvare le parti del contesto.

```python
for i, item in enumerate(results, start=1):
```
Cicla sui risultati:
- `enumerate(..., start=1)`: conta da 1 invece che da 0

```python
chunk_text = item["metadata"].get("text", "")
source = item["metadata"].get("source", "Unknown source")
```
Estrae informazioni dal dizionario:
- `.get("text", "")`: prende il valore di "text", se non esiste restituisce stringa vuota
- `.get("source", "Unknown source")`: prende la sorgente, se non esiste restituisce "Unknown source"

```python
context_parts.append(
    f"Source {i}: {source}\n"
    f"Content:\n{chunk_text}\n"
)
```
Crea una stringa formattata usando **f-string**:
- `{i}`: numero del chunk (1, 2, 3...)
- `{source}`: nome del file
- `{chunk_text}`: il testo del chunk

```python
return "\n".join(context_parts)
```
Unisce tutte le parti con un "a capo" e restituisce la stringa finale.

**Esempio di output:**
```
Source 1: policy_aziendale.pdf
Content:
I dipendenti hanno diritto a 20 giorni di ferie...

Source 2: contratto.pdf
Content:
Le ferie non godute possono essere riportate...
```

#### Funzione: answer_question

```python
def answer_question(question: str, top_k: int = 3) -> dict:
```

**Firma della funzione:**
- **Input:**
  - `question`: la domanda dell'utente
  - `top_k`: quanti chunk recuperare (default 3)
- **Output:** dizionario con "answer" e "sources"

**Questa è la funzione più importante del progetto. Coordina tutto il processo.**

**Codice riga per riga:**

```python
client = get_genai_client()
```
Ottiene il client Gemini.

```python
query_embedding = embed_text(question)
```
**Step 1:** Converte la domanda in embedding usando la funzione di `embeddings.py`.

```python
results = search_similar_chunks(query_embedding, top_k=top_k)
```
**Step 2:** Cerca i chunk più simili usando la funzione di `vector_store.py`.

```python
if not results:
    return {
        "answer": "No indexed documents found. Please upload and process documents first.",
        "sources": []
    }
```
Se non ci sono risultati (database vuoto), restituisce un messaggio di errore.

```python
context = build_context(results)
```
**Step 3:** Costruisce il contesto dai chunk trovati.

```python
prompt = f"""
You are an assistant that answers questions using the provided company documents.

Use only the context below to answer.
If the answer is not present in the context, say that the information was not found in the uploaded documents.

Context:
{context}

Question:
{question}
"""
```
**Step 4:** Costruisce il prompt per Gemini:
- Istruzioni su come comportarsi
- Il contesto (chunk trovati)
- La domanda

**Perché queste istruzioni?**
- "Use only the context below": evitiamo che Gemini inventi informazioni
- "If the answer is not present": Gemini deve ammettere se non sa la risposta

```python
response = client.models.generate_content(
    model=GENERATION_MODEL,
    contents=prompt
)
```
**Step 5:** Invia il prompt a Gemini e ottiene la risposta:
- `generate_content()`: metodo per generare testo
- `model=GENERATION_MODEL`: usa "gemini-2.5-flash"
- `contents=prompt`: il testo da elaborare

```python
return {
    "answer": response.text,
    "sources": results
}
```
**Step 6:** Restituisce un dizionario con:
- `answer`: la risposta generata da Gemini
- `sources`: i chunk utilizzati (per mostrare le fonti)

---

### File 7: app.py

#### Scopo del File
Interfaccia utente Streamlit. Coordina tutto il flusso del progetto.

#### Import

```python
import os
import streamlit as st

from config import (
    GEMINI_API_KEY,
    DOCUMENTS_DIR,
    VECTOR_STORE_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

from modules.document_loader import load_document
from modules.text_splitter import split_text
from modules.embeddings import embed_texts
from modules.vector_store import add_embeddings_to_index
from modules.chat_engine import answer_question
```

**Cosa fa:**
- Importa Streamlit (framework per l'interfaccia web)
- Importa tutte le configurazioni
- Importa tutte le funzioni necessarie dai moduli

#### Setup Iniziale

```python
os.makedirs(DOCUMENTS_DIR, exist_ok=True)
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
```
Crea le cartelle per i dati se non esistono.

```python
st.set_page_config(
    page_title="AI Enterprise Knowledge Extractor",
    layout="wide"
)
```
Configura la pagina Streamlit:
- Titolo della scheda del browser
- Layout largo (usa tutta la larghezza dello schermo)

```python
st.title("AI Enterprise Knowledge Extractor")
```
Mostra il titolo principale nell'interfaccia.

```python
col1, col2, col3 = st.columns(3)

with col2:
    st.image(image=r"E:\Ambienti\cs50\patrick_project\data\ChatGPT Image Mar 7, 2026, 11_13_38 AM.png")
```
Crea 3 colonne e mostra un'immagine nella colonna centrale (per centrare l'immagine).

```python
st.write("Upload company documents, index them, and ask questions about their content.")
```
Mostra una descrizione.

#### Controllo API Key

```python
if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY not found. Please add it inside the .env file.")
    st.stop()
```
Se la chiave API non è caricata:
- Mostra un errore rosso
- `st.stop()`: ferma l'esecuzione dell'app

```python
st.success("Gemini API key loaded successfully.")
```
Se arriviamo qui, la chiave è OK. Mostra un messaggio verde.

#### Session State

Streamlit ricarica lo script a ogni interazione. Il **session state** mantiene i dati tra un reload e l'altro.

```python
if "documents_processed" not in st.session_state:
    st.session_state.documents_processed = False
```
Se la variabile non esiste ancora, la crea e la inizializza a `False`.

```python
if "last_uploaded_files" not in st.session_state:
    st.session_state.last_uploaded_files = []
```
Inizializza la lista dei file caricati.

#### Sezione Upload

```python
st.header("1. Upload documents")
```
Mostra un'intestazione di sezione.

```python
uploaded_files = st.file_uploader(
    "Upload PDF or DOCX files",
    type=["pdf", "docx"],
    accept_multiple_files=True
)
```
Crea un widget per caricare file:
- `type=["pdf", "docx"]`: accetta solo questi formati
- `accept_multiple_files=True`: permette di caricare più file
- Restituisce una lista di oggetti file

```python
if uploaded_files:
    st.write(f"Uploaded files: {len(uploaded_files)}")
```
Se l'utente ha caricato file, mostra quanti.

#### Sezione Processamento

```python
st.header("2. Process documents")
```
Intestazione della sezione.

```python
if st.button("Process documents"):
```
Crea un pulsante. Il codice dentro l'`if` viene eseguito solo quando l'utente clicca il pulsante.

```python
if not uploaded_files:
    st.warning("Please upload at least one PDF or DOCX file.")
```
Se non ci sono file caricati, mostra un warning giallo.

```python
else:
    all_chunks = []
    all_metadata = []
```
Inizializza due liste per raccogliere tutti i chunk e metadati di tutti i file.

```python
with st.spinner("Processing documents..."):
```
Mostra uno spinner (animazione di caricamento) con il messaggio. Il codice dentro viene eseguito mentre lo spinner è visibile.

```python
for uploaded_file in uploaded_files:
```
Cicla su ogni file caricato.

```python
file_name = uploaded_file.name
save_path = os.path.join(DOCUMENTS_DIR, file_name)
```
- `uploaded_file.name`: nome del file
- Costruisce il percorso completo dove salvare il file

```python
with open(save_path, "wb") as f:
    f.write(uploaded_file.getbuffer())
```
Salva il file su disco:
- `"wb"`: modalità scrittura binaria (i file non sono testo puro)
- `getbuffer()`: ottiene i dati del file
- `write()`: scrive i dati su disco

```python
try:
    document_text = load_document(save_path)
except Exception as e:
    st.error(f"Error reading {file_name}: {e}")
    continue
```
Prova a estrarre il testo:
- Se c'è un errore, lo cattura (`except`)
- Mostra l'errore
- `continue`: salta al prossimo file

```python
if not document_text.strip():
    st.warning(f"No text found inside {file_name}.")
    continue
```
Se il testo è vuoto, mostra un warning e salta al prossimo file.

```python
chunks = split_text(
    text=document_text,
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)
```
Divide il testo in chunk.

```python
for i, chunk in enumerate(chunks):
    all_chunks.append(chunk)
    all_metadata.append(
        {
            "source": file_name,
            "chunk_id": i,
            "text": chunk
        }
    )
```
Per ogni chunk:
- Aggiunge il chunk alla lista `all_chunks`
- Crea un dizionario di metadati e lo aggiunge a `all_metadata`

**Perché salviamo i metadati?**
Quando cerchiamo in FAISS, otteniamo solo gli indici. I metadati ci dicono da quale file proviene il chunk e qual è il testo originale.

```python
if not all_chunks:
    st.error("No valid text chunks were created.")
```
Se alla fine non ci sono chunk (tutti i file erano vuoti o danneggiati), mostra un errore.

```python
else:
    try:
        with st.spinner("Generating embeddings and saving to FAISS..."):
            embeddings = embed_texts(all_chunks)
            add_embeddings_to_index(embeddings, all_metadata)
```
- Genera gli embeddings per tutti i chunk
- Crea l'indice FAISS e salva

```python
st.session_state.documents_processed = True
st.session_state.last_uploaded_files = [f.name for f in uploaded_files]
```
Aggiorna il session state:
- Segna che i documenti sono stati processati
- Salva i nomi dei file

```python
st.success("Documents processed and indexed successfully.")
st.write(f"Total chunks created: {len(all_chunks)}")
```
Mostra messaggi di successo.

```python
except Exception as e:
    st.error(f"Error during embedding/indexing: {e}")
```
Cattura eventuali errori durante embedding o indicizzazione.

#### Sezione Chat

```python
st.header("3. Ask questions about your documents")
```
Intestazione della sezione domande.

```python
if st.session_state.documents_processed:
    st.info("Documents are ready. You can now ask questions.")
else:
    st.warning("Upload and process documents first.")
```
Mostra un messaggio diverso a seconda che i documenti siano stati processati o no.

```python
question = st.text_input("Write your question here")
```
Crea un campo di testo per la domanda. `question` contiene il testo inserito.

```python
if st.button("Ask"):
```
Pulsante per inviare la domanda.

```python
if not st.session_state.documents_processed:
    st.warning("Please process documents before asking a question.")
elif not question.strip():
    st.warning("Please enter a question.")
```
Controlli di validazione:
- Ci sono documenti processati?
- La domanda non è vuota?

```python
else:
    try:
        with st.spinner("Searching relevant chunks and generating answer..."):
            result = answer_question(question)
```
Chiama la funzione principale che:
1. Embed la domanda
2. Cerca in FAISS
3. Costruisce il contesto
4. Genera la risposta con Gemini

```python
st.subheader("Answer")
st.write(result["answer"])
```
Mostra la risposta.

```python
st.subheader("Retrieved sources")
if result["sources"]:
```
Se ci sono fonti, le mostra.

```python
for i, item in enumerate(result["sources"], start=1):
    metadata = item["metadata"]
```
Cicla sulle fonti.

```python
st.markdown(f"**Source {i}**")
st.write(f"**File:** {metadata.get('source', 'Unknown')}")
st.write(f"**Chunk ID:** {metadata.get('chunk_id', 'N/A')}")
st.write("**Chunk text:**")
st.code(metadata.get("text", ""), language="text")
st.write(f"**Distance:** {item.get('distance', 'N/A')}")
st.markdown("---")
```
Per ogni fonte mostra:
- Numero della fonte
- Nome del file
- ID del chunk
- Testo del chunk (in un blocco di codice)
- Distanza (quanto è simile alla domanda)
- Una linea separatrice

```python
else:
    st.write("No sources found.")
```
Se non ci sono fonti, lo dice.

```python
except Exception as e:
    st.error(f"Error while answering the question: {e}")
```
Cattura eventuali errori.

#### Sidebar

```python
with st.sidebar:
```
Il codice dentro appare nella barra laterale.

```python
st.header("Project info")
st.write("Simple local RAG with:")
st.write("- Streamlit")
st.write("- Gemini API")
st.write("- Embeddings")
st.write("- FAISS")
```
Mostra informazioni sul progetto.

```python
st.header("Chunk settings")
st.write(f"Chunk size: {CHUNK_SIZE}")
st.write(f"Chunk overlap: {CHUNK_OVERLAP}")
```
Mostra le impostazioni correnti dei chunk.

---

## 5. Spiegazione Dettagliata del Codice

### Parti Complesse del Codice

#### 1. Come Funziona l'Overlap nel Text Splitter

```python
while start < text_length:
    end = start + chunk_size
    chunk = text[start:end]
    chunks.append(chunk)
    start += chunk_size - chunk_overlap
```

**Spiegazione passo-passo con esempio concreto:**

Immaginiamo di avere un testo di 1200 caratteri:
- `chunk_size = 500`
- `chunk_overlap = 50`

**Iterazione 1:**
- `start = 0`
- `end = 0 + 500 = 500`
- `chunk = text[0:500]` → primi 500 caratteri
- Nuovo `start = 0 + 500 - 50 = 450`

**Iterazione 2:**
- `start = 450`
- `end = 450 + 500 = 950`
- `chunk = text[450:950]` → caratteri dal 450 al 950
- **Overlap:** i caratteri 450-500 sono in entrambi i chunk!
- Nuovo `start = 450 + 500 - 50 = 900`

**Iterazione 3:**
- `start = 900`
- `end = 900 + 500 = 1400` (oltre la lunghezza)
- `chunk = text[900:1400]` → Python si ferma automaticamente a 1200
- Nuovo `start = 1350` (oltre la lunghezza, il ciclo si ferma)

**Risultato:** 3 chunk con overlap di 50 caratteri.

---

#### 2. Come Funziona la List Comprehension in embed_texts

```python
return [item.values for item in response.embeddings]
```

**Forma estesa:**
```python
result = []
for item in response.embeddings:
    result.append(item.values)
return result
```

**Spiegazione:**
- `response.embeddings` è una lista di oggetti embedding
- Ogni oggetto ha un attributo `.values` (i numeri dell'embedding)
- La list comprehension crea una nuova lista prendendo `.values` da ogni elemento

**Esempio concreto:**
```python
response.embeddings = [
    Embedding(values=[0.1, 0.2, 0.3]),
    Embedding(values=[0.4, 0.5, 0.6]),
    Embedding(values=[0.7, 0.8, 0.9])
]

# La list comprehension produce:
[
    [0.1, 0.2, 0.3],
    [0.4, 0.5, 0.6],
    [0.7, 0.8, 0.9]
]
```

---

#### 3. Come Funziona la Ricerca FAISS

```python
query_vector = np.array([query_embedding], dtype="float32")
distances, indices = index.search(query_vector, top_k)
```

**Perché doppie parentesi quadre?**

FAISS si aspetta sempre un array 2D (anche se cerchiamo un solo vettore):
- Input corretto: `[[0.1, 0.2, 0.3]]` (shape: 1 x 3)
- Input sbagliato: `[0.1, 0.2, 0.3]` (shape: 3)

**Cosa restituisce `index.search()`?**

Due array:
1. `distances`: le distanze L2 dai vettori trovati
2. `indices`: gli indici dei vettori nell'indice

**Esempio:**
```python
# Abbiamo 100 chunk nell'indice
# Cerchiamo i top 3

distances = [[0.234, 0.567, 0.789]]
indices = [[12, 45, 78]]

# Significa:
# - Il chunk 12 ha distanza 0.234 (più simile)
# - Il chunk 45 ha distanza 0.567
# - Il chunk 78 ha distanza 0.789 (meno simile dei 3)
```

**Come si usa nella pratica:**
```python
for i, idx in enumerate(indices[0]):
    # i = 0, idx = 12 (primo risultato)
    # i = 1, idx = 45 (secondo risultato)
    # i = 2, idx = 78 (terzo risultato)
    
    distance = distances[0][i]
    chunk_data = metadata[idx]
```

---

#### 4. Come Funziona il Prompt per Gemini

```python
prompt = f"""
You are an assistant that answers questions using the provided company documents.

Use only the context below to answer.
If the answer is not present in the context, say that the information was not found in the uploaded documents.

Context:
{context}

Question:
{question}
"""
```

**Perché questo formato?**

1. **Ruolo chiaro:** "You are an assistant..." → Gemini sa come comportarsi

2. **Istruzione critica:** "Use only the context below" → Questo è il cuore del RAG. Evitiamo che Gemini inventi informazioni o usi la sua conoscenza generale.

3. **Gestione dell'incertezza:** "If the answer is not present..." → Gemini deve ammettere se non sa, invece di inventare.

4. **Contesto strutturato:** I chunk sono formattati in modo chiaro con sorgenti.

5. **Domanda esplicita:** La domanda è alla fine, dopo tutto il contesto.

**Esempio di prompt completo:**
```
You are an assistant that answers questions using the provided company documents.

Use only the context below to answer.
If the answer is not present in the context, say that the information was not found in the uploaded documents.

Context:
Source 1: policy_aziendale.pdf
Content:
I dipendenti hanno diritto a 20 giorni di ferie all'anno. Le ferie devono essere richieste con almeno 2 settimane di anticipo.

Source 2: contratto.pdf
Content:
Le ferie non godute possono essere riportate all'anno successivo fino a un massimo di 10 giorni.

Question:
Quanti giorni di ferie ho?
```

**Risposta di Gemini:**
```
Secondo la policy aziendale (policy_aziendale.pdf), hai diritto a 20 giorni di ferie all'anno. Le ferie devono essere richieste con almeno 2 settimane di anticipo. Inoltre, dal contratto risulta che le ferie non godute possono essere riportate all'anno successivo fino a un massimo di 10 giorni.
```

---

#### 5. Gestione degli Errori con Try-Except

```python
try:
    document_text = load_document(save_path)
except Exception as e:
    st.error(f"Error reading {file_name}: {e}")
    continue
```

**Spiegazione:**

- **`try:`** → Prova a eseguire il codice
- **`except Exception as e:`** → Se c'è un errore, catturalo in `e`
- **`st.error(...)`** → Mostra l'errore all'utente
- **`continue`** → Salta al prossimo file invece di fermare tutto

**Perché è importante:**
Se un file è corrotto, il programma non si blocca ma continua con gli altri file.

---

## 6. Concetti Tecnici Spiegati in Modo Semplice

### Che Cosa Sono gli Embeddings?

**Definizione semplice:**
Gli embeddings sono traduzioni del testo in vettori di numeri che rappresentano il **significato** del testo.

**Analogia:**
Immagina di dover spiegare il concetto di "cane" a un alieno che non conosce le parole ma capisce solo i numeri. Potresti dire:
- Dimensione: 60cm
- Peso: 20kg
- Amichevolezza: 9/10
- Pelo: lungo
- Zampe: 4

Questo "vettore" descrive il concetto di cane. Gli embeddings fanno la stessa cosa con significati più complessi.

**Esempio concreto:**
```
"20 giorni di ferie" → [0.123, -0.456, 0.789, ..., 0.321] (768 numeri)
"20 giorni di vacanza" → [0.125, -0.450, 0.792, ..., 0.318] (molto simile!)
"gatto" → [-0.789, 0.234, -0.123, ..., 0.567] (molto diverso)
```

**Proprietà magiche degli embeddings:**
- Testi con significato simile hanno embeddings simili
- Puoi fare operazioni matematiche sui significati
- Esempio: vettore("re") - vettore("uomo") + vettore("donna") ≈ vettore("regina")

---

### Che Cosa Fa FAISS?

**Definizione semplice:**
FAISS è un database specializzato per cercare velocemente tra milioni di vettori.

**Il problema che risolve:**
Hai 10.000 chunk, ognuno con un embedding di 768 numeri. Quando l'utente fa una domanda, devi trovare i 3 chunk più simili. Senza FAISS dovresti:
1. Calcolare la distanza tra la domanda e tutti i 10.000 chunk
2. Ordinare le distanze
3. Prendere i primi 3

Con 10.000 chunk va ancora bene, ma con 1 milione? FAISS usa strutture dati specializzate per fare questa operazione in millisecondi.

**Come funziona FAISS:**
- Organizza i vettori in una struttura simile a un albero
- Quando cerchi, non esamina tutti i vettori ma solo i "rami" più promettenti
- Nel nostro caso usiamo `IndexFlatL2` che è la versione più semplice (ricerca esatta)

**Distanza L2:**
È la formula matematica per misurare quanto sono "lontani" due vettori:
```
distanza(A, B) = sqrt((A₁-B₁)² + (A₂-B₂)² + ... + (Aₙ-Bₙ)²)
```
Distanza piccola = vettori simili = testi con significato simile.

---

### Che Cos'è il Chunking?

**Definizione semplice:**
Il chunking è dividere un testo lungo in pezzi più piccoli e gestibili.

**Perché serve:**

1. **Limiti dei modelli:** Gemini ha un limite di token (unità di testo). Non possiamo inviargli documenti interi di 100 pagine.

2. **Precisione della ricerca:** Se cerchi "policy ferie", vuoi trovare esattamente il paragrafo sulle ferie, non tutto il manuale di 50 pagine.

3. **Costi:** Ogni token inviato a Gemini costa. Inviare solo i chunk rilevanti costa molto meno.

**Come funziona l'overlap:**

Senza overlap:
```
Chunk 1: "...il dipendente ha diritto a"
Chunk 2: "20 giorni di ferie all'anno..."
```
La frase è spezzata! Il chunk 1 non ha senso da solo.

Con overlap di 50 caratteri:
```
Chunk 1: "...il dipendente ha diritto a 20 giorni di ferie..."
Chunk 2: "...20 giorni di ferie all'anno. Le ferie devono..."
```
Ogni chunk è comprensibile da solo.

---

### Che Cos'è il Retrieval?

**Definizione semplice:**
Retrieval significa "recupero". È il processo di cercare e trovare le informazioni rilevanti per rispondere a una domanda.

**Il processo completo:**

1. **Embedding della domanda:**
   ```
   "Quanti giorni di ferie?" → [0.234, -0.567, ...]
   ```

2. **Ricerca semantica:**
   FAISS trova i chunk i cui embeddings sono più vicini all'embedding della domanda.

3. **Ranking:**
   I risultati sono ordinati per distanza (più vicino = più rilevante).

4. **Recupero dei testi:**
   Dagli indici FAISS, recuperiamo i testi originali dei chunk.

**Differenza con ricerca per parole chiave:**

Ricerca keyword:
- Cerca "ferie"
- Trova solo i chunk che contengono esattamente la parola "ferie"
- Non trova "vacanze" o "giorni di permesso"

Ricerca semantica (retrieval):
- Capisce che "ferie", "vacanze", "permessi" hanno significato simile
- Trova tutti i chunk rilevanti anche se non contengono la parola esatta

---

### Che Cos'è il RAG?

**Definizione semplice:**
RAG = Retrieval-Augmented Generation (Generazione Aumentata da Recupero).

**Scomposizione:**
1. **Retrieval:** Recupera informazioni rilevanti da una base di conoscenza
2. **Augmented:** Aumenta/arricchisce il prompt dell'AI con queste informazioni
3. **Generation:** Genera la risposta usando l'AI

**Perché RAG è potente:**

**Senza RAG (LLM da solo):**
- Gemini ha conoscenza generale fino a una certa data
- Non conosce i tuoi documenti aziendali
- Potrebbe inventare informazioni (allucinazioni)

**Con RAG:**
- Recuperi i pezzi rilevanti dai tuoi documenti
- Li includi nel prompt
- Gemini genera una risposta basata SOLO su quei documenti
- Risposta accurata e verificabile

**Formula del RAG:**
```
Domanda → Retrieval → Contesto Rilevante → LLM(Domanda + Contesto) → Risposta
```

**Esempio pratico:**

**Senza RAG:**
```
Utente: "Quanti giorni di ferie ho nella mia azienda?"
Gemini: "Generalmente le aziende offrono 15-25 giorni di ferie..."
```
(Risposta generica, non specifica per la tua azienda)

**Con RAG:**
```
Utente: "Quanti giorni di ferie ho nella mia azienda?"

Sistema:
1. Cerca "ferie" nei documenti aziendali
2. Trova: "I dipendenti hanno diritto a 20 giorni di ferie"
3. Invia a Gemini: "Context: [chunk trovato] Question: Quanti giorni..."

Gemini: "Secondo la policy aziendale, hai diritto a 20 giorni di ferie all'anno."
```
(Risposta precisa basata sui tuoi documenti!)

---

### Perché Usiamo Gemini Due Volte?

**Prima volta: Per gli Embeddings**
- Modello: `gemini-embedding-001`
- Scopo: Convertire testo in vettori numerici
- Quando: Durante l'indicizzazione dei documenti E quando l'utente fa una domanda

**Seconda volta: Per Generare la Risposta**
- Modello: `gemini-2.5-flash`
- Scopo: Leggere il contesto e generare una risposta in linguaggio naturale
- Quando: Solo quando l'utente fa una domanda

**Perché non un solo modello?**

Sono due compiti diversi:
1. **Embedding:** Compito matematico, produce vettori di numeri
2. **Generazione:** Compito linguistico, produce testo fluido

È come usare due strumenti diversi:
- Un righello per misurare (embeddings)
- Una penna per scrivere (generazione)

**Flusso completo:**

**Fase 1: Indicizzazione**
```
Documento → Chunk → Gemini Embedding → Vettori → FAISS
```

**Fase 2: Domanda**
```
Domanda → Gemini Embedding → Vettore
         ↓
      FAISS cerca → Recupera chunk
         ↓
      Chunk + Domanda → Gemini Generation → Risposta
```

---

## 7. Riassunto Finale

### Il Progetto in 60 Secondi

**Cosa fa:**
Un sistema che ti permette di fare domande ai tuoi documenti PDF/DOCX e ricevere risposte precise con fonti.

**Come funziona:**

**Preparazione (una volta):**
1. Carichi documenti
2. Sistema estrae il testo
3. Divide in chunk (pezzi piccoli)
4. Converte ogni chunk in embedding (vettore di numeri)
5. Salva in FAISS (database vettoriale)

**Uso (ogni domanda):**
1. Fai una domanda
2. Sistema converte la domanda in embedding
3. FAISS trova i 3 chunk più simili
4. Sistema costruisce un prompt con chunk + domanda
5. Gemini legge e genera la risposta
6. Vedi la risposta + le fonti originali

---

### Tecnologie Chiave

**Streamlit:** Framework per creare l'interfaccia web senza HTML/CSS/JavaScript.

**Gemini API:** Intelligenza artificiale di Google per:
- Creare embeddings (vettori semantici)
- Generare risposte in linguaggio naturale

**FAISS:** Database vettoriale ultra-veloce per cercare tra milioni di embeddings.

**PyPDF e python-docx:** Librerie per estrarre testo da PDF e DOCX.

**NumPy:** Libreria per operazioni matematiche su array (usata con FAISS).

---

### Concetti Fondamentali

**Embeddings:** Rappresentazione numerica del significato del testo. Testi simili hanno embeddings simili.

**Chunking:** Dividere testo lungo in pezzi piccoli con overlap per non perdere contesto.

**Vector Database (FAISS):** Database specializzato per cercare velocemente vettori simili.

**RAG (Retrieval-Augmented Generation):** Tecnica che combina ricerca (retrieval) e generazione AI. Recupera informazioni rilevanti e le usa per generare risposte accurate.

**Semantic Search:** Ricerca basata sul significato, non solo sulle parole esatte.

---

### Punti Importanti da Ricordare

1. **Perché l'overlap nei chunk?**
   Per non spezzare le frasi a metà. Garantisce che ogni chunk abbia senso completo.

2. **Perché convertiamo in embeddings?**
   I computer non capiscono il linguaggio. Gli embeddings sono rappresentazioni numeriche del significato che permettono confronti matematici.

3. **Come FAISS sa quali chunk sono rilevanti?**
   Calcola la distanza L2 tra l'embedding della domanda e tutti gli embeddings dei chunk. Distanza piccola = significato simile.

4. **Perché non inviamo tutti i documenti a Gemini?**
   - Limiti di token
   - Costi elevati
   - Minor precisione
   Il retrieval trova solo i pezzi rilevanti.

5. **Perché specifichiamo "Use only the context" nel prompt?**
   Per evitare che Gemini inventi informazioni o usi la sua conoscenza generale. Vogliamo risposte basate SOLO sui nostri documenti.

6. **Cosa succede se la risposta non è nei documenti?**
   Gemini dovrebbe dire "L'informazione non è stata trovata nei documenti caricati" grazie alle istruzioni nel prompt.

7. **I metadati cosa sono e perché servono?**
   Informazioni extra sui chunk (nome file, ID, testo originale). Servono per mostrare le fonti all'utente.

---

### Flusso Completo Passo-Passo (Da Ricordare)

**Indicizzazione:**
```
1. Upload file → 2. Salva su disco → 3. Estrai testo → 
4. Dividi in chunk → 5. Genera embeddings → 6. Salva in FAISS
```

**Risposta:**
```
1. Domanda utente → 2. Genera embedding domanda → 
3. Cerca in FAISS → 4. Recupera top-3 chunk → 
5. Costruisci prompt (chunk + domanda) → 6. Invia a Gemini → 
7. Ricevi risposta → 8. Mostra risposta + fonti
```

---

### Architettura Modulare (Schema Mentale)

```
app.py (Interfaccia)
   ↓
config.py (Configurazioni)
   ↓
modules/
   ├── document_loader.py (Estrazione testo)
   ├── text_splitter.py (Chunking)
   ├── embeddings.py (Gemini embeddings)
   ├── vector_store.py (FAISS)
   └── chat_engine.py (Orchestrazione RAG)
```

Ogni modulo ha una responsabilità specifica. Se vuoi modificare come vengono estratti i PDF, modifichi solo `document_loader.py`.

---

### Quando Usare Questo Progetto (Casi d'Uso)

- Query su manuali tecnici
- Ricerca in policy aziendali
- Q&A su documenti legali
- Analisi di report finanziari
- Knowledge base aziendale
- Assistente per documentazione prodotto

---

### Domande per Verificare la Comprensione

Prima di un colloquio, assicurati di saper rispondere:

1. **Che cos'è il RAG e come funziona?**
2. **Perché usiamo embeddings invece di ricerca per parole chiave?**
3. **Che ruolo ha FAISS nel progetto?**
4. **Perché dividiamo il testo in chunk?**
5. **Cosa succede quando l'utente fa una domanda? (flusso completo)**
6. **Perché usiamo Gemini due volte e per cosa?**
7. **Come comunica FAISS quale chunk è più rilevante?**
8. **Come garantiamo che Gemini non inventi informazioni?**

---

### Miglioramenti Possibili (Per Discutere)

- **Supporto più formati:** TXT, Markdown, HTML
- **Chunking semantico:** Dividere per paragrafi/sezioni invece che per caratteri
- **Hybrid search:** Combinare embeddings + keyword search
- **Cache degli embeddings:** Non ricalcolare embeddings già fatti
- **Indicizzazione incrementale:** Aggiungere documenti senza rifare tutto
- **Multilingua:** Supporto documenti in più lingue
- **User auth:** Sistema di login e permessi

---

### Conclusione

Hai costruito un sistema RAG completo che dimostra:
- Integrazione con API AI moderne (Gemini)
- Uso di database vettoriali (FAISS)
- Comprensione dell'NLP (embeddings, semantic search)
- Architettura modulare e pulita
- Interfaccia utente funzionale (Streamlit)

Questo progetto mostra competenze pratiche in:
- Python moderno
- AI/ML applications
- Information Retrieval
- Software architecture
- API integration

**Sei pronto per spiegare il tuo progetto con sicurezza!** 🚀
