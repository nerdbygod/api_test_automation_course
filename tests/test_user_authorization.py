import pytest
from utils.urls import API_USER_LOGIN, API_USER_AUTH
from utils.data_for_tests import test_user_credentials
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.send_requests import SendRequest


class TestUserAuthorization(BaseCase):
    condition = ["no_token", "no_cookie"]

    def setup(self):
        login_response = SendRequest.post(API_USER_LOGIN, data=test_user_credentials)

        self.auth_sid_cookie = self.get_cookie(login_response, "auth_sid")
        self.csrf_token_header = self.get_header(login_response, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(login_response, "user_id")

    def test_successful_user_authorization(self):
        response = SendRequest.get(
            API_USER_AUTH,
            cookies={"auth_sid": self.auth_sid_cookie},
            headers={"x-csrf-token": self.csrf_token_header},
        )

        Assertions.assert_json_value_by_key(
            response,
            "user_id",
            self.user_id_from_auth_method
        )

    @pytest.mark.parametrize("condition", condition)
    def test_authorization_without_headers(self, condition):
        expected_id_value = 0
        if condition == "no_token":
            response = SendRequest.get(
                API_USER_AUTH,
                cookies={"auth_sid": self.auth_sid_cookie},
            )

            Assertions.assert_json_value_by_key(
                response,
                "user_id",
                expected_id_value
            )
        else:
            response = SendRequest.get(
                API_USER_AUTH,
                headers={"x-csrf-token": self.csrf_token_header}
            )

            Assertions.assert_json_value_by_key(
                response,
                "user_id",
                expected_id_value
            )
