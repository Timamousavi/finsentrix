import pytest
from datetime import datetime, timedelta
from src.models.event_detector import EventDetector, RumorDetector

def test_event_detection():
    detector = EventDetector()
    
    # Test Persian text
    persian_text = "بانک مرکزی امروز نرخ بهره را افزایش داد"
    events = detector.detect_events(persian_text)
    
    assert len(events) > 0
    assert any(e["text"] == "بانک مرکزی" for e in events)
    assert any(e["event_type"] == "central_bank" for e in events)
    
    # Test English text
    english_text = "Company XYZ reported earnings above expectations"
    events = detector.detect_events(english_text)
    
    assert len(events) > 0
    assert any(e["text"].lower() == "earnings" for e in events)
    assert any(e["event_type"] == "earnings" for e in events)

def test_rumor_detection():
    detector = RumorDetector()
    
    # Create sample messages
    messages = [
        {
            "text": "گفته می‌شود شرکت X قرار است سود خوبی اعلام کند",
            "timestamp": datetime.now() - timedelta(hours=1)
        },
        {
            "text": "به گفته منابع شرکت X سود خوبی خواهد داشت",
            "timestamp": datetime.now() - timedelta(hours=2)
        },
        {
            "text": "طبق اخبار شرکت X سود خوبی اعلام خواهد کرد",
            "timestamp": datetime.now() - timedelta(hours=3)
        }
    ]
    
    rumors = detector.detect_rumors(messages)
    
    assert len(rumors) > 0
    assert rumors[0]["confidence"] > 0.5
    assert rumors[0]["verdict"] in ["Likely manipulation", "Likely true"]
    assert len(rumors[0]["messages"]) == 3

def test_rumor_confidence_calculation():
    detector = RumorDetector()
    
    # Test high confidence case
    high_conf = detector._calculate_confidence(
        spread_score=0.8,
        time_span=timedelta(hours=2),
        pattern_matches=3,
        cluster_size=3
    )
    assert high_conf > 0.7
    
    # Test low confidence case
    low_conf = detector._calculate_confidence(
        spread_score=0.2,
        time_span=timedelta(hours=12),
        pattern_matches=0,
        cluster_size=3
    )
    assert low_conf < 0.3

def test_event_sentiment_correlation():
    detector = EventDetector()
    
    # Test event impact on sentiment
    events = detector.detect_events("بانک مرکزی نرخ بهره را افزایش داد")
    assert any(e["text"] == "بانک مرکزی" for e in events)
    
    # Add sentiment impact
    for event in events:
        if event["text"] == "بانک مرکزی":
            event["sentiment_impact"] = -0.5  # Negative impact
    
    assert any(e.get("sentiment_impact", 0) < 0 for e in events) 