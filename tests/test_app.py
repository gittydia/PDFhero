import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from backend.app import app
from backend.api import HeroBot
client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to PDFhero API"}

def test_chat():
    response = client.post(
        "/chat",
        json={"message": "Hello"}
    )
    assert response.status_code == 200
    assert "response" in response.json()