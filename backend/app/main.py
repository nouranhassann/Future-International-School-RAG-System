from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import auth, query
from app.services.retrieval import load_models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load Models and ChromaDB once at startup
    print("Loading models and vector store...")
    load_models()
    print("Models loaded successfully.")
    yield
    print("Shutting down...")

app = FastAPI(title="School Knowledge RAG Assistant", lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(query.router, prefix="/query", tags=["query"])
