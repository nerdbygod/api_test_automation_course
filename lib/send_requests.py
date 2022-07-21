import requests
from .logger import Logger


class SendRequest:
    @staticmethod
    def post(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return SendRequest._send("POST", url, data, headers, cookies)

    @staticmethod
    def get(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return SendRequest._send("GET", url, data, headers, cookies)

    @staticmethod
    def put(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return SendRequest._send("PUT", url, data, headers, cookies)

    @staticmethod
    def delete(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return SendRequest._send("DELETE", url, data, headers, cookies)

    @staticmethod
    def _send(method: str,
              url: str,
              data: dict,
              headers: dict,
              cookies: dict):

        url = f"https://playground.learnqa.ru/api{url}"

        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        Logger.add_request(method, url, data, headers, cookies)

        response = requests.request(method=method,
                                    url=url,
                                    data=data,
                                    headers=headers,
                                    cookies=cookies)

        Logger.add_response(response)

        return response
