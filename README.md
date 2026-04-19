# 🎮 Agentic Player Retention Optimizer

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Stateful_Agents-orange)](https://python.langchain.com/v0.1/docs/langgraph/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-FF4B4B)](https://game-churn-predictor.streamlit.app/)

## From Predictive Analytics to Autonomous Agentic Intervention

### 📖 Project Overview
This project bridges the gap between predictive machine learning and actionable game design. Originally built as a Random Forest churn predictor, the system has evolved into an **Agentic AI Assistant**. 

Instead of merely flagging players who are likely to quit, the system utilizes an autonomous LangGraph workflow to reason about the underlying causes of churn, query a specialized vector database of game design strategies (RAG), and generate a deterministic, highly structured retention plan using Llama 3.3.

---

### 🧠 System Architecture

The core logic operates on a state-based **LangGraph** architecture, cleanly separating predictive ML from generative AI:

1. **Prediction Node:** Parses tabular player telemetry through a pre-trained `Scikit-Learn` Random Forest pipeline to generate a churn probability.
2. **Analysis Node:** Evaluates the risk factors mathematically (e.g., high difficulty + short sessions = progression friction).
3. **Retrieval Node (RAG):** Uses `ChromaDB` and `HuggingFaceEmbeddings` (`all-MiniLM-L6-v2`) to perform semantic search against a custom `retention_playbook.md`, retrieving targeted game economy and engagement mechanics.
4. **Generation Node:** A `Llama-3.3-70b-versatile` LLM (via Groq) synthesizes the data. It is constrained by **Pydantic** schema validation to guarantee a strict 5-part JSON output, eliminating hallucinations and formatting errors.

---

### 🛠️ Technology Stack

| Component | Technology |
| :--- | :--- |
| **Agent Framework** | LangGraph, LangChain, Pydantic |
| **Large Language Model** | Llama 3.3 70B (via Groq API) |
| **RAG & Vector DB** | ChromaDB, HuggingFace (`all-MiniLM-L6-v2`) |
| **Predictive ML** | Scikit-Learn (Random Forest: 93.9% Acc), Pandas |
| **Frontend UI** | Streamlit |

---

### 🌟 Key Features
* **Modular Codebase:** Clean separation of concerns (`core/agents`, `core/rag`, `core/models`) designed for scalability and isolated testing.
* **Intelligent Chunking:** Uses `MarkdownHeaderTextSplitter` to ensure retrieved strategies maintain their target profile context.
* **Deterministic Structured Output:** Forces the LLM to output specific fields (Summary, Analysis, Plan, References, Disclaimer) for direct UI integration.
* **Graceful Degradation:** Built-in fallback logic ensures the Streamlit UI safely serves a standard retention strategy even if the LLM API times out.

---

### 📂 Directory Structure

```text
game-churn-predictor/
├── core/                       # Main application package
│   ├── agents/                 # LangGraph Agent logic
│   │   ├── __init__.py
│   │   ├── nodes.py            # Individual node functions
│   │   ├── prompts.py          # AI system prompts
│   │   └── workflow.py         # Graph definition & compilation
│   ├── models/                 # ML Prediction logic
│   │   ├── __init__.py
│   │   └── predictor.py        # Random Forest inference
│   ├── rag/                    # Retrieval-Augmented Generation
│   │   ├── __init__.py
│   │   ├── embedding.py        # HuggingFace model factory
│   │   ├── loader.py           # Playbook document loader
│   │   └── retriever.py        # ChromaDB search interface
│   ├── utils/                  
│   │   └── logger.py           # Centralized logging setup
│   └── config.py               # Environment configuration
├── app.py                      # Streamlit UI (Entry Point)
├── churn_model.pkl             # Serialized Random Forest model
├── retention_playbook.md       # Knowledge base for RAG
├── player_data.csv             # Raw telemetry dataset
└── requirements.txt            # Project dependencies

---

### How to Run Locally
1. Clone the repo: `git clone https://github.com/jigyasu-kalyan/game-churn-predictor.git`
2. Set up a virtual environment:
`
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
`
3. Configure environment variable: `GROQ_API_KEY="gsk_your_api_key_here"`
4. Run the app: `streamlit run app.py`

### 🌐 Live Deployment
**Hosted Link:** https://game-churn-predictor.streamlit.app/