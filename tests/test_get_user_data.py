from lib.base_case import BaseCase
from lib.assertions import Assertions
from utils.urls import API_USER_CREATE, API_USER_LOGIN
from utils.data_for_tests import test_user_authorized_data, test_user_credentials
from random import randint
from lib.send_requests import SendRequest


class TestGetUserData(BaseCase):
    def setup(self):
        self.test_user_id = test_user_authorized_data["id"]
        self.expected_user_name = test_user_authorized_data["username"]

        response = SendRequest.post(API_USER_LOGIN, data=test_user_credentials)

        self.auth_sid_cookie = self.get_cookie(response, "auth_sid")
        self.csrf_token_header = self.get_header(response, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response, "user_id")

        self.api_user_id = f"{API_USER_CREATE}/{self.user_id_from_auth_method}"

        self.unexpected_keys = ("id", "email", "firstName", "lastName")

    def test_get_user_data_unauthorized(self):
        response = SendRequest.get(self.api_user_id)

        Assertions.assert_json_value_by_key(
            response,
            "username",
            self.expected_user_name
        )
        Assertions.assert_json_has_not_keys(response, *self.unexpected_keys)
        Assertions.assert_json_value_by_key(response, "username", self.expected_user_name)

    def test_get_user_data_authorized_as_same_user(self):
        response = SendRequest.get(
            self.api_user_id,
            cookies={"auth_sid": self.auth_sid_cookie},
            headers={"x-csrf-token": self.csrf_token_header}
        )

        expected_keys = ("id", "email", "firstName", "lastName", "username")
        Assertions.assert_json_has_keys(response, *expected_keys)
        Assertions.assert_equal_json_objects(response, test_user_authorized_data)

    def test_get_user_data_authorized_as_different_user(self):
        api_user_id = f"{API_USER_CREATE}/1"
        response = SendRequest.get(
            api_user_id,
            cookies={"auth_sid": self.auth_sid_cookie},
            headers={"x-csrf-token": self.csrf_token_header}
        )

        Assertions.assert_json_has_not_keys(response, *self.unexpected_keys)
        Assertions.assert_different_json_values_by_key(response, "username", self.expected_user_name)

    def test_get_unexisting_user_data_unauthorized(self):
        unexisting_user_id = randint(400_000, 500_000)
        api_user_id = f"{API_USER_CREATE}/{unexisting_user_id}"
        response = SendRequest.get(api_user_id)

        assert response.text == "User not found", f"'user_id': {unexisting_user_id} should be unexisting"
