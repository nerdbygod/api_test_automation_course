import requests
import urls

payload = {"name": "Peter"}

response = requests.get(urls.API_HELLO, params=payload)
print(response.text)

response2 = requests.get(urls.API_GET_TEXT)
print(response2.text)
