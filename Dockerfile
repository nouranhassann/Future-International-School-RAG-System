FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY data/vector_store /data/vector_store

ENV VECTOR_STORE_PATH=/data/vector_store
ENV OLLAMA_BASE_URL=http://host.docker.internal:11434

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
