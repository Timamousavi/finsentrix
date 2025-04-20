"""
Sentiment analysis model for Persian financial text.
"""
from typing import List, Dict, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import json
from datetime import datetime
import os
import logging
from ..utils.text_processor import FinancialTextProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='sentiment_analysis.log'
)
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """Sentiment analysis model for Persian financial text."""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the sentiment analyzer.
        
        Args:
            model_path (str, optional): Path to load a pre-trained model
        """
        self.text_processor = FinancialTextProcessor()
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words=None  # We handle stopwords in text processor
        )
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=30,
            random_state=42
        )
        
        # Model metadata
        self.metadata = {
            'version': '1.0.0',
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'performance_metrics': {},
            'training_data_info': {}
        }
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='sentiment_analysis.log'
        )
        self.logger = logging.getLogger(__name__)
        
        # Load model if path provided
        if model_path:
            self.load_model(model_path)

    def preprocess_data(self, texts: List[str]) -> np.ndarray:
        """
        Preprocess text data for model input.
        
        Args:
            texts (List[str]): List of input texts
            
        Returns:
            np.ndarray: Processed feature matrix
        """
        # Process texts
        processed_texts = self.text_processor.batch_process(texts)
        
        # Extract normalized texts
        normalized_texts = [p['normalized_text'] for p in processed_texts]
        
        # Vectorize texts
        if not hasattr(self, 'vectorizer_fitted'):
            X = self.vectorizer.fit_transform(normalized_texts)
            self.vectorizer_fitted = True
        else:
            X = self.vectorizer.transform(normalized_texts)
            
        return X

    def train(self, 
              texts: List[str], 
              labels: List[int],
              test_size: float = 0.2,
              random_state: int = 42) -> Dict:
        """
        Train the sentiment analysis model.
        
        Args:
            texts (List[str]): List of input texts
            labels (List[int]): List of sentiment labels
            test_size (float): Proportion of data to use for testing
            random_state (int): Random seed for reproducibility
            
        Returns:
            Dict: Training results and metrics
        """
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=test_size, random_state=random_state
        )
        
        # Preprocess training data
        X_train_processed = self.preprocess_data(X_train)
        X_test_processed = self.preprocess_data(X_test)
        
        # Train model
        self.model.fit(X_train_processed, y_train)
        
        # Evaluate model
        train_pred = self.model.predict(X_train_processed)
        test_pred = self.model.predict(X_test_processed)
        
        # Calculate metrics
        train_metrics = classification_report(y_train, train_pred, output_dict=True)
        test_metrics = classification_report(y_test, test_pred, output_dict=True)
        
        # Update metadata
        self.metadata.update({
            'last_updated': datetime.now().isoformat(),
            'performance_metrics': {
                'train': train_metrics,
                'test': test_metrics
            },
            'training_data_info': {
                'train_size': len(X_train),
                'test_size': len(X_test),
                'feature_count': X_train_processed.shape[1]
            }
        })
        
        self.logger.info("Model training completed")
        return self.metadata['performance_metrics']

    def tune_hyperparameters(self, 
                           texts: List[str], 
                           labels: List[int],
                           param_grid: Optional[Dict] = None) -> Dict:
        """
        Tune model hyperparameters using grid search.
        
        Args:
            texts (List[str]): List of input texts
            labels (List[int]): List of sentiment labels
            param_grid (Dict, optional): Parameter grid for grid search
            
        Returns:
            Dict: Best parameters and scores
        """
        if param_grid is None:
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [10, 20, 30, None],
                'min_samples_split': [2, 5, 10]
            }
        
        # Preprocess data
        X = self.preprocess_data(texts)
        
        # Perform grid search
        grid_search = GridSearchCV(
            estimator=self.model,
            param_grid=param_grid,
            cv=5,
            n_jobs=-1,
            verbose=2
        )
        
        grid_search.fit(X, labels)
        
        # Update model with best parameters
        self.model = grid_search.best_estimator_
        
        # Update metadata
        self.metadata.update({
            'best_parameters': grid_search.best_params_,
            'best_score': grid_search.best_score_
        })
        
        self.logger.info("Hyperparameter tuning completed")
        return {
            'best_parameters': grid_search.best_params_,
            'best_score': grid_search.best_score_
        }

    def predict(self, texts: List[str]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict sentiment for input texts.
        
        Args:
            texts (List[str]): List of input texts
            
        Returns:
            Tuple[np.ndarray, np.ndarray]: Predicted labels and probabilities
        """
        # Preprocess texts
        X = self.preprocess_data(texts)
        
        # Make predictions
        labels = self.model.predict(X)
        probabilities = self.model.predict_proba(X)
        
        return labels, probabilities

    def evaluate(self, texts: List[str], labels: List[int]) -> Dict:
        """
        Evaluate model performance on new data.
        
        Args:
            texts (List[str]): List of input texts
            labels (List[int]): List of true labels
            
        Returns:
            Dict: Evaluation metrics
        """
        # Make predictions
        pred_labels, _ = self.predict(texts)
        
        # Calculate metrics
        metrics = classification_report(labels, pred_labels, output_dict=True)
        confusion = confusion_matrix(labels, pred_labels).tolist()
        
        # Update metadata
        self.metadata['evaluation_metrics'] = {
            'classification_report': metrics,
            'confusion_matrix': confusion,
            'accuracy': accuracy_score(labels, pred_labels)
        }
        
        return self.metadata['evaluation_metrics']

    def save_model(self, directory: str):
        """
        Save model and metadata to directory.
        
        Args:
            directory (str): Directory to save model files
        """
        # Create directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        
        # Save model components
        joblib.dump(self.model, os.path.join(directory, 'model.joblib'))
        joblib.dump(self.vectorizer, os.path.join(directory, 'vectorizer.joblib'))
        
        # Save metadata
        with open(os.path.join(directory, 'metadata.json'), 'w') as f:
            json.dump(self.metadata, f, indent=4)
        
        self.logger.info(f"Model saved to {directory}")

    def load_model(self, directory: str):
        """
        Load model and metadata from directory.
        
        Args:
            directory (str): Directory containing model files
        """
        try:
            # Load model components
            self.model = joblib.load(os.path.join(directory, 'model.joblib'))
            self.vectorizer = joblib.load(os.path.join(directory, 'vectorizer.joblib'))
            self.vectorizer_fitted = True
            
            # Load metadata
            with open(os.path.join(directory, 'metadata.json'), 'r') as f:
                self.metadata = json.load(f)
            
            self.logger.info(f"Model loaded from {directory}")
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")
            raise

if __name__ == "__main__":
    # Initialize analyzer
    analyzer = SentimentAnalyzer()
    
    # Example data
    texts = [
        "سهام شرکت فولاد امروز با افزایش قیمت مواجه شد",
        "بازار بورس امروز با کاهش شاخص همراه بود",
        "شرکت فولاد سود خوبی اعلام کرد"
    ]
    labels = [1, 0, 1]  # 1: positive, 0: negative
    
    # Train model
    analyzer.train(texts, labels)
    
    # Make predictions
    new_texts = ["سهام فولاد رشد خوبی داشت"]
    pred_labels, probabilities = analyzer.predict(new_texts)
    
    print("Predictions:", pred_labels)
    print("Probabilities:", probabilities)
    
    # Save model
    analyzer.save_model("models/v1") 