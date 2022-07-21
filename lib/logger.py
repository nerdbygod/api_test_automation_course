import datetime
import os
from requests import Response


class Logger:
    current_dir = os.getcwd()
    logs_dir = f"{current_dir}/logs"
    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)
    file_name = f"{logs_dir}/log_" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".log"

    @classmethod
    def _write_to_log_file(cls, data: str):
        with open(cls.file_name, "a", encoding="utf-8") as logger_file:
            logger_file.write(data)

    @classmethod
    def add_request(cls, method: str, url: str, data: dict, headers: dict, cookies: dict):
        test_name = os.environ.get("PYTEST_CURRENT_TEST")

        data_to_add = f"\n-----\n"
        data_to_add += f"Test: {test_name}\n"
        data_to_add += f"Time: {str(datetime.datetime.now())}\n"
        data_to_add += f"Request method: {method}\n"
        data_to_add += f"Request URL: {url}\n"
        data_to_add += f"Request data: {data}\n"
        data_to_add += f"Request headers: {headers}\n"
        data_to_add += f"Request cookies: {cookies}\n"
        data_to_add += "\n"

        cls._write_to_log_file(data_to_add)

    @classmethod
    def add_response(cls, response: Response):
        cookies = dict(response.cookies)
        headers = dict(response.headers)

        data_to_add = f"Response code: {response.status_code}\n"
        data_to_add += f"Response text: {response.text}\n"
        data_to_add += f"Response headers {headers}\n"
        data_to_add += f"Response cookies {cookies}\n"
        data_to_add += "\n-----\n"

        cls._write_to_log_file(data_to_add)
