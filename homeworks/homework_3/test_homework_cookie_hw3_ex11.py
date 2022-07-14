import requests
from urls import API_HOMEWORK_COOKIE


class TestHomeworkCookie:
    def test_cookie_value(self):
        response = requests.get(API_HOMEWORK_COOKIE)
        response_cookie = response.cookies.get_dict()
        print(f"Response cookie: {response_cookie}")

        assert "HomeWork" in response_cookie, "No 'HomeWork' cookie in response"

        expected_cookie_value = "hw_value"
        actual_cookie_value = response_cookie["HomeWork"]

        assert actual_cookie_value == expected_cookie_value, f"Actual cookie value: {actual_cookie_value}" \
                                                             f"should equal to {expected_cookie_value}"
