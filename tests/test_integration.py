import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.models.sentiment_analyzer import SentimentAnalyzer
from src.utils.text_processor import FinancialTextProcessor
import numpy as np
import os
import tempfile
import shutil

client = TestClient(app)

@pytest.fixture
def test_data():
    return {
        "texts": [
            "سهام شرکت فولاد امروز با افزایش قیمت مواجه شد",
            "بازار بورس امروز با کاهش شاخص همراه بود",
            "شرکت فولاد سود خوبی اعلام کرد"
        ],
        "labels": [1, 0, 1]  # 1: positive, 0: negative
    }

@pytest.fixture
def temp_model_dir():
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup
    shutil.rmtree(temp_dir)

def test_end_to_end_workflow(test_data, temp_model_dir):
    # Initialize components
    analyzer = SentimentAnalyzer()
    processor = FinancialTextProcessor()
    
    # Test text processing
    processed_texts = processor.batch_process(test_data["texts"])
    assert len(processed_texts) == len(test_data["texts"])
    
    # Test model training
    metrics = analyzer.train(test_data["texts"], test_data["labels"])
    assert "train" in metrics
    assert "test" in metrics
    
    # Test model saving
    analyzer.save_model(temp_model_dir)
    assert os.path.exists(os.path.join(temp_model_dir, "model.joblib"))
    assert os.path.exists(os.path.join(temp_model_dir, "vectorizer.joblib"))
    assert os.path.exists(os.path.join(temp_model_dir, "metadata.json"))
    
    # Test model loading
    new_analyzer = SentimentAnalyzer(temp_model_dir)
    assert new_analyzer.metadata["version"] == analyzer.metadata["version"]
    
    # Test predictions
    labels, probabilities = new_analyzer.predict(test_data["texts"])
    assert isinstance(labels, np.ndarray)
    assert isinstance(probabilities, np.ndarray)
    assert len(labels) == len(test_data["texts"])

def test_api_integration(test_data):
    # Test login
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test single text analysis
    response = client.post(
        "/analyze",
        json={"text": test_data["texts"][0]},
        headers=headers
    )
    assert response.status_code == 200
    result = response.json()
    assert "sentiment" in result
    assert "confidence" in result
    
    # Test batch analysis
    response = client.post(
        "/analyze/batch",
        json={"texts": test_data["texts"]},
        headers=headers
    )
    assert response.status_code == 200
    results = response.json()
    assert "results" in results
    assert len(results["results"]) == len(test_data["texts"])
    
    # Test model info
    response = client.get("/model/info", headers=headers)
    assert response.status_code == 200
    info = response.json()
    assert "version" in info
    assert "performance_metrics" in info

def test_error_handling_integration():
    # Test invalid token
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.post(
        "/analyze",
        json={"text": "سهام شرکت فولاد"},
        headers=headers
    )
    assert response.status_code == 401
    
    # Test invalid input
    response = client.post(
        "/analyze",
        json={"text": ""},
        headers=headers
    )
    assert response.status_code == 422
    
    # Test rate limiting
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpass"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Make multiple requests to trigger rate limit
    for _ in range(6):
        response = client.get("/", headers=headers)
    assert response.status_code == 429

def test_model_versioning_integration(temp_model_dir):
    # Initialize and train first version
    analyzer_v1 = SentimentAnalyzer()
    analyzer_v1.metadata["version"] = "1.0.0"
    analyzer_v1.save_model(temp_model_dir)
    
    # Load and verify version
    analyzer_v1_loaded = SentimentAnalyzer(temp_model_dir)
    assert analyzer_v1_loaded.metadata["version"] == "1.0.0"
    
    # Update version
    analyzer_v1_loaded.metadata["version"] = "1.1.0"
    analyzer_v1_loaded.save_model(temp_model_dir)
    
    # Load and verify updated version
    analyzer_v2 = SentimentAnalyzer(temp_model_dir)
    assert analyzer_v2.metadata["version"] == "1.1.0"

def test_performance_integration(test_data):
    import time
    
    # Initialize analyzer
    analyzer = SentimentAnalyzer()
    
    # Test single text processing time
    start_time = time.time()
    analyzer.predict([test_data["texts"][0]])
    single_text_time = time.time() - start_time
    
    # Test batch processing time
    start_time = time.time()
    analyzer.predict(test_data["texts"])
    batch_time = time.time() - start_time
    
    # Verify batch processing is more efficient
    assert batch_time < single_text_time * len(test_data["texts"])
    
    # Test API response time
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpass"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    start_time = time.time()
    response = client.post(
        "/analyze",
        json={"text": test_data["texts"][0]},
        headers=headers
    )
    api_time = time.time() - start_time
    
    # Verify API response time is reasonable
    assert api_time < 1.0  # Response should be under 1 second 