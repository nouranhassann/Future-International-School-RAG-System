import nbformat as nbf

nb = nbf.v4.new_notebook()

cells = []

# 1. Project Overview
cells.append(nbf.v4.new_markdown_cell("""# School Knowledge RAG Assistant - Pipeline

This notebook implements the data processing, vector indexing, retrieval, and generation steps of our Role-Based AI School Knowledge System.

## Project Overview
This project builds a RAG system for 'Future Scholars International School' (2026-2027) with role-based access control. The system ensures that users only retrieve documents they are authorized to see."""))

# 2. Imports and Setup
cells.append(nbf.v4.new_code_cell("""import os
import json
import glob
import pandas as pd
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import requests
import uuid

# Configuration
DATA_DIR = "../data/raw"
VECTOR_STORE_DIR = "../data/vector_store"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3" # Replace with your local model
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120

os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
"""))

# 3. Load & Inspect
cells.append(nbf.v4.new_markdown_cell("""## Load & Inspect Documents
We will load the synthetic markdown documents, extract metadata from the frontmatter, and inspect the dataset."""))

cells.append(nbf.v4.new_code_cell("""def parse_markdown(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split('---')
    if len(parts) >= 3:
        frontmatter = parts[1].strip()
        body = '---'.join(parts[2:]).strip()
        
        metadata = {}
        for line in frontmatter.split('\\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                metadata[key.strip()] = val.strip()
        
        return metadata, body
    return {}, content

documents = []
for root, _, files in os.walk(DATA_DIR):
    for file in files:
        if file.endswith('.md'):
            filepath = os.path.join(root, file)
            metadata, body = parse_markdown(filepath)
            if metadata:
                metadata['source_file'] = filepath
                documents.append({'metadata': metadata, 'content': body})

print(f"Loaded {len(documents)} documents.")
df = pd.DataFrame([doc['metadata'] for doc in documents])
display(df.head())
print("\\nAccess Level Distribution:")
print(df['Access Level'].value_counts())
"""))

# 4. Cleaning
cells.append(nbf.v4.new_markdown_cell("""## Cleaning
The documents are synthetic markdown, so they are relatively clean. We will strip excessive newlines."""))

cells.append(nbf.v4.new_code_cell("""def clean_text(text):
    import re
    # Remove excessive newlines
    text = re.sub(r'\\n{3,}', '\\n\\n', text)
    return text.strip()

for doc in documents:
    doc['content'] = clean_text(doc['content'])
"""))

# 5. Chunking Strategy
cells.append(nbf.v4.new_markdown_cell("""## Chunking Strategy
We use a simple character-based chunking strategy with overlap.
- **Chunk Size**: 800 characters (approx. 150-200 words, suitable for capturing policy details without diluting context).
- **Chunk Overlap**: 120 characters (ensures continuity between chunks).
Metadata is preserved for every chunk."""))

cells.append(nbf.v4.new_code_cell("""def chunk_text(text, chunk_size, chunk_overlap):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start += (chunk_size - chunk_overlap)
    return chunks

chunked_documents = []
for doc in documents:
    chunks = chunk_text(doc['content'], CHUNK_SIZE, CHUNK_OVERLAP)
    for i, chunk_content in enumerate(chunks):
        chunk_metadata = doc['metadata'].copy()
        chunk_metadata['chunk_id'] = f"{chunk_metadata.get('Document ID', 'DOC')}-CHUNK-{i}"
        chunk_metadata['document_id'] = chunk_metadata.pop('Document ID', 'UNKNOWN')
        chunk_metadata['title'] = chunk_metadata.pop('Title', 'UNKNOWN')
        chunk_metadata['category'] = chunk_metadata.pop('Category', 'UNKNOWN')
        chunk_metadata['subject'] = chunk_metadata.pop('Subject', 'UNKNOWN')
        chunk_metadata['audience'] = chunk_metadata.pop('Audience', 'UNKNOWN')
        chunk_metadata['access_level'] = chunk_metadata.pop('Access Level', 'UNKNOWN')
        
        chunked_documents.append({
            'chunk_id': chunk_metadata['chunk_id'],
            'metadata': chunk_metadata,
            'content': chunk_content
        })

print(f"Total chunks created: {len(chunked_documents)}")
"""))

# 6. Embeddings and ChromaDB
cells.append(nbf.v4.new_markdown_cell("""## Embeddings & ChromaDB Vector Store
We will generate embeddings using `all-MiniLM-L6-v2` and store them in a persistent ChromaDB instance.
We configure ChromaDB to store data locally so the FastAPI backend can load it later without rebuilding."""))

cells.append(nbf.v4.new_code_cell("""embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

client = chromadb.PersistentClient(path=VECTOR_STORE_DIR)
# Delete existing collection if it exists for a fresh run
try:
    client.delete_collection("school_knowledge")
except:
    pass

collection = client.create_collection("school_knowledge")

# Batch processing to add to ChromaDB
batch_size = 100
for i in range(0, len(chunked_documents), batch_size):
    batch = chunked_documents[i:i+batch_size]
    
    ids = [chunk['chunk_id'] for chunk in batch]
    documents_content = [chunk['content'] for chunk in batch]
    metadatas = [chunk['metadata'] for chunk in batch]
    
    # Generate embeddings
    embeddings = embedding_model.encode(documents_content).tolist()
    
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents_content,
        metadatas=metadatas
    )

print(f"Added {collection.count()} chunks to the vector store.")
"""))

