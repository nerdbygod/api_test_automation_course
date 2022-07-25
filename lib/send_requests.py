import requests
import allure
from .logger import Logger
from environment import ENVIRONMENT


class SendRequest:
    # To enable logs, set logging parameter to True
    # This needs to be refactored to one single parameter passed in one function (_send),
    # so that it is not passed every time to each method, or better use it as a pytest fixture or
    # to pytest.ini to be passed as a command line argument
    @staticmethod
    def post(url: str, data: dict = None, headers: dict = None, cookies: dict = None, logging=True):
        with allure.step(f"POST request to URL: '{url}'"):
            return SendRequest._send("POST", url, data, headers, cookies, logging)

    @staticmethod
    def get(url: str, data: dict = None, headers: dict = None, cookies: dict = None, logging=True):
        with allure.step(f"GET request to URL: '{url}'"):
            return SendRequest._send("GET", url, data, headers, cookies, logging)

    @staticmethod
    def put(url: str, data: dict = None, headers: dict = None, cookies: dict = None, logging=True):
        with allure.step(f"PUT request to URL: '{url}'"):
            return SendRequest._send("PUT", url, data, headers, cookies, logging)

    @staticmethod
    def delete(url: str, data: dict = None, headers: dict = None, cookies: dict = None, logging=True):
        with allure.step(f"DELETE request to URL: '{url}'"):
            return SendRequest._send("DELETE", url, data, headers, cookies, logging)

    @staticmethod
    def _send(method: str,
              url: str,
              data: dict,
              headers: dict,
              cookies: dict,
              logging: bool):

        url = f"{ENVIRONMENT.get_base_url()}{url}"

        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        if logging:
            Logger.add_request(method, url, data, headers, cookies)

        response = requests.request(method=method,
                                    url=url,
                                    data=data,
                                    headers=headers,
                                    cookies=cookies)
        if logging:
            Logger.add_response(response)

        return response
