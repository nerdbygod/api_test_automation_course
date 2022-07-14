import requests
import urls

response = requests.get(urls.API_LONG_REDIRECT, allow_redirects=True)
history = response.history
print(f"Number of redirects: {len(history)}, final url: {history[-1].url}")
