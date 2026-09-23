import os

test_files = {
    "backend/tests/test_auth.py": """from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    response = client.post(
        "/auth/login",
        json={"email": "student@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "student"

def test_login_failure():
    response = client.post(
        "/auth/login",
        json={"email": "student@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
""",
    "backend/tests/test_query.py": """from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

@patch('app.services.generation.generate_answer')
@patch('app.services.retrieval.retrieve_chunks')
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
""",
    "backend/tests/test_authorization.py": """from app.services.authorization import get_allowed_access_levels, is_access_allowed

def test_student_access():
    levels = get_allowed_access_levels('student')
    assert 'student' in levels
    assert 'shared' in levels
    assert 'teacher' not in levels
    
    assert is_access_allowed('student', 'shared') is True
    assert is_access_allowed('student', 'student') is True
    assert is_access_allowed('student', 'teacher') is False

def test_teacher_access():
    levels = get_allowed_access_levels('teacher')
    assert 'student' in levels
    assert 'shared' in levels
    assert 'teacher' in levels
    
    assert is_access_allowed('teacher', 'teacher') is True
    assert is_access_allowed('teacher', 'student') is True
"""
}

def generate_tests():
    base_dir = "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant"
    for file_path, content in test_files.items():
        full_path = os.path.join(base_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
    print("Tests generated successfully.")

if __name__ == "__main__":
    generate_tests()
