from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

@patch('app.api.routes.query.generate_answer')
@patch('app.api.routes.query.retrieve_chunks')
def test_valid_query(mock_retrieve, mock_generate):
    # Setup mock returns
    mock_retrieve.return_value = [{'metadata': {'document_id': 'DOC-1'}, 'content': 'Test context'}]
    mock_generate.return_value = ('Test Answer', ['DOC-1'])

    # Need to get a valid token first
    login_res = client.post("/auth/login", json={"email": "student@example.com", "password": "password123"})
    token = login_res.json()["access_token"]

    response = client.post(
        "/query/",
        json={"question": "What is testing?"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Test Answer"
    assert "DOC-1" in data["sources"]

def test_unauthenticated_query_rejected():
    response = client.post(
        "/query/",
        json={"question": "What is testing?"}
    )
    assert response.status_code == 401

def test_invalid_input():
    # Need to get a valid token first
    login_res = client.post("/auth/login", json={"email": "student@example.com", "password": "password123"})
    token = login_res.json()["access_token"]

    response = client.post(
        "/query/",
        json={}, # Missing question field
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422
