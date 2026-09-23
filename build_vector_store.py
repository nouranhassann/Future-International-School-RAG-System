"""
build_vector_store.py
Standalone script to process all documents and populate the ChromaDB vector store.
Run this after generate_dataset.py to create the persistent index.
"""
import os
import re
import json
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
VECTOR_STORE_DIR = os.path.join(BASE_DIR, "data", "vector_store")

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120
COLLECTION_NAME = "school_knowledge"

os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

def parse_markdown(filepath):
    """Parse a markdown file with YAML-like frontmatter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split('---')
    if len(parts) >= 3:
        frontmatter = parts[1].strip()
        body = '---'.join(parts[2:]).strip()
        metadata = {}
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                metadata[key.strip()] = val.strip()
        return metadata, body
    return {}, content

def clean_text(text):
    """Remove excessive whitespace/newlines."""
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def chunk_text(text, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start += (chunk_size - chunk_overlap)
    return chunks

def main():
    print(f"Loading documents from {DATA_DIR}...")
    
    # 1. Load all markdown files
    documents = []
    md_files = glob.glob(os.path.join(DATA_DIR, "**", "*.md"), recursive=True)
    
    for filepath in md_files:
        metadata, body = parse_markdown(filepath)
        if metadata and body:
            metadata['source_file'] = os.path.relpath(filepath, BASE_DIR)
            body = clean_text(body)
            documents.append({'metadata': metadata, 'content': body})
    
    print(f"Loaded {len(documents)} documents.")
    
    # 2. Chunk with metadata preservation
    chunked_documents = []
    for doc in documents:
        chunks = chunk_text(doc['content'])
        raw_meta = doc['metadata']
        doc_id = raw_meta.get('Document ID', 'UNKNOWN')
        
        for i, chunk_content in enumerate(chunks):
            chunk_meta = {
                'chunk_id': f"{doc_id}-CHUNK-{i}",
                'document_id': doc_id,
                'title': raw_meta.get('Title', 'Unknown'),
                'category': raw_meta.get('Category', 'Unknown'),
                'subject': raw_meta.get('Subject', 'Unknown'),
                'audience': raw_meta.get('Audience', 'Unknown'),
                'access_level': raw_meta.get('Access Level', 'shared'),
                'source_file': raw_meta.get('source_file', ''),
            }
            chunked_documents.append({
                'chunk_id': chunk_meta['chunk_id'],
                'metadata': chunk_meta,
                'content': chunk_content
            })
    
    print(f"Created {len(chunked_documents)} chunks.")
    
    # 3. Embed and store in ChromaDB
    print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}...")
    from sentence_transformers import SentenceTransformer
    import chromadb
    
    embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    
    client = chromadb.PersistentClient(path=VECTOR_STORE_DIR)
    
    # Drop existing collection for fresh build
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"Deleted existing collection '{COLLECTION_NAME}'.")
    except Exception:
        pass
    
    collection = client.create_collection(COLLECTION_NAME)
    
    # Batch add
    batch_size = 50
    total = 0
    for i in range(0, len(chunked_documents), batch_size):
        batch = chunked_documents[i:i+batch_size]
        ids = [c['chunk_id'] for c in batch]
        texts = [c['content'] for c in batch]
        metas = [c['metadata'] for c in batch]
        embeddings = embedding_model.encode(texts, show_progress_bar=False).tolist()
        collection.add(ids=ids, embeddings=embeddings, documents=texts, metadatas=metas)
        total += len(batch)
        print(f"  Indexed {total}/{len(chunked_documents)} chunks...")
    
    print(f"\nVector store built! Total chunks indexed: {collection.count()}")
    
    # 4. Save config
    config = {
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "embedding_model_name": EMBEDDING_MODEL_NAME,
        "collection_name": COLLECTION_NAME,
        "total_documents": len(documents),
        "total_chunks": len(chunked_documents)
    }
    config_path = os.path.join(VECTOR_STORE_DIR, "config.json")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"Config saved to {config_path}")

if __name__ == "__main__":
    main()
