import pytest
import torch
from src.models.market_sentiment_analyzer import MarketSentimentAnalyzer
from src.utils.text_processor import FinancialTextProcessor

@pytest.fixture
def analyzer():
    """Create a MarketSentimentAnalyzer instance for testing."""
    return MarketSentimentAnalyzer()

@pytest.fixture
def sample_texts():
    """Provide sample texts for different market types."""
    return {
        'stock': "سهام شرکت فولاد امروز با افزایش ۵ درصدی همراه بود",
        'forex': "دلار امروز با کاهش قیمت مواجه شد و به ۲۵۰۰۰ تومان رسید",
        'crypto': "بیت کوین امروز رشد خوبی داشت و به ۵۰۰۰۰ دلار رسید"
    }

def test_initialization(analyzer):
    """Test proper initialization of the analyzer."""
    assert analyzer.device in ['cuda', 'cpu']
    assert isinstance(analyzer.tokenizer, type(analyzer.tokenizer))
    assert isinstance(analyzer.model, type(analyzer.model))
    assert isinstance(analyzer.text_processor, FinancialTextProcessor)
    assert 'stock' in analyzer.market_thresholds
    assert 'forex' in analyzer.market_thresholds
    assert 'crypto' in analyzer.market_thresholds

def test_detect_market_type(analyzer, sample_texts):
    """Test market type detection."""
    for market_type, text in sample_texts.items():
        detected_type = analyzer.detect_market_type(text)
        assert detected_type == market_type

def test_analyze_sentiment(analyzer, sample_texts):
    """Test sentiment analysis for different market types."""
    for market_type, text in sample_texts.items():
        result = analyzer.analyze_sentiment(text)
        assert 'sentiment' in result
        assert 'confidence' in result
        assert 'market_type' in result
        assert 'scores' in result
        assert result['market_type'] == market_type
        assert result['sentiment'] in ['positive', 'neutral', 'negative']
        assert 0 <= result['confidence'] <= 1

def test_analyze_batch(analyzer, sample_texts):
    """Test batch sentiment analysis."""
    texts = list(sample_texts.values())
    results = analyzer.analyze_batch(texts)
    
    assert len(results) == len(texts)
    for result in results:
        assert 'sentiment' in result
        assert 'confidence' in result
        assert 'market_type' in result
        assert 'scores' in result

def test_get_market_insights(analyzer, sample_texts):
    """Test market insights generation."""
    texts = list(sample_texts.values())
    insights = analyzer.get_market_insights(texts)
    
    assert 'overall_sentiment' in insights
    assert 'sentiment_distribution' in insights
    assert 'average_confidence' in insights
    assert 'market_type' in insights
    assert 'total_samples' in insights
    
    assert insights['total_samples'] == len(texts)
    assert insights['overall_sentiment'] in ['bullish', 'bearish', 'neutral']
    assert sum(insights['sentiment_distribution'].values()) == pytest.approx(100.0)

def test_market_thresholds(analyzer):
    """Test market-specific thresholds."""
    thresholds = analyzer.market_thresholds
    
    # Test threshold ranges
    for market in ['stock', 'forex', 'crypto']:
        assert 0 < thresholds[market]['positive'] < 1
        assert 0 < thresholds[market]['negative'] < 1
        assert 0 < thresholds[market]['confidence'] < 1
        assert thresholds[market]['positive'] > thresholds[market]['negative']

def test_error_handling(analyzer):
    """Test error handling for invalid inputs."""
    # Test empty text
    with pytest.raises(ValueError):
        analyzer.analyze_sentiment("")
    
    # Test invalid market type
    with pytest.raises(ValueError):
        analyzer.analyze_sentiment("test", market_type="invalid_market")
    
    # Test empty batch
    with pytest.raises(ValueError):
        analyzer.analyze_batch([])

def test_model_output_format(analyzer, sample_texts):
    """Test format of model outputs."""
    for text in sample_texts.values():
        result = analyzer.analyze_sentiment(text)
        scores = result['scores']
        
        assert 'positive' in scores
        assert 'neutral' in scores
        assert 'negative' in scores
        assert sum(scores.values()) == pytest.approx(1.0)
        assert all(0 <= score <= 1 for score in scores.values())

def test_confidence_scoring(analyzer, sample_texts):
    """Test confidence scoring mechanism."""
    for text in sample_texts.values():
        result = analyzer.analyze_sentiment(text)
        scores = result['scores']
        confidence = result['confidence']
        
        # Confidence should be the maximum score
        assert confidence == max(scores.values())
        
        # If confidence is high, sentiment should be clear
        if confidence > 0.8:
            assert result['sentiment'] != 'neutral'

def test_market_specific_analysis(analyzer, sample_texts):
    """Test market-specific analysis features."""
    for market_type, text in sample_texts.items():
        result = analyzer.analyze_sentiment(text, market_type)
        assert result['market_type'] == market_type
        
        # Market-specific thresholds should be applied
        thresholds = analyzer.market_thresholds[market_type]
        if result['confidence'] < thresholds['confidence']:
            assert result['sentiment'] == 'neutral'

def test_performance(analyzer, sample_texts):
    """Test performance of the analyzer."""
    import time
    
    # Test single text analysis time
    start_time = time.time()
    analyzer.analyze_sentiment(sample_texts['stock'])
    single_time = time.time() - start_time
    assert single_time < 1.0  # Should take less than 1 second
    
    # Test batch analysis time
    texts = list(sample_texts.values()) * 10  # 30 texts
    start_time = time.time()
    analyzer.analyze_batch(texts)
    batch_time = time.time() - start_time
    assert batch_time < 5.0  # Should take less than 5 seconds for 30 texts 