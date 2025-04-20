from typing import Dict, List, Optional, Tuple
import numpy as np
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from collections import Counter
import re

class RumorAnalyzer:
    def __init__(self, min_samples: int = 3, eps: float = 0.5):
        """Initialize the rumor analyzer with clustering parameters."""
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.clusterer = DBSCAN(
            min_samples=min_samples,
            eps=eps,
            metric='cosine'
        )
        
    def detect_rumors(self, texts: List[str], timestamps: Optional[List[datetime]] = None) -> List[Dict]:
        """Detect potential rumors in a collection of texts.
        
        Args:
            texts: List of texts to analyze
            timestamps: Optional list of timestamps for each text
            
        Returns:
            List of detected rumors with their characteristics
        """
        if not texts:
            return []
            
        # Vectorize texts
        X = self.vectorizer.fit_transform(texts)
        
        # Cluster similar texts
        clusters = self.clusterer.fit_predict(X.toarray())
        
        rumors = []
        for cluster_id in set(clusters):
            if cluster_id == -1:  # Noise points
                continue
                
            # Get texts in this cluster
            cluster_texts = [text for i, text in enumerate(texts) if clusters[i] == cluster_id]
            cluster_timestamps = [timestamps[i] for i, t in enumerate(timestamps) if clusters[i] == cluster_id]
            
            # Analyze rumor characteristics
            rumor = self._analyze_rumor(cluster_texts, cluster_timestamps)
            rumors.append(rumor)
            
        return rumors
        
    def _analyze_rumor(self, texts: List[str], timestamps: List[datetime]) -> Dict:
        """Analyze characteristics of a potential rumor.
        
        Args:
            texts: Texts belonging to the rumor cluster
            timestamps: Timestamps of the texts
            
        Returns:
            Dictionary containing rumor analysis results
        """
        # Calculate spread metrics
        time_range = (max(timestamps) - min(timestamps)).total_seconds() / 3600  # in hours
        spread_rate = len(texts) / (time_range + 1)  # texts per hour
        
        # Extract common phrases
        phrases = self._extract_common_phrases(texts)
        
        # Calculate confidence score
        confidence = self._calculate_confidence(texts, spread_rate)
        
        return {
            "texts": texts,
            "timestamps": [t.isoformat() for t in timestamps],
            "spread_rate": spread_rate,
            "confidence": confidence,
            "key_phrases": phrases,
            "source_count": len(set(texts)),
            "time_range_hours": time_range
        }
        
    def _extract_common_phrases(self, texts: List[str]) -> List[str]:
        """Extract common phrases from rumor texts.
        
        Args:
            texts: Texts to analyze
            
        Returns:
            List of common phrases
        """
        # Simple phrase extraction (can be enhanced with NLP)
        phrases = []
        for text in texts:
            # Split into sentences and extract noun phrases
            sentences = re.split(r'[.!?]+', text)
            for sentence in sentences:
                words = sentence.strip().split()
                if len(words) >= 2:  # Only consider phrases with 2+ words
                    phrases.extend([' '.join(words[i:i+2]) for i in range(len(words)-1)])
                    
        # Get most common phrases
        phrase_counts = Counter(phrases)
        return [phrase for phrase, count in phrase_counts.most_common(5)]
        
    def _calculate_confidence(self, texts: List[str], spread_rate: float) -> float:
        """Calculate confidence score for a detected rumor.
        
        Args:
            texts: Texts belonging to the rumor
            spread_rate: Rate at which the rumor is spreading
            
        Returns:
            Confidence score between 0 and 1
        """
        # Base confidence from spread rate
        confidence = min(spread_rate / 10, 1.0)  # Normalize spread rate
        
        # Boost confidence based on text similarity
        avg_similarity = self._calculate_text_similarity(texts)
        confidence = (confidence + avg_similarity) / 2
        
        # Reduce confidence if texts are too similar (might be spam)
        if avg_similarity > 0.9:
            confidence *= 0.7
            
        return min(max(confidence, 0), 1)
        
    def _calculate_text_similarity(self, texts: List[str]) -> float:
        """Calculate average similarity between texts.
        
        Args:
            texts: Texts to compare
            
        Returns:
            Average similarity score
        """
        if len(texts) < 2:
            return 0.0
            
        # Vectorize texts
        X = self.vectorizer.transform(texts)
        
        # Calculate pairwise similarities
        similarities = []
        for i in range(len(texts)):
            for j in range(i+1, len(texts)):
                sim = np.dot(X[i].toarray(), X[j].toarray().T)[0][0]
                similarities.append(sim)
                
        return np.mean(similarities) if similarities else 0.0
        
    def analyze_rumor_impact(self, rumor: Dict, market_data: Dict) -> float:
        """Analyze the potential impact of a rumor on the market.
        
        Args:
            rumor: Detected rumor
            market_data: Current market data
            
        Returns:
            Impact score between -1 and 1
        """
        # Base impact from confidence and spread
        impact = rumor["confidence"] * (rumor["spread_rate"] / 10)
        
        # Adjust based on market conditions
        if "volatility" in market_data:
            impact *= (1 + market_data["volatility"])
            
        # Consider source diversity
        source_diversity = min(rumor["source_count"] / 5, 1.0)
        impact *= (0.7 + 0.3 * source_diversity)
        
        return min(max(impact, -1), 1) 