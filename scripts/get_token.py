import requests

def get_token():
    url = "http://localhost:8000/token"
    data = {
        "username": "testuser",
        "password": "testpass"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        print("Token received successfully:")
        print(response.json())
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"Error getting token: {e}")
        return None

if __name__ == "__main__":
    get_token() 