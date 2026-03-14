# ⚖️ Legal Assistant

> An AI-powered legal research and practice management platform built for Indian legal professionals — combining **Retrieval-Augmented Generation (RAG)** with a locally-hosted LLM for grounded, traceable legal analysis.

---

## 📌 Table of Contents

- [Why Legal Assistant?](#-why-legal-assistant)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [LM Studio Setup](#lm-studio-setup)
- [Environment Variables](#-environment-variables)
- [API Reference](#-api-reference)
- [How the RAG Pipeline Works](#-how-the-rag-pipeline-works)
- [Legal Knowledge Base](#-legal-knowledge-base)
- [Contributing](#-contributing)
- [License](#-license)

---

## 💡 Why Legal Assistant?

Most AI tools for legal work are either generic chatbots that hallucinate case law, or expensive SaaS platforms that send sensitive client data to the cloud. Legal Assistant is built differently:

| Problem                                                    | How Legal Assistant Solves It                                                                                                          |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| AI hallucinating laws that don't exist                     | Every answer is grounded in retrieved sections from actual Indian statutes — section numbers and similarity scores are always shown    |
| Sensitive client data sent to external servers             | Runs 100% locally. No API keys. No data ever leaves your machine                                                                       |
| Switching between multiple tools for research + management | One platform for legal research, contract review, client records, scheduling, and billing                                              |
| Generic AI that doesn't understand Indian law              | Prompts are engineered specifically for BNS 2023 and ICA 1872 — with rules like "never attribute self-defence to an attacker" baked in |
| Expensive cloud LLM costs per query                        | Uses a free, locally-running open-source model via LM Studio — zero per-query cost                                                     |
| Manually writing appointment summaries                     | One-click PDF export for any appointment — ready to print or share with clients                                                        |
| Tracking payments and issuing receipts manually            | Generate a professional payment bill/receipt the moment a client pays — exportable as PDF instantly                                    |

---

## ✨ Features

### 🤖 AI Legal Research

| Feature                       | Description                                                                                                                                                                                        |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Criminal Law Intelligence** | Query the Bharatiya Nyaya Sanhita (BNS) 2023 and related acts in plain language. The system identifies offences, punishments, and right of private defence — automatically.                        |
| **Contract Clause Analysis**  | Paste any contract clause and receive a structured legal analysis under the Indian Contract Act 1872 — void vs voidable, coercion, misrepresentation, applicable sections, and a clear conclusion. |
| **Transparent RAG Answers**   | Every AI response shows the exact retrieved legal sections with similarity scores. You always know which statute the answer came from.                                                             |
| **Smart Query Detection**     | Short keyword queries go straight to FAISS. Narrative story queries (e.g. "Ram stabbed Shyam and fled") are automatically expanded into legal sub-queries using 25+ regex rules before retrieval.  |
| **Fully Local LLM**           | Runs DeepSeek R1 Distill Qwen 7B via LM Studio. No internet required. No per-query costs. No data leaves your machine.                                                                             |

### 👥 Practice Management

| Feature                                  | Description                                                                                                                                                                       |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Client Management**                    | Add, view, update, and delete client records with name, phone, and email.                                                                                                         |
| **Appointment Scheduling**               | Create and manage appointments linked to specific clients, with date, time, and case description.                                                                                 |
| **📄 Appointment PDF Export**            | Generate a clean, printable PDF summary of any appointment — useful for personal records, client handouts, or court filings. Powered entirely by jsPDF on the frontend.           |
| **🧾 Client Billing & Payment Receipts** | Once a payment is received, generate a professional itemised bill/receipt for the client with fee details, payment date, and client information — exported as a PDF in one click. |

---

## 🛠 Tech Stack

### Frontend

- [Next.js 14](https://nextjs.org/) (App Router) — React framework
- TypeScript — type-safe development
- [TanStack React Query](https://tanstack.com/query) — server state management and caching
- Axios — HTTP client with request/response interceptors
- React Markdown — renders LLM output with full formatting support
- **jsPDF + jsPDF-AutoTable** — client-side PDF generation for appointment summaries and payment bills

### Backend

- [FastAPI](https://fastapi.tiangolo.com/) — high-performance REST API framework
- SQLAlchemy + SQLite — relational database with ORM
- Pydantic — request/response schema validation
- [sentence-transformers](https://www.sbert.net/) (`multi-qa-MiniLM-L6-cos-v1`) — semantic text embeddings
- [FAISS](https://github.com/facebookresearch/faiss) (CPU) — vector similarity search index
- PyMuPDF + pypdf — PDF ingestion and section parsing
- Requests — communication with local LLM server

### AI / LLM

- [LM Studio](https://lmstudio.ai/) — local LLM inference server
- DeepSeek R1 Distill Qwen 7B — open-source reasoning model, runs on consumer hardware

---

## 📁 Project Structure

```
Legal-Assistant/
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── client.py           # Client CRUD endpoints
│   │   │   ├── appointment.py      # Appointment CRUD endpoints
│   │   │   ├── legal.py            # Criminal law RAG endpoint
│   │   │   └── contract.py         # Contract law RAG endpoint
│   │   ├── models/
│   │   │   ├── client.py           # Client table (id, name, phone, email)
│   │   │   └── appointment.py      # Appointment table (client_id FK, date, description)
│   │   ├── schemas/                # Pydantic request/response schemas
│   │   ├── rag/                    # Criminal law RAG pipeline
│   │   │   ├── loader.py           # PDF loader
│   │   │   ├── parser.py           # Section parser
│   │   │   ├── chunker.py          # Text chunker
│   │   │   ├── normalizer.py       # Text normalizer
│   │   │   ├── faiss_manager.py    # FAISS index builder
│   │   │   └── retriever.py        # Smart query retriever (keyword + story expansion)
│   │   ├── contractRag/            # Contract law RAG pipeline (same structure + enricher)
│   │   ├── llm/
│   │   │   ├── deepseek.py         # LLM call for legal queries
│   │   │   └── contract_call.py    # LLM call for contract analysis (with temperature config)
│   │   └── core/
│   │       └── database.py         # SQLite engine + session factory
│   ├── data/
│   │   ├── criminal/               # BNS 2023, BNSS 2023, BSA 2023 PDFs
│   │   ├── contract/               # Indian Contract Act 1872 PDF
│   │   └── faiss/                  # Pre-built FAISS index (faiss_index.bin + chunks.pkl)
│   ├── scripts/
│   │   ├── legalIngest.py          # Rebuilds criminal law FAISS index
│   │   └── contractIngest.py       # Rebuilds contract law FAISS index
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── page.tsx                     # Public landing page
    │   │   └── (workspace)/
    │   │       ├── layout.tsx               # Workspace layout with sidebar
    │   │       ├── clientDetails/           # Client list + management
    │   │       ├── appointment/             # Appointment list + PDF export
    │   │       ├── legal/                   # Legal intelligence query UI
    │   │       └── contract/                # Contract clause analysis UI
    │   ├── componenets/
    │   │   ├── AppointmentForm/             # Create appointment form
    │   │   ├── AppointmentUpdate/           # Edit appointment form
    │   │   ├── BillModal/                   # Bill generation modal + PDF receipt export
    │   │   ├── ClientForm/                  # Create/edit client form
    │   │   ├── Modal/                       # Generic modal wrapper
    │   │   └── Sidebar/                     # Navigation sidebar
    │   ├── hooks/                           # React Query custom hooks
    │   ├── api/                             # Axios API call functions
    │   ├── types/                           # TypeScript interfaces
    │   └── lib/
    │       └── axiosInstance.ts             # Axios base config + auth interceptors
    └── package.json
```

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.10+
- **Node.js** 18+
- **LM Studio** — [Download here](https://lmstudio.ai/)
- **DeepSeek R1 Distill Qwen 7B** model downloaded and loaded in LM Studio

---

### Backend Setup

```bash
# 1. Navigate to the backend directory
cd backend

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`  
Interactive API docs: `http://localhost:8000/docs`

> **Note:** The FAISS index is pre-built and committed to the repo inside `data/faiss/`. You do **not** need to run the ingestion scripts on first setup. Only re-run them if you add or update the source PDFs.

#### Rebuilding the FAISS index (optional)

```bash
# Re-ingest criminal law PDFs (BNS, BNSS, BSA)
python scripts/legalIngest.py

# Re-ingest contract law PDF (ICA 1872)
python scripts/contractIngest.py
```

---

### Frontend Setup

```bash
# 1. Navigate to the frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Create your environment file
cp env.template.txt .env.local
# Edit .env.local and set NEXT_PUBLIC_BACKEND_URL

# 4. Start the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

---

### LM Studio Setup

1. Download and install [LM Studio](https://lmstudio.ai/)
2. Search for and download the model: **`deepseek-r1-distill-qwen-7b`**
3. Go to the **Local Server** tab in LM Studio
4. Load the model and start the server on port **1234**
5. Verify it is running at `http://127.0.0.1:1234/v1/responses`

The backend connects to LM Studio automatically — no additional configuration needed.

---

## 🔧 Environment Variables

### Frontend — `.env.local`

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### Backend

No `.env` file is required. All configuration lives in source:

| File                   | Setting                                             |
| ---------------------- | --------------------------------------------------- |
| `app/llm/deepseek.py`  | LLM endpoint → `http://127.0.0.1:1234/v1/responses` |
| `app/core/database.py` | SQLite path → `sqlite:///./app.db`                  |

---

## 📡 API Reference

All endpoints are prefixed with `/api/v1`.

### Clients

| Method   | Endpoint        | Description         |
| -------- | --------------- | ------------------- |
| `GET`    | `/clients/`     | List all clients    |
| `POST`   | `/clients/`     | Create a new client |
| `GET`    | `/clients/{id}` | Get a single client |
| `PUT`    | `/clients/{id}` | Update a client     |
| `DELETE` | `/clients/{id}` | Delete a client     |

### Appointments

| Method   | Endpoint             | Description                               |
| -------- | -------------------- | ----------------------------------------- |
| `GET`    | `/appointments/`     | List all appointments with client details |
| `POST`   | `/appointments/`     | Create a new appointment                  |
| `GET`    | `/appointments/{id}` | Get a single appointment                  |
| `PUT`    | `/appointments/{id}` | Update an appointment                     |
| `DELETE` | `/appointments/{id}` | Delete an appointment                     |

> **PDF Export:** Appointment PDFs and payment bills are generated entirely on the frontend using jsPDF — no additional backend endpoint is required. Use the export button on any appointment card or the billing modal on the client detail page.

### Legal Intelligence

| Method | Endpoint       | Description                 |
| ------ | -------------- | --------------------------- |
| `POST` | `/legal/query` | Submit a criminal law query |

**Request body:**

```json
{
  "query": "Ram stabbed Shyam and he died. What offence has been committed?",
  "top_k": 5
}
```

**Response:**

```json
{
  "question": "...",
  "answer": "Legal analysis text...",
  "retrieved_sections": ["101", "103"],
  "retrieved_chunks": [
    {
      "section_number": "101",
      "title": "Culpable homicide",
      "chunk_type": "definition",
      "score": 0.87,
      "chunk_text": "..."
    }
  ]
}
```

### Contract Analysis

| Method | Endpoint            | Description               |
| ------ | ------------------- | ------------------------- |
| `POST` | `/contract/analyze` | Analyze a contract clause |

**Request body:**

```json
{
  "contract_text": "A agreed to sell his car to B under threat of violence.",
  "top_k": 5
}
```

**Response:**

```json
{
  "analysis": "Structured legal analysis...",
  "relevant_law_sections": [
    {
      "section": "15",
      "title": "Coercion",
      "chapter": "Chapter II",
      "content": "..."
    }
  ]
}
```

---

## 🧠 How the RAG Pipeline Works

```
PDF Documents (BNS 2023 / ICA 1872)
     │
     ▼
 Loader → Parser (extract sections) → Chunker (split by clause/paragraph)
     │
     ▼
 Normalizer → Enricher (attach legal concept tags)
     │
     ▼
 SentenceTransformer embeddings  (multi-qa-MiniLM-L6-cos-v1)
     │
     ▼
 FAISS index  ──────── saved as faiss_index.bin + chunks.pkl
     │
     ▼  (at query time)
 Smart Retriever
 ├── Short query  (≤ 12 words) ──► direct FAISS cosine similarity search
 └── Long query   (> 12 words) ──► 25+ regex rules extract legal sub-queries
                                    → multi-query FAISS search
                                    → merge results, keep best score per section
     │
     ▼
 Prompt builder
 (injects retrieved sections + domain-specific legal guardrails)
     │
     ▼
 DeepSeek R1 via LM Studio ──► structured legal analysis
```

The criminal law retriever uses over **25 regex rules** to map narrative language to legal sub-queries. For example:

- Detecting `stabbed / killed / died` → triggers a murder / culpable homicide sub-query
- Detecting `rape / forced / against will` → triggers Section 63/64/65 sub-queries
- Detecting `fought back / self defence / to escape` → triggers right of private defence sub-queries

This ensures the right sections are retrieved even when the input is a plain-language case description rather than a legal keyword.

---

## 📚 Legal Knowledge Base

| Domain       | Source Document                    | Replaces                     | Coverage                                              |
| ------------ | ---------------------------------- | ---------------------------- | ----------------------------------------------------- |
| Criminal Law | Bharatiya Nyaya Sanhita (BNS) 2023 | Indian Penal Code (IPC) 1860 | Offences, punishments, right of private defence       |
| Contract Law | Indian Contract Act 1872           | Indian Contract Act 1872     | Validity, void/voidable agreements, consent, coercion |

> The BNS, BNSS, and BSA replaced India's colonial-era criminal laws and came into force on **1 July 2024**. This system is built on the new acts — not the IPC.

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add: your feature description"`
4. Push to your branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please ensure the backend server starts without errors and that existing API contracts are preserved before submitting.

---
