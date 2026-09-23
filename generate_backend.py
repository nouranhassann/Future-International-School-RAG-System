import os

backend_files = {
    "backend/requirements.txt": """fastapi
uvicorn
pydantic
pydantic-settings
python-jose[cryptography]
passlib[bcrypt]
python-multipart
chromadb
sentence-transformers
requests
pytest
""",
    "backend/.env.example": """OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
JWT_SECRET_KEY=super_secret_key_for_demo_purposes_only
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
VECTOR_STORE_PATH=../data/vector_store
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
""",
    "backend/app/__init__.py": "",
    "backend/app/core/__init__.py": "",
    "backend/app/core/config.py": """import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "School Knowledge RAG Assistant"
    API_V1_STR: str = "/api/v1"
    
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")
    
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "fallback_secret")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    VECTOR_STORE_PATH: str = os.getenv("VECTOR_STORE_PATH", "../data/vector_store")
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")

    class Config:
        env_file = ".env"

settings = Settings()
""",
    "backend/app/core/security.py": """from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: Union[str, Any], role: str, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject), "role": role}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt
""",
    "backend/app/schemas/__init__.py": "",
    "backend/app/schemas/auth.py": """from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None

class LoginRequest(BaseModel):
    email: str
    password: str
""",
    "backend/app/schemas/query.py": """from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]
""",
    "backend/app/services/__init__.py": "",
    "backend/app/services/auth_service.py": """# Demo users database
from app.core.security import get_password_hash

# For demonstration, passwords are 'password123'
DEMO_USERS = {
    "student@example.com": {
        "id": "1",
        "email": "student@example.com",
        "password_hash": get_password_hash("password123"),
        "role": "student"
    },
    "teacher@example.com": {
        "id": "2",
        "email": "teacher@example.com",
        "password_hash": get_password_hash("password123"),
        "role": "teacher"
    }
}

def get_user(email: str):
    return DEMO_USERS.get(email)
""",
    "backend/app/services/authorization.py": """def get_allowed_access_levels(user_role: str) -> list[str]:
    \"\"\"Determine which document access levels a role can retrieve.\"\"\"
    if user_role == 'student':
        return ['shared', 'student']
    elif user_role == 'teacher':
        return ['shared', 'student', 'teacher']
    return []

def is_access_allowed(user_role: str, document_access_level: str) -> bool:
    return document_access_level in get_allowed_access_levels(user_role)
""",
    "backend/app/api/__init__.py": "",
    "backend/app/api/routes/__init__.py": "",
    "backend/app/core/dependencies.py": """from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings
from app.schemas.auth import TokenData
from app.services.auth_service import get_user

# Using a standard bearer token, but you can also use OAuth2PasswordBearer directly
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role is None:
            raise credentials_exception
        token_data = TokenData(email=email, role=role)
    except JWTError:
        raise credentials_exception
    
    user = get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
""",
    "backend/app/api/routes/auth.py": """from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import LoginRequest, Token
from app.services.auth_service import get_user
from app.core.security import verify_password, create_access_token

router = APIRouter()

@router.post("/login", response_model=Token)
def login(request: LoginRequest):
    user = get_user(request.email)
    if not user or not verify_password(request.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user["email"], role=user["role"])
    return {"access_token": access_token, "token_type": "bearer", "role": user["role"]}
""",
    "backend/app/services/retrieval.py": """import chromadb
from chromadb.config import Settings
from app.core.config import settings
from sentence_transformers import SentenceTransformer
from app.services.authorization import get_allowed_access_levels

# Global variables for models (loaded in lifespan)
_chroma_client = None
_collection = None
_embedding_model = None

def load_models():
    global _chroma_client, _collection, _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
    if _chroma_client is None:
        try:
            _chroma_client = chromadb.PersistentClient(path=settings.VECTOR_STORE_PATH)
            _collection = _chroma_client.get_collection("school_knowledge")
        except Exception as e:
            print(f"Warning: ChromaDB collection not found or error loading: {e}")
            _collection = None

def retrieve_chunks(query: str, user_role: str, top_k: int = 3):
    if _collection is None:
        return []
        
    allowed_levels = get_allowed_access_levels(user_role)
    if not allowed_levels:
        return []

    # Security check BEFORE retrieval
    if len(allowed_levels) == 1:
        where_filter = {"access_level": allowed_levels[0]}
    else:
        where_filter = {"$or": [{"access_level": level} for level in allowed_levels]}

    query_embedding = _embedding_model.encode([query]).tolist()
    
    results = _collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        where=where_filter
    )
    
    retrieved = []
    if results and results.get('ids') and results['ids'][0]:
        for i in range(len(results['ids'][0])):
            retrieved.append({
                'id': results['ids'][0][i],
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
            })
    return retrieved
""",
    "backend/app/services/generation.py": """import requests
from app.core.config import settings

def generate_answer(query: str, retrieved_chunks: list):
    if not retrieved_chunks:
        return "I don't have access to information to answer this question. Teacher-only information must not be disclosed if you are a student, or the query may be out of scope.", []
    
    context_parts = []
    sources = set()
    
    for chunk in retrieved_chunks:
        doc_id = chunk['metadata'].get('document_id', 'Unknown')
        title = chunk['metadata'].get('title', 'Unknown Title')
        context_parts.append(f"Document [{doc_id} - {title}]:\\n{chunk['content']}")
        sources.add(doc_id)
        
    context_str = "\\n\\n---\\n\\n".join(context_parts)
    
    prompt = f\"\"\"You are a helpful school assistant for Future Scholars International School.
Answer the user's question based strictly on the context provided below.
If the context does not contain the answer, explicitly state that you do not have the information.
Do not use outside knowledge. Cite the Document IDs from the context in your answer.

Context:
{context_str}

Question: {query}
Answer:\"\"\"

    try:
        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.1}
            },
            timeout=30
        )
        response.raise_for_status()
        result = response.json().get("response", "")
        return result, list(sources)
    except Exception as e:
        return f"Error communicating with Ollama: {str(e)}", []
""",
    "backend/app/api/routes/query.py": """from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.query import QueryRequest, QueryResponse
from app.core.dependencies import get_current_user
from app.services.retrieval import retrieve_chunks
from app.services.generation import generate_answer

router = APIRouter()

@router.post("/", response_model=QueryResponse)
def handle_query(request: QueryRequest, current_user: dict = Depends(get_current_user)):
    user_role = current_user.get("role")
    
    # 1. Authorization & Retrieval
    chunks = retrieve_chunks(request.question, user_role)
    
    # 2. Generation
    answer, sources = generate_answer(request.question, chunks)
    
    return QueryResponse(answer=answer, sources=sources)
""",
    "backend/app/main.py": """from contextlib import asynccontextmanager
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
"""
}

def generate_backend():
    base_dir = "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant"
    for file_path, content in backend_files.items():
        full_path = os.path.join(base_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
    print("Backend generated successfully.")

if __name__ == "__main__":
    generate_backend()
