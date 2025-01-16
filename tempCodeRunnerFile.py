from fastapi.testclient import TestClient
import os
import sys
import pytest
from .app import app, favicon_path

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to PDFhero API"}

def test_favicon():
    response = client.get("/favicon.ico")
    if os.path.exists(favicon_path):
        assert response.status_code == 200
    else:
        assert response.json() == {"error": "favicon.ico not found"}

def test_test_endpoint():
    response = client.get("/test")
    assert response.status_code == 200 
    assert response.json() == {"message": "API is working"}

def test_chat():
    test_message = "Hello"
    response = client.post("/chat", params={"message": test_message})
    assert response.status_code == 200
    assert "response" in response.json() or "error" in response.json()

def test_chat_empty_message():
    test_message = ""
    response = client.post("/chat", params={"message": test_message})
    assert response.status_code == 200
    assert "response" in response.json() or "error" in response.json()