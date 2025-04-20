from prometheus_client import start_http_server, Counter, Gauge, Histogram
import time
from typing import Dict, Any
from functools import wraps

# Metrics
API_REQUESTS = Counter(
    'api_requests_total',
    'Total number of API requests',
    ['endpoint', 'method', 'status']
)

API_LATENCY = Histogram(
    'api_request_duration_seconds',
    'API request latency in seconds',
    ['endpoint', 'method']
)

MODEL_PREDICTIONS = Counter(
    'model_predictions_total',
    'Total number of model predictions',
    ['model_type', 'market_type']
)

MODEL_CONFIDENCE = Gauge(
    'model_confidence',
    'Model prediction confidence',
    ['model_type', 'market_type']
)

EVENT_DETECTIONS = Counter(
    'event_detections_total',
    'Total number of event detections',
    ['event_type', 'market_type']
)

RUMOR_DETECTIONS = Counter(
    'rumor_detections_total',
    'Total number of rumor detections',
    ['status', 'market_type']
)

def start_monitoring(port: int = 9090):
    """Start the Prometheus metrics server."""
    start_http_server(port)
    return True

def track_api_request(endpoint: str, method: str):
    """Decorator to track API requests and latency."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                response = await func(*args, **kwargs)
                status = 'success'
                return response
            except Exception as e:
                status = 'error'
                raise e
            finally:
                duration = time.time() - start_time
                API_REQUESTS.labels(
                    endpoint=endpoint,
                    method=method,
                    status=status
                ).inc()
                API_LATENCY.labels(
                    endpoint=endpoint,
                    method=method
                ).observe(duration)
        return wrapper
    return decorator

def track_model_prediction(model_type: str, market_type: str, confidence: float):
    """Track model predictions and confidence."""
    MODEL_PREDICTIONS.labels(
        model_type=model_type,
        market_type=market_type
    ).inc()
    MODEL_CONFIDENCE.labels(
        model_type=model_type,
        market_type=market_type
    ).set(confidence)

def track_event_detection(event_type: str, market_type: str):
    """Track event detections."""
    EVENT_DETECTIONS.labels(
        event_type=event_type,
        market_type=market_type
    ).inc()

def track_rumor_detection(status: str, market_type: str):
    """Track rumor detections."""
    RUMOR_DETECTIONS.labels(
        status=status,
        market_type=market_type
    ).inc()

def get_metrics() -> Dict[str, Any]:
    """Get current metrics values."""
    return {
        'api_requests': {
            'total': API_REQUESTS._value.get(),
            'by_endpoint': {
                ep: API_REQUESTS.labels(endpoint=ep)._value.get()
                for ep in set(labels['endpoint'] for labels in API_REQUESTS._metrics)
            }
        },
        'model_predictions': {
            'total': MODEL_PREDICTIONS._value.get(),
            'by_type': {
                mt: MODEL_PREDICTIONS.labels(model_type=mt)._value.get()
                for mt in set(labels['model_type'] for labels in MODEL_PREDICTIONS._metrics)
            }
        },
        'event_detections': {
            'total': EVENT_DETECTIONS._value.get(),
            'by_type': {
                et: EVENT_DETECTIONS.labels(event_type=et)._value.get()
                for et in set(labels['event_type'] for labels in EVENT_DETECTIONS._metrics)
            }
        },
        'rumor_detections': {
            'total': RUMOR_DETECTIONS._value.get(),
            'by_status': {
                st: RUMOR_DETECTIONS.labels(status=st)._value.get()
                for st in set(labels['status'] for labels in RUMOR_DETECTIONS._metrics)
            }
        }
    } 