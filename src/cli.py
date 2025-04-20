import argparse
import sys
from typing import Optional

from .api.main import app
from .utils.text_processor import TextProcessor
from .utils.sentiment_analyzer import SentimentAnalyzer

def analyze_text(text: str, model_version: Optional[str] = None) -> dict:
    """Analyze text sentiment using the configured model."""
    processor = TextProcessor()
    analyzer = SentimentAnalyzer()
    
    processed_text = processor.process(text)
    result = analyzer.analyze(processed_text, model_version)
    
    return {
        "text": text,
        "processed_text": processed_text,
        "sentiment": result["sentiment"],
        "confidence": result["confidence"],
        "model_version": result["model_version"]
    }

def start_server(host: str = "0.0.0.0", port: int = 8000):
    """Start the FastAPI server."""
    import uvicorn
    uvicorn.run(app, host=host, port=port)

def main():
    parser = argparse.ArgumentParser(description="FinSentrix CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze text sentiment")
    analyze_parser.add_argument("text", help="Text to analyze")
    analyze_parser.add_argument("--model", help="Model version to use")
    
    # Server command
    server_parser = subparsers.add_parser("serve", help="Start the API server")
    server_parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    server_parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    
    args = parser.parse_args()
    
    if args.command == "analyze":
        result = analyze_text(args.text, args.model)
        print("\nAnalysis Results:")
        print(f"Text: {result['text']}")
        print(f"Processed Text: {result['processed_text']}")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Model Version: {result['model_version']}")
    
    elif args.command == "serve":
        print(f"Starting server on {args.host}:{args.port}")
        start_server(args.host, args.port)
    
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main() 