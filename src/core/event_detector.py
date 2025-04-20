from typing import Dict, List, Optional, Tuple
import numpy as np
from datetime import datetime
import spacy
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
import yaml
import os

class EventDetector:
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the event detector with configuration and NLP models."""
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = PhraseMatcher(self.nlp.vocab)
        
        # Load event patterns from config
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            self.event_patterns = config.get("event_patterns", {})
            
        # Initialize phrase matcher with event patterns
        for event_type, patterns in self.event_patterns.items():
            patterns = [self.nlp(text) for text in patterns]
            self.matcher.add(event_type, None, *patterns)
            
    def detect_events(self, text: str) -> List[Dict]:
        """Detect events in a given text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of detected events with their types and confidence scores
        """
        doc = self.nlp(text)
        matches = self.matcher(doc)
        
        events = []
        for match_id, start, end in matches:
            event_type = self.nlp.vocab.strings[match_id]
            span = doc[start:end]
            
            # Calculate confidence based on context
            confidence = self._calculate_confidence(doc, span, event_type)
            
            events.append({
                "type": event_type,
                "text": span.text,
                "start": start,
                "end": end,
                "confidence": confidence,
                "timestamp": datetime.now().isoformat()
            })
            
        return events
        
    def _calculate_confidence(self, doc, span, event_type) -> float:
        """Calculate confidence score for a detected event.
        
        Args:
            doc: The full document
            span: The matched span
            event_type: Type of the event
            
        Returns:
            Confidence score between 0 and 1
        """
        # Base confidence from pattern matching
        confidence = 0.7
        
        # Boost confidence if event is in a sentence with market-related terms
        market_terms = {"stock", "market", "price", "trade", "invest", "share"}
        sentence = span.sent
        if any(term in sentence.text.lower() for term in market_terms):
            confidence += 0.2
            
        # Reduce confidence if event is in a question
        if "?" in sentence.text:
            confidence -= 0.1
            
        return min(max(confidence, 0), 1)
        
    def get_event_timeline(self, texts: List[str], timestamps: Optional[List[datetime]] = None) -> List[Dict]:
        """Create a timeline of events from multiple texts.
        
        Args:
            texts: List of texts to analyze
            timestamps: Optional list of timestamps for each text
            
        Returns:
            List of events with their timestamps
        """
        if timestamps is None:
            timestamps = [datetime.now()] * len(texts)
            
        events = []
        for text, timestamp in zip(texts, timestamps):
            detected = self.detect_events(text)
            for event in detected:
                event["timestamp"] = timestamp.isoformat()
            events.extend(detected)
            
        # Sort events by timestamp
        events.sort(key=lambda x: x["timestamp"])
        return events
        
    def analyze_event_impact(self, event: Dict, market_data: Dict) -> float:
        """Analyze the potential impact of an event on the market.
        
        Args:
            event: Detected event
            market_data: Current market data
            
        Returns:
            Impact score between -1 and 1
        """
        # Base impact score
        impact = 0.0
        
        # Adjust impact based on event type
        if event["type"] in ["earnings", "merger", "acquisition"]:
            impact += 0.5
        elif event["type"] in ["regulation", "lawsuit"]:
            impact -= 0.3
            
        # Adjust based on confidence
        impact *= event["confidence"]
        
        # Consider market volatility
        if "volatility" in market_data:
            impact *= (1 + market_data["volatility"])
            
        return min(max(impact, -1), 1) 