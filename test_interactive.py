import requests
import json

def analyze_text(text):
    """Analyze a single text."""
    response = requests.post(
        "http://localhost:8000/analyze",
        json={"text": text}
    )
    return response.json()

def analyze_batch(texts):
    """Analyze multiple texts."""
    response = requests.post(
        "http://localhost:8000/analyze/batch",
        json={"texts": texts}
    )
    return response.json()

def print_result(result):
    """Pretty print analysis result."""
    print("\nAnalysis Result:")
    print(f"Text: {result['text']}")
    print(f"Sentiment: {result['sentiment']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print("\nDetails:")
    for term, score in result['details'].items():
        print(f"- {term}: {score:+.2f}")

def main():
    while True:
        print("\nIranian Stock Market Sentiment Analyzer")
        print("1. Analyze single text")
        print("2. Analyze multiple texts")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            text = input("\nEnter Persian financial text to analyze: ")
            try:
                result = analyze_text(text)
                print_result(result)
            except Exception as e:
                print(f"Error: {str(e)}")
        
        elif choice == "2":
            texts = []
            while True:
                text = input("\nEnter Persian financial text (or press Enter to finish): ")
                if not text:
                    break
                texts.append(text)
            
            if texts:
                try:
                    results = analyze_batch(texts)
                    for result in results['results']:
                        print_result(result)
                except Exception as e:
                    print(f"Error: {str(e)}")
            else:
                print("No texts entered.")
        
        elif choice == "3":
            print("\nGoodbye!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main() 