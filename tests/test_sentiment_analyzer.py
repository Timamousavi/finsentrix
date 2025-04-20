import pytest
import numpy as np
from src.models.sentiment_analyzer import SentimentAnalyzer

@pytest.fixture
def analyzer():
    return SentimentAnalyzer()

@pytest.fixture
def sample_texts():
    return [
        "سهام شرکت فولاد امروز با افزایش قیمت مواجه شد",
        "بازار بورس امروز با کاهش شاخص همراه بود",
        "شرکت فولاد سود خوبی اعلام کرد"
    ]

@pytest.fixture
def sample_labels():
    return [1, 0, 1]  # 1: positive, 0: negative

def test_initialization(analyzer):
    assert analyzer.model is not None
    assert analyzer.vectorizer is not None
    assert analyzer.metadata['version'] == '1.0.0'

def test_preprocess_data(analyzer, sample_texts):
    X = analyzer.preprocess_data(sample_texts)
    assert isinstance(X, np.ndarray)
    assert X.shape[0] == len(sample_texts)

def test_train(analyzer, sample_texts, sample_labels):
    metrics = analyzer.train(sample_texts, sample_labels)
    assert 'train' in metrics
    assert 'test' in metrics
    assert 'accuracy' in metrics['train']
    assert 'accuracy' in metrics['test']

def test_predict(analyzer, sample_texts):
    labels, probabilities = analyzer.predict(sample_texts)
    assert isinstance(labels, np.ndarray)
    assert isinstance(probabilities, np.ndarray)
    assert len(labels) == len(sample_texts)
    assert len(probabilities) == len(sample_texts)

def test_evaluate(analyzer, sample_texts, sample_labels):
    metrics = analyzer.evaluate(sample_texts, sample_labels)
    assert 'classification_report' in metrics
    assert 'confusion_matrix' in metrics
    assert 'accuracy' in metrics

def test_tune_hyperparameters(analyzer, sample_texts, sample_labels):
    best_params = analyzer.tune_hyperparameters(sample_texts, sample_labels)
    assert 'best_parameters' in best_params
    assert 'best_score' in best_params
    assert isinstance(best_params['best_score'], float)

def test_save_and_load_model(analyzer, sample_texts, sample_labels, tmp_path):
    # Train model first
    analyzer.train(sample_texts, sample_labels)
    
    # Save model
    model_dir = tmp_path / "test_model"
    analyzer.save_model(str(model_dir))
    
    # Create new analyzer and load model
    new_analyzer = SentimentAnalyzer(str(model_dir))
    
    # Verify loaded model works
    labels, _ = new_analyzer.predict(sample_texts)
    assert isinstance(labels, np.ndarray)
    assert len(labels) == len(sample_texts)

def test_batch_processing(analyzer, sample_texts):
    results = analyzer.text_processor.batch_process(sample_texts)
    assert len(results) == len(sample_texts)
    for result in results:
        assert 'original_text' in result
        assert 'normalized_text' in result
        assert 'tokens' in result
        assert 'financial_terms' in result 