import requests

BASE_URL = 'https://playground.learnqa.ru/'
API_GET_TEXT = 'api/get_text'
API_HELLO = 'api/hello'

response = requests.get(BASE_URL + API_HELLO)
print(response.text)

response2 = requests.get(BASE_URL + API_GET_TEXT)
print(response2.text)
