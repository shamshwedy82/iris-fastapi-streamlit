import requests


BASE_URL = "http://127.0.0.1:8000"

payload = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2,
}

response = requests.post(f"{BASE_URL}/predict", json=payload)

print("Status Code:", response.status_code)
print("Response:", response.json())
