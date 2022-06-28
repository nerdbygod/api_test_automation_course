import requests

BASE_URL = 'https://playground.learnqa.ru/'
API_GET_TEXT = BASE_URL + 'api/get_text'
API_HELLO = BASE_URL + 'api/hello'

payload = {"name": "Pavel"}

response = requests.get(API_HELLO, params=payload)
print(response.text)

response2 = requests.get(API_GET_TEXT)
print(response2.text)
