import os
import json
import torch
from datetime import datetime
from typing import Dict, Optional, List
import logging
from pathlib import Path
import shutil
from .market_sentiment_analyzer import MarketSentimentAnalyzer

class ModelManager:
    """Manages model versioning, persistence, and deployment."""
    
    def __init__(self, model_dir: str = "models"):
        """Initialize the model manager.
        
        Args:
            model_dir: Directory to store model versions
        """
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        
        # Load version history
        self.version_history = self._load_version_history()
        
    def _load_version_history(self) -> Dict:
        """Load model version history from file."""
        history_file = self.model_dir / "version_history.json"
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"versions": []}
    
    def _save_version_history(self):
        """Save model version history to file."""
        history_file = self.model_dir / "version_history.json"
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(self.version_history, f, indent=2)
    
    def save_model(
        self,
        model: MarketSentimentAnalyzer,
        version: str = None,
        metadata: Optional[Dict] = None
    ) -> str:
        """Save a model version with metadata.
        
        Args:
            model: The model to save
            version: Optional version string (defaults to timestamp)
            metadata: Optional metadata about the model
            
        Returns:
            str: Version identifier
        """
        if version is None:
            version = datetime.now().strftime("%Y%m%d_%H%M%S")
            
        version_dir = self.model_dir / version
        version_dir.mkdir(exist_ok=True)
        
        # Save model state
        torch.save(model.model.state_dict(), version_dir / "model.pt")
        
        # Save tokenizer
        model.tokenizer.save_pretrained(version_dir / "tokenizer")
        
        # Save metadata
        metadata = metadata or {}
        metadata.update({
            "version": version,
            "timestamp": datetime.now().isoformat(),
            "model_name": model.model_name,
            "device": model.device,
            "market_thresholds": model.market_thresholds
        })
        
        with open(version_dir / "metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
            
        # Update version history
        self.version_history["versions"].append({
            "version": version,
            "timestamp": metadata["timestamp"],
            "metadata": metadata
        })
        self._save_version_history()
        
        self.logger.info(f"Saved model version {version}")
        return version
    
    def load_model(self, version: str) -> MarketSentimentAnalyzer:
        """Load a specific model version.
        
        Args:
            version: Version identifier to load
            
        Returns:
            MarketSentimentAnalyzer: Loaded model instance
        """
        version_dir = self.model_dir / version
        if not version_dir.exists():
            raise ValueError(f"Model version {version} not found")
            
        # Load metadata
        with open(version_dir / "metadata.json", 'r', encoding='utf-8') as f:
            metadata = json.load(f)
            
        # Initialize model
        model = MarketSentimentAnalyzer(
            model_name=metadata["model_name"],
            device=metadata["device"]
        )
        
        # Load model state
        model.model.load_state_dict(torch.load(version_dir / "model.pt"))
        
        # Load tokenizer
        model.tokenizer = model.tokenizer.from_pretrained(version_dir / "tokenizer")
        
        # Restore market thresholds
        model.market_thresholds = metadata["market_thresholds"]
        
        self.logger.info(f"Loaded model version {version}")
        return model
    
    def get_latest_version(self) -> Optional[str]:
        """Get the latest model version.
        
        Returns:
            Optional[str]: Latest version identifier or None if no versions exist
        """
        versions = self.version_history["versions"]
        if not versions:
            return None
        return versions[-1]["version"]
    
    def list_versions(self) -> List[Dict]:
        """List all available model versions.
        
        Returns:
            List[Dict]: List of version information
        """
        return self.version_history["versions"]
    
    def delete_version(self, version: str) -> None:
        """Delete a specific model version.
        
        Args:
            version: Version identifier to delete
        """
        version_dir = self.model_dir / version
        if not version_dir.exists():
            raise ValueError(f"Model version {version} not found")
            
        # Remove version directory
        shutil.rmtree(version_dir)
        
        # Update version history
        self.version_history["versions"] = [
            v for v in self.version_history["versions"]
            if v["version"] != version
        ]
        self._save_version_history()
        
        self.logger.info(f"Deleted model version {version}")
    
    def get_version_metadata(self, version: str) -> Dict:
        """Get metadata for a specific version.
        
        Args:
            version: Version identifier
            
        Returns:
            Dict: Version metadata
        """
        version_dir = self.model_dir / version
        if not version_dir.exists():
            raise ValueError(f"Model version {version} not found")
            
        with open(version_dir / "metadata.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def deploy_version(self, version: str, target_dir: str) -> None:
        """Deploy a model version to a target directory.
        
        Args:
            version: Version identifier to deploy
            target_dir: Target directory for deployment
        """
        version_dir = self.model_dir / version
        if not version_dir.exists():
            raise ValueError(f"Model version {version} not found")
            
        target_path = Path(target_dir)
        target_path.mkdir(parents=True, exist_ok=True)
        
        # Copy model files
        shutil.copytree(version_dir, target_path / version, dirs_exist_ok=True)
        
        self.logger.info(f"Deployed model version {version} to {target_dir}")
    
    def compare_versions(self, version1: str, version2: str) -> Dict:
        """Compare two model versions.
        
        Args:
            version1: First version identifier
            version2: Second version identifier
            
        Returns:
            Dict: Comparison results
        """
        meta1 = self.get_version_metadata(version1)
        meta2 = self.get_version_metadata(version2)
        
        comparison = {
            "versions": [version1, version2],
            "differences": {}
        }
        
        # Compare metadata fields
        for key in set(meta1.keys()) | set(meta2.keys()):
            if key not in ["timestamp", "version"]:
                if key not in meta1:
                    comparison["differences"][key] = {
                        version1: "missing",
                        version2: meta2[key]
                    }
                elif key not in meta2:
                    comparison["differences"][key] = {
                        version1: meta1[key],
                        version2: "missing"
                    }
                elif meta1[key] != meta2[key]:
                    comparison["differences"][key] = {
                        version1: meta1[key],
                        version2: meta2[key]
                    }
                    
        return comparison 