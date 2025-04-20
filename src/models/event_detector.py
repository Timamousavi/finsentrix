from typing import List, Dict, Optional
import pandas as pd
from datetime import datetime, timedelta
from transformers import pipeline
from sklearn.cluster import DBSCAN
import numpy as np
import logging

class EventDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ner_pipeline = pipeline("ner", model="HooshvareLab/bert-fa-base-ner")
        self.event_types = {
            "earnings": ["سود", "زیان", "درآمد", "EPS", "earnings", "profit", "loss"],
            "central_bank": ["بانک مرکزی", "نرخ بهره", "سیاست پولی", "central bank", "interest rate"],
            "political": ["سیاسی", "تحریم", "سیاست", "political", "sanctions"],
            "market": ["بازار", "شاخص", "نوسان", "market", "index", "volatility"]
        }
        
    def detect_events(self, text: str) -> List[Dict]:
        """Detect events in text using NER and keyword matching."""
        try:
            # Get named entities
            entities = self.ner_pipeline(text)
            
            # Extract event-related entities
            events = []
            for entity in entities:
                if entity["entity"] in ["ORG", "EVENT", "DATE"]:
                    events.append({
                        "type": "entity",
                        "text": entity["word"],
                        "entity_type": entity["entity"],
                        "confidence": entity["score"]
                    })
            
            # Check for event keywords
            for event_type, keywords in self.event_types.items():
                for keyword in keywords:
                    if keyword.lower() in text.lower():
                        events.append({
                            "type": "keyword",
                            "text": keyword,
                            "event_type": event_type,
                            "confidence": 1.0
                        })
            
            return events
        except Exception as e:
            self.logger.error(f"Error detecting events: {str(e)}")
            return []

class RumorDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.clusterer = DBSCAN(eps=0.5, min_samples=3)
        self.rumor_patterns = [
            r"گفته می‌شود",
            r"به گفته منابع",
            r"طبق اخبار",
            r"rumor",
            r"according to sources",
            r"unconfirmed"
        ]
        
    def detect_rumors(self, messages: List[Dict], time_window: int = 12) -> List[Dict]:
        """Detect potential rumors in messages."""
        try:
            # Filter messages within time window
            now = datetime.now()
            recent_messages = [
                msg for msg in messages 
                if now - msg["timestamp"] <= timedelta(hours=time_window)
            ]
            
            if not recent_messages:
                return []
            
            # Extract text features
            texts = [msg["text"] for msg in recent_messages]
            
            # Cluster similar messages
            clusters = self.clusterer.fit_predict(texts)
            
            # Analyze clusters
            rumors = []
            for cluster_id in set(clusters):
                if cluster_id == -1:  # Noise
                    continue
                    
                cluster_messages = [
                    msg for i, msg in enumerate(recent_messages)
                    if clusters[i] == cluster_id
                ]
                
                # Calculate spread metrics
                spread_score = len(cluster_messages) / len(recent_messages)
                time_span = max(msg["timestamp"] for msg in cluster_messages) - \
                           min(msg["timestamp"] for msg in cluster_messages)
                
                # Check for rumor patterns
                pattern_matches = sum(
                    1 for msg in cluster_messages
                    if any(pattern in msg["text"] for pattern in self.rumor_patterns)
                )
                
                # Calculate confidence score
                confidence = self._calculate_confidence(
                    spread_score=spread_score,
                    time_span=time_span,
                    pattern_matches=pattern_matches,
                    cluster_size=len(cluster_messages)
                )
                
                rumors.append({
                    "cluster_id": cluster_id,
                    "messages": cluster_messages,
                    "spread_score": spread_score,
                    "time_span": time_span,
                    "pattern_matches": pattern_matches,
                    "confidence": confidence,
                    "verdict": "Likely manipulation" if confidence > 0.7 else "Likely true"
                })
            
            return sorted(rumors, key=lambda x: x["confidence"], reverse=True)
            
        except Exception as e:
            self.logger.error(f"Error detecting rumors: {str(e)}")
            return []
    
    def _calculate_confidence(
        self,
        spread_score: float,
        time_span: timedelta,
        pattern_matches: int,
        cluster_size: int
    ) -> float:
        """Calculate confidence score for rumor detection."""
        # Normalize time span to hours
        time_score = min(time_span.total_seconds() / 3600, 1.0)
        
        # Calculate pattern match ratio
        pattern_score = pattern_matches / cluster_size if cluster_size > 0 else 0
        
        # Combine scores with weights
        confidence = (
            0.4 * spread_score +  # Spread importance
            0.3 * time_score +    # Time span importance
            0.3 * pattern_score   # Pattern match importance
        )
        
        return min(max(confidence, 0.0), 1.0) 