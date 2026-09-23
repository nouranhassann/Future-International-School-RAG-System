from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.query import QueryRequest, QueryResponse
from app.core.dependencies import get_current_user
from app.services.retrieval import retrieve_chunks
from app.services.generation import generate_answer

router = APIRouter()


@router.post("/", response_model=QueryResponse)
def handle_query(
    request: QueryRequest,
    current_user: dict = Depends(get_current_user)
):
    user_role = current_user.get("role")

    # 1. Authorization & Retrieval
    chunks = retrieve_chunks(request.question, user_role, top_k=3)

    # DEBUG: show exactly what retrieval returned
    print("\n" + "=" * 60)
    print("RETRIEVAL DEBUG")
    print(f"Question: {request.question}")
    print(f"User role: {user_role}")
    print(f"Retrieved chunks: {len(chunks)}")
    print("=" * 60)

    for i, chunk in enumerate(chunks, 1):
        document_id = chunk["metadata"].get("document_id", "Unknown")
        title = chunk["metadata"].get("title", "Unknown Title")

        print(f"\nChunk {i}")
        print(f"Document ID: {document_id}")
        print(f"Title: {title}")
        print(f"Content:\n{chunk['content'][:500]}")
        print("-" * 60)

    # 2. Generation
    answer, sources = generate_answer(request.question, chunks)

    # 3. Response
    return QueryResponse(
        answer=answer,
        sources=sources
    )