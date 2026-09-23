import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.token = None
        self.role = None
        
    def login(self, email, password):
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={"email": email, "password": password},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            self.token = data.get("access_token")
            self.role = data.get("role")
            return True, None
        except requests.exceptions.RequestException as e:
            if e.response is not None and e.response.status_code == 401:
                return False, "Invalid credentials."
            return False, f"Connection error: {e}"

    def query(self, question):
        if not self.token:
            return False, "Not authenticated", []
        
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.post(
                f"{self.base_url}/query/",
                json={"question": question},
                headers=headers,
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            return True, data.get("answer"), data.get("sources", [])
        except requests.exceptions.RequestException as e:
            if e.response is not None:
                return False, f"API Error: {e.response.text}", []
            return False, f"Connection error: {e}", []
