import requests
import pytest
from urls import API_USER_LOGIN, API_USER_AUTH
from utils.data_for_tests import test_user_credentials
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserAuthorization(BaseCase):
    condition = ["no_token", "no_cookie"]

    def setup(self):
        response1 = requests.post(API_USER_LOGIN, data=test_user_credentials)

        self.auth_sid_cookie = self.get_cookie(response1, "auth_sid")
        self.csrf_token_header = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    def test_successful_user_authorization(self):
        response2 = requests.get(
            API_USER_AUTH,
            cookies={"auth_sid": self.auth_sid_cookie},
            headers={"x-csrf-token": self.csrf_token_header},
        )

        Assertions.assert_json_value_by_key(
            response2,
            "user_id",
            self.user_id_from_auth_method
        )

    @pytest.mark.parametrize("condition", condition)
    def test_authorization_without_headers(self, condition):
        expected_id_value = 0
        if condition == "no_token":
            response3 = requests.get(
                API_USER_AUTH,
                cookies={"auth_sid": self.auth_sid_cookie},
            )

            Assertions.assert_json_value_by_key(
                response3,
                "user_id",
                expected_id_value
            )
        else:
            response4 = requests.get(
                API_USER_AUTH,
                headers={"x-csrf-token": self.csrf_token_header}
            )

            Assertions.assert_json_value_by_key(
                response4,
                "user_id",
                expected_id_value
            )
