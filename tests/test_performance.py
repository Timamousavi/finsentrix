import pytest
import time
import psutil
import asyncio
from fastapi.testclient import TestClient
from src.api.main import app
from concurrent.futures import ThreadPoolExecutor

client = TestClient(app)

def measure_memory_usage():
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024  # MB

def test_api_response_time():
    start_time = time.time()
    response = client.get("/health")
    end_time = time.time()
    
    assert response.status_code == 200
    assert (end_time - start_time) < 0.1  # Response should be under 100ms

def test_batch_processing_performance():
    # Generate 100 sample texts
    sample_texts = [f"این شرکت در سال جاری عملکرد خوبی داشته است {i}" for i in range(100)]
    
    start_time = time.time()
    response = client.post(
        "/analyze/batch",
        json={"texts": sample_texts}
    )
    end_time = time.time()
    
    assert response.status_code == 200
    assert len(response.json()["results"]) == 100
    assert (end_time - start_time) < 5.0  # Should process 100 texts in under 5 seconds

def test_memory_usage():
    initial_memory = measure_memory_usage()
    
    # Process multiple requests
    for _ in range(10):
        client.post(
            "/analyze",
            json={"text": "این شرکت در سال جاری عملکرد خوبی داشته است"}
        )
    
    final_memory = measure_memory_usage()
    memory_increase = final_memory - initial_memory
    
    assert memory_increase < 50  # Memory increase should be less than 50MB

def test_concurrent_requests():
    def make_request():
        response = client.post(
            "/analyze",
            json={"text": "این شرکت در سال جاری عملکرد خوبی داشته است"}
        )
        return response.status_code
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(10)]
        results = [future.result() for future in futures]
    
    assert all(code == 200 for code in results)

@pytest.mark.asyncio
async def test_async_performance():
    async def make_async_request():
        response = client.post(
            "/analyze",
            json={"text": "این شرکت در سال جاری عملکرد خوبی داشته است"}
        )
        return response.status_code
    
    tasks = [make_async_request() for _ in range(10)]
    results = await asyncio.gather(*tasks)
    
    assert all(code == 200 for code in results)

def test_real_time_data_performance():
    start_time = time.time()
    response = client.get("/api/dashboard/real-time")
    end_time = time.time()
    
    assert response.status_code == 200
    assert (end_time - start_time) < 0.5  # Real-time data should be fetched in under 500ms 