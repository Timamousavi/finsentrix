import pytest
from unittest.mock import patch, MagicMock
from src.cli import analyze_text, start_server, main

def test_analyze_text():
    # Mock the TextProcessor and SentimentAnalyzer
    with patch('src.cli.TextProcessor') as mock_processor, \
         patch('src.cli.SentimentAnalyzer') as mock_analyzer:
        
        # Setup mocks
        mock_processor_instance = MagicMock()
        mock_processor.return_value = mock_processor_instance
        mock_processor_instance.process.return_value = "processed text"
        
        mock_analyzer_instance = MagicMock()
        mock_analyzer.return_value = mock_analyzer_instance
        mock_analyzer_instance.analyze.return_value = {
            "sentiment": "positive",
            "confidence": 0.95,
            "model_version": "1.0"
        }
        
        # Test the function
        result = analyze_text("test text", "1.0")
        
        # Verify the result
        assert result["text"] == "test text"
        assert result["processed_text"] == "processed text"
        assert result["sentiment"] == "positive"
        assert result["confidence"] == 0.95
        assert result["model_version"] == "1.0"
        
        # Verify the mocks were called correctly
        mock_processor_instance.process.assert_called_once_with("test text")
        mock_analyzer_instance.analyze.assert_called_once_with("processed text", "1.0")

def test_start_server():
    with patch('src.cli.uvicorn') as mock_uvicorn:
        start_server("localhost", 8080)
        mock_uvicorn.run.assert_called_once_with(app, host="localhost", port=8080)

def test_cli_analyze_command():
    with patch('src.cli.analyze_text') as mock_analyze, \
         patch('sys.argv', ['cli.py', 'analyze', 'test text', '--model', '1.0']):
        
        mock_analyze.return_value = {
            "text": "test text",
            "processed_text": "processed text",
            "sentiment": "positive",
            "confidence": 0.95,
            "model_version": "1.0"
        }
        
        with patch('builtins.print') as mock_print:
            main()
            
            # Verify the output
            mock_print.assert_any_call("\nAnalysis Results:")
            mock_print.assert_any_call("Text: test text")
            mock_print.assert_any_call("Processed Text: processed text")
            mock_print.assert_any_call("Sentiment: positive")
            mock_print.assert_any_call("Confidence: 0.95")
            mock_print.assert_any_call("Model Version: 1.0")

def test_cli_serve_command():
    with patch('src.cli.start_server') as mock_server, \
         patch('sys.argv', ['cli.py', 'serve', '--host', 'localhost', '--port', '8080']):
        
        with patch('builtins.print') as mock_print:
            main()
            
            # Verify the output and server start
            mock_print.assert_called_once_with("Starting server on localhost:8080")
            mock_server.assert_called_once_with("localhost", 8080)

def test_cli_no_command():
    with patch('sys.argv', ['cli.py']), \
         patch('argparse.ArgumentParser.print_help') as mock_print_help, \
         patch('sys.exit') as mock_exit:
        
        main()
        mock_print_help.assert_called_once()
        mock_exit.assert_called_once_with(1) 