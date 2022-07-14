import requests
from urls import API_HOMEWORK_HEADER


class TestHomeworkHeader:
    def test_header_value(self):
        response = requests.get(API_HOMEWORK_HEADER)
        response_headers = response.headers

        hw_header = "x-secret-homework-header"

        assert hw_header in response_headers, f"{hw_header} is not in response headers"

        expected_hw_header_value = "Some secret value"
        actual_header_value = response_headers.get(hw_header)

        assert actual_header_value == expected_hw_header_value, f"Expected header value is {expected_hw_header_value},"\
                                                                f" actual header value is {actual_header_value}"
