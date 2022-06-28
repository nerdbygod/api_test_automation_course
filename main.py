import requests

BASE_URL = "https://playground.learnqa.ru/"
API_GET_TEXT = f"{BASE_URL}api/get_text"
API_HELLO = f"{BASE_URL}api/hello"

payload = {"name": "Peter"}

response = requests.get(API_HELLO, params=payload)
print(response.text)

response2 = requests.get(API_GET_TEXT)
print(response2.text)
