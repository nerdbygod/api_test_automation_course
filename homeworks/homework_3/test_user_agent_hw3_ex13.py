import requests
import pytest
from utils.urls import API_USER_AGENT_CHECK


class TestUserAgent:
    user_agent_list = [
        ("Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) "
         "AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
         {
             'platform': 'Mobile',
             'browser': 'No',
             'device': 'Android'
         }),
        ("Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 "
         "(KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
         {
             'platform': 'Mobile',
             'browser': 'Chrome',
             'device': 'iOS'
         }),
        ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
         {
             'platform': 'Googlebot',
             'browser': 'Unknown',
             'device': 'Unknown'
         }),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
         "(KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
         {
             'platform': 'Web',
             'browser': 'Chrome',
             'device': 'No'
         }),
        (
            "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 "
            "(KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            {
                'platform': 'Mobile',
                'browser': 'No',
                'device': 'iPhone'
            })
    ]

    @pytest.mark.parametrize("user_agent, expected_values", user_agent_list)
    def test_user_agent(self, user_agent, expected_values):
        response = requests.get(API_USER_AGENT_CHECK,
                                headers={"User-Agent": user_agent}).json()

        actual_browser_value = response["browser"]
        actual_device_value = response["device"]
        actual_platform_value = response["platform"]

        expected_browser_value = expected_values["browser"]
        expected_device_value = expected_values["device"]
        expected_platform_value = expected_values["platform"]

        assert actual_browser_value == expected_browser_value, f"Browser version {actual_browser_value} " \
                                                               f"should equal {expected_browser_value}"
        assert actual_device_value == expected_device_value, f"Device {actual_device_value} " \
                                                             f"should equal {expected_device_value}"
        assert actual_platform_value == expected_platform_value, f"Platform {actual_platform_value} " \
                                                                 f"should equal {expected_platform_value}"
