import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    print("\nTesting root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_health():
    print("\nTesting health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_single_sentiment():
    print("\nTesting single sentiment analysis...")
    test_texts = [
        "شاخص کل بورس تهران امروز با رشد ۲ درصدی به ۱,۵۰۰,۰۰۰ واحد رسید و حجم معاملات به ۵۰۰ میلیارد تومان افزایش یافت",
        "بازار سهام امروز با افت ۱.۵ درصدی مواجه شد و شاخص هم وزن نیز ۰.۸ درصد کاهش یافت",
        "شرکت فولاد مبارکه اصفهان در گزارش ۶ ماهه خود اعلام کرد که سود خالص این شرکت نسبت به دوره مشابه سال قبل ۳۰ درصد افزایش داشته است"
    ]
    
    for text in test_texts:
        payload = {"text": text}
        response = requests.post(f"{BASE_URL}/analyze", json=payload)
        print(f"\nText: {text}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_batch_sentiment():
    print("\nTesting batch sentiment analysis...")
    texts = [
        "شاخص کل بورس تهران امروز با رشد ۲ درصدی به ۱,۵۰۰,۰۰۰ واحد رسید و حجم معاملات به ۵۰۰ میلیارد تومان افزایش یافت",
        "بازار سهام امروز با افت ۱.۵ درصدی مواجه شد و شاخص هم وزن نیز ۰.۸ درصد کاهش یافت",
        "شرکت فولاد مبارکه اصفهان در گزارش ۶ ماهه خود اعلام کرد که سود خالص این شرکت نسبت به دوره مشابه سال قبل ۳۰ درصد افزایش داشته است",
        "بورس تهران امروز با معاملات مثبت به کار خود پایان داد و شاخص کل با افزایش ۰.۵ درصدی همراه بود"
    ]
    
    payload = {"texts": texts}
    response = requests.post(f"{BASE_URL}/analyze/batch", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_real_time_data():
    print("\nTesting real-time data endpoint...")
    response = requests.get(f"{BASE_URL}/api/dashboard/real-time")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    print("Starting API tests...")
    test_root()
    test_health()
    test_single_sentiment()
    test_batch_sentiment()
    test_real_time_data()
    print("\nAll tests completed!") 