# School Knowledge RAG Assistant Implementation Plan

Provide a complete production-style RAG web application for a fictional school, "Future Scholars International School" (2026-2027), using local LLMs (Ollama) and Role-Based Access Control before retrieval.

## User Review Required

> [!IMPORTANT]  
> Please review the plan below. I will proceed with executing all phases automatically once you approve. Be aware that the final verification phase will require starting background tasks (like FastAPI and Streamlit) to test the UI and API locally. 

## Open Questions

> [!NOTE]
> Do you have any specific preferences for the SentenceTransformers model to use (e.g., `all-MiniLM-L6-v2`) or a specific Ollama model (e.g., `llama3` or `phi3`)? If not, I will use `all-MiniLM-L6-v2` for embeddings and `phi3` or `llama3` for Ollama as they are lightweight and performant.

## Proposed Changes

We will build the system iteratively through the following phases:

### Phase 1: Dataset Generation
- Create a script `generate_dataset.py` that generates 25-35 synthetic Markdown documents (Shared, Student, Teacher) inside `data/raw/`.
- Each document will contain the required metadata (ID, Title, Category, Subject, Audience, Access Level, Description).
- Generate `data/dataset_manifest.csv` and `data/dataset_manifest.md`.

### Phase 2: Evaluation Data
- Generate JSON files in `data/evaluation/`:
  - `evaluation_questions.json` (10 student, 10 teacher questions, 5 multi-doc, 5 out-of-scope)
  - `security_tests.json` (10 security/access-control questions)

### Phase 3: Project Structure
- Create the overarching folder structure (`notebooks`, `data`, `backend`, `frontend`, etc.).

### Phase 4: Notebook (RAG Pipeline)
- Create `notebooks/rag_pipeline.ipynb` that will run end-to-end.
- Load, clean, and chunk the synthetic dataset.
- Extract and preserve metadata for every chunk.
- Embed using SentenceTransformers and populate a persistent Chroma vector database in `data/vector_store/`.
- Implement testing of retrieval and generation within the notebook.

### Phase 5-7: FastAPI Backend, Authentication & Security
- Implement JWT-based auth in `backend/app/api/routes/auth.py`.
- Implement security model in `backend/app/services/authorization.py` ensuring authorization happens *before* retrieval.
- Implement ChromaDB search with metadata filtering in `backend/app/services/retrieval.py`.
- Integrate Ollama for grounded response generation in `backend/app/services/generation.py`.
- Define FastAPI routes and application lifespan to load DB and models once.

### Phase 8: Streamlit Frontend
- Implement `frontend/app.py` and `frontend/api_client.py`.
- Build the UI with Login, Role display, Chat interface, and Citations rendering.

### Phase 9: Testing
- Write Pytest suite in `backend/tests/` covering Auth, Query execution, and Authorization.

### Phase 10-13: Project Config & Documentation
- Write `.env.example` files for backend and frontend.
- Create comprehensive `README.md`.
- Create `.gitignore`, `Dockerfile`, and `docker-compose.yml`.

## Verification Plan

### Automated Tests
- Run `pytest backend/tests/` to verify backend routes, security policies, and retrieval filtering logic.

### Manual Verification
- Execute `generate_dataset.py` to build the data.
- Run `notebooks/rag_pipeline.ipynb` to construct the ChromaDB index.
- Start FastAPI with `uvicorn` and verify `/health` and `/query`.
- Start Streamlit with `streamlit run frontend/app.py` and execute manual user testing for Student and Teacher roles, verifying secure access controls.