# 7. Retrieval with Authorization
cells.append(nbf.v4.new_markdown_cell("""## Filtered Retrieval
Retrieval MUST support metadata filtering based on the user's role.
- **Student**: can access `shared`, `student`.
- **Teacher**: can access `shared`, `student`, `teacher`.
We enforce this BEFORE the vector search happens by passing a `where` filter to ChromaDB."""))

cells.append(nbf.v4.new_code_cell("""def get_allowed_access_levels(user_role):
    if user_role == 'student':
        return ['shared', 'student']
    elif user_role == 'teacher':
        return ['shared', 'student', 'teacher']
    return []

def retrieve_chunks(query, user_role, top_k=3):
    allowed_levels = get_allowed_access_levels(user_role)
    
    if not allowed_levels:
        return []

    # Prepare where filter for ChromaDB
    if len(allowed_levels) == 1:
        where_filter = {"access_level": allowed_levels[0]}
    else:
        where_filter = {"$or": [{"access_level": level} for level in allowed_levels]}

    query_embedding = embedding_model.encode([query]).tolist()
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        where=where_filter
    )
    
    retrieved = []
    for i in range(len(results['ids'][0])):
        retrieved.append({
            'id': results['ids'][0][i],
            'content': results['documents'][0][i],
            'metadata': results['metadatas'][0][i],
            'distance': results['distances'][0][i]
        })
    return retrieved

# Test Retrieval
print("Test: Student retrieving math guide")
res = retrieve_chunks("What are linear equations?", "student")
for r in res:
    print(f" - {r['id']} (Access: {r['metadata']['access_level']})")

print("\\nTest: Student retrieving teacher grading policy (Should return empty or irrelevant, but NOT teacher docs)")
res = retrieve_chunks("What percentage of the grade is formative?", "student")
for r in res:
    print(f" - {r['id']} (Access: {r['metadata']['access_level']})")
"""))

# 8. Prompt Construction and Ollama Generation
cells.append(nbf.v4.new_markdown_cell("""## Prompt Construction & Generation (Ollama)
We construct a grounded prompt. The LLM is instructed to use ONLY the retrieved context and explicitly refuse if the context is insufficient."""))

cells.append(nbf.v4.new_code_cell("""def generate_answer(query, retrieved_chunks):
    if not retrieved_chunks:
        return "I don't have access to information to answer this question.", []
    
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
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.1}
            }
        )
        response.raise_for_status()
        result = response.json().get("response", "")
        return result, list(sources)
    except Exception as e:
        return f"Error communicating with Ollama: {str(e)}", []
"""))

# 9. Test Retrieval and Evaluation
cells.append(nbf.v4.new_markdown_cell("""## Test Retrieval & Security Evaluation
Let's run through sample questions from different roles."""))

cells.append(nbf.v4.new_code_cell("""test_cases = [
    {"role": "student", "q": "What topics are included in Grade 10 Mathematics?"},
    {"role": "student", "q": "What percentage should formative assessment contribute to the final grade?"}, # Security test
    {"role": "teacher", "q": "What percentage should formative assessment contribute to the final grade?"},
    {"role": "student", "q": "What is the capital of France?"}, # Out of scope
    {"role": "student", "q": "When is the winter break?"} # Shared
]

results = []
for case in test_cases:
    print(f"\\n--- Query: {case['q']} (Role: {case['role']}) ---")
    chunks = retrieve_chunks(case['q'], case['role'])
    
    authorized = True
    for c in chunks:
        if case['role'] == 'student' and c['metadata']['access_level'] == 'teacher':
            authorized = False
            
    answer, sources = generate_answer(case['q'], chunks)
    print(f"Answer: {answer}")
    print(f"Sources: {sources}")
    print(f"Authorized Retrieval: {authorized}")
"""))

# 10. Failure Analysis
cells.append(nbf.v4.new_markdown_cell("""## Failure Analysis & Mitigation
- **Retrieval Failures**: Addressed by ensuring chunking retains enough context (800 chars) and overlapping chunks.
- **Hallucination Risks**: The prompt strongly enforces `Do not use outside knowledge` and temperature is set to 0.1.
- **Authorization Failures**: Mitigated by strictly applying the `where` filter at the database level *before* retrieving context, making it physically impossible for unauthorized data to reach the LLM.
"""))

# 11. Configuration Export
cells.append(nbf.v4.new_code_cell("""# Export configuration for backend
config = {
    "CHUNK_SIZE": CHUNK_SIZE,
    "CHUNK_OVERLAP": CHUNK_OVERLAP,
    "EMBEDDING_MODEL_NAME": EMBEDDING_MODEL_NAME,
    "VECTOR_STORE_DIR": "data/vector_store",
    "COLLECTION_NAME": "school_knowledge"
}

with open("../data/vector_store/config.json", "w") as f:
    json.dump(config, f, indent=4)
print("Configuration saved.")
"""))

nb['cells'] = cells
with open('c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/notebooks/rag_pipeline.ipynb', 'w') as f:
    nbf.write(nb, f)
print("Notebook generated successfully")
