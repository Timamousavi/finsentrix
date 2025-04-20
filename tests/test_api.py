import pytest
from fastapi.testclient import TestClient
from src.api.main import app
import jwt
from datetime import datetime, timedelta

client = TestClient(app)

# Test data
TEST_USERNAME = "testuser"
TEST_PASSWORD = "testpass"
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"

@pytest.fixture
def test_token():
    # Create a test token
    access_token_expires = timedelta(minutes=30)
    to_encode = {"sub": TEST_USERNAME, "exp": datetime.utcnow() + access_token_expires}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Iranian Stock Market Sentiment Analysis API"}

def test_login():
    response = client.post(
        "/token",
        data={"username": TEST_USERNAME, "password": TEST_PASSWORD}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials():
    response = client.post(
        "/token",
        data={"username": "invalid", "password": "invalid"}
    )
    assert response.status_code == 401

def test_analyze_sentiment(test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.post(
        "/analyze",
        json={"text": "سهام شرکت فولاد امروز با افزایش قیمت مواجه شد"},
        headers=headers
    )
    assert response.status_code == 200
    assert "sentiment" in response.json()
    assert "confidence" in response.json()
    assert "model_version" in response.json()
    assert "processing_time" in response.json()

def test_analyze_sentiment_unauthorized():
    response = client.post(
        "/analyze",
        json={"text": "سهام شرکت فولاد امروز با افزایش قیمت مواجه شد"}
    )
    assert response.status_code == 401

def test_analyze_batch_sentiment(test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.post(
        "/analyze/batch",
        json={
            "texts": [
                "سهام شرکت فولاد امروز با افزایش قیمت مواجه شد",
                "بازار بورس امروز با کاهش شاخص همراه بود"
            ]
        },
        headers=headers
    )
    assert response.status_code == 200
    assert "results" in response.json()
    assert "total_processing_time" in response.json()
    assert len(response.json()["results"]) == 2

def test_get_model_info(test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/model/info", headers=headers)
    assert response.status_code == 200
    assert "version" in response.json()
    assert "created_at" in response.json()
    assert "last_updated" in response.json()
    assert "performance_metrics" in response.json()

def test_rate_limiting(test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    # Make more than 5 requests per minute to the root endpoint
    for _ in range(6):
        response = client.get("/", headers=headers)
    assert response.status_code == 429  # Too Many Requests

def test_invalid_input(test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    # Test empty text
    response = client.post(
        "/analyze",
        json={"text": ""},
        headers=headers
    )
    assert response.status_code == 422  # Validation Error

    # Test text too long
    long_text = "a" * 1001
    response = client.post(
        "/analyze",
        json={"text": long_text},
        headers=headers
    )
    assert response.status_code == 422  # Validation Error

def test_batch_invalid_input(test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    # Test empty batch
    response = client.post(
        "/analyze/batch",
        json={"texts": []},
        headers=headers
    )
    assert response.status_code == 422  # Validation Error

    # Test batch too large
    large_batch = ["text"] * 101
    response = client.post(
        "/analyze/batch",
        json={"texts": large_batch},
        headers=headers
    )
    assert response.status_code == 422  # Validation Error 