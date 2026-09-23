import requests
from app.core.config import settings

def generate_answer(query: str, retrieved_chunks: list):
    if not retrieved_chunks:
        return "I don't have access to information to answer this question. Teacher-only information must not be disclosed if you are a student, or the query may be out of scope.", []
    
    context_parts = []
    sources = set()
    
    for chunk in retrieved_chunks:
        doc_id = chunk['metadata'].get('document_id', 'Unknown')
        title = chunk['metadata'].get('title', 'Unknown Title')
        context_parts.append(f"Document [{doc_id} - {title}]:\n{chunk['content']}")
        sources.add(doc_id)
        
    context_str = "\n\n---\n\n".join(context_parts)
    
    prompt = f"""You are a school knowledge assistant.

    Answer the QUESTION using ONLY the CONTEXT.

    RULES:
    - If the answer is in the CONTEXT, answer it directly.
    - If the answer is NOT in the CONTEXT, say exactly:
    "I don't have the information in the provided school knowledge base."
    - Never use outside knowledge.
    - Never guess or invent information.
    - Use the exact facts, numbers, equations, and steps from the CONTEXT.
    - For calculations or procedures, give the steps shown in the CONTEXT.
    - Cite the Document ID that supports your answer.

    CONTEXT:
    {context_str}

    QUESTION:
    {query}

    ANSWER:
    """

    try:
        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.1}
            },
            timeout=120
        )
        response.raise_for_status()
        result = response.json().get("response", "")
        return result, list(sources)
    except Exception as e:
        return f"Error communicating with Ollama: {str(e)}", []
