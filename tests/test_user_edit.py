from random import choice
import allure
import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.send_requests import SendRequest
from utils.urls import (API_USER_CREATE,
                        API_USER_LOGIN,
                        API_USER_AUTH)


@allure.epic("Successful editing user data test cases")
class TestUserSuccessfulEdit(BaseCase):
    params_to_edit = ["firstName", "lastName", "username"]
    credentials_to_edit = ["email", "password"]

    def setup(self):
        # Register new user
        self.register_data = self.prepare_registration_data()
        response_1 = SendRequest.post(API_USER_CREATE, data=self.register_data)

        Assertions.assert_status_code(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

        self.email = self.register_data["email"]
        self.password = self.register_data["password"]
        self.created_user_id = int(self.get_json_value(response_1, "id"))  # Bug: POST /api/user returns "id" as str

        # Login registered user
        self.login_data = {
            "email": self.email,
            "password": self.password
        }
        response_2 = SendRequest.post(API_USER_LOGIN, data=self.login_data)
        self.auth_sid_cookie = self.get_cookie(response_2, "auth_sid")
        self.csrf_token_header = self.get_header(response_2, "x-csrf-token")

        self.api_update_user = f"{API_USER_CREATE}/{self.created_user_id}"

    @allure.description(f"Tests if authorized user can successfully edit his personal data: {params_to_edit}")
    @pytest.mark.parametrize("param_to_edit", params_to_edit)
    def test_edit_created_user_personal_data(self, param_to_edit):
        # Edit created user's data
        if param_to_edit == "firstName":
            new_param_value = "New first name"

        elif param_to_edit == "lastName":
            new_param_value = "New last name"

        else:
            new_param_value = "New username"

        response = SendRequest.put(
            self.api_update_user,
            cookies={"auth_sid": self.auth_sid_cookie},
            headers={"x-csrf-token": self.csrf_token_header},
            data={param_to_edit: new_param_value}
        )
        Assertions.assert_status_code(response, 200)

        # Check changed data
        response_1 = SendRequest.get(
            self.api_update_user,
            cookies={"auth_sid": self.auth_sid_cookie},
            headers={"x-csrf-token": self.csrf_token_header}
        )
        Assertions.assert_json_value_by_key(
            response_1,
            param_to_edit,
            new_param_value
        )

    @allure.description("Tests if authorized user can edit his email and password and log in with new creds")
    @pytest.mark.parametrize("credential_to_edit", credentials_to_edit)
    def test_edit_created_user_credentials_and_login(self, credential_to_edit):
        error_message = "Invalid username/password supplied"
        if credential_to_edit == "email":
            new_valid_credential_value = self.prepare_registration_data()["email"]
        else:
            new_valid_credential_value = self.random_sting()

        response = SendRequest.put(
            self.api_update_user,
            cookies={"auth_sid": self.auth_sid_cookie},
            headers={"x-csrf-token": self.csrf_token_header},
            data={credential_to_edit: new_valid_credential_value}
        )
        Assertions.assert_status_code(response, 200)

        # Check changed data (with token/cookie received by old email) if email was changed
        if credential_to_edit == "email":
            response_1 = SendRequest.get(
                self.api_update_user,
                cookies={"auth_sid": self.auth_sid_cookie},
                headers={"x-csrf-token": self.csrf_token_header}
            )
            Assertions.assert_json_value_by_key(
                response_1,
                credential_to_edit,
                new_valid_credential_value
            )

        # Verify user can't login with old credentials
        response_2 = SendRequest.post(API_USER_LOGIN, data=self.login_data)

        Assertions.assert_status_code(response_2, 400)
        Assertions.assert_response_text(response_2, error_message)

        # Verify user can login with new credentials
        self.login_data[credential_to_edit] = new_valid_credential_value

        response_3 = SendRequest.post(API_USER_LOGIN, data=self.login_data)

        Assertions.assert_status_code(response_3, 200)
        Assertions.assert_json_value_by_key(response_3, "user_id", self.created_user_id)
        new_auth_sid_cookie = self.get_cookie(response_3, "auth_sid")
        new_csrf_token_header = self.get_header(response_3, "x-csrf-token")

        # Check if user is authorized after login with new credentials
        response_4 = SendRequest.get(
            API_USER_AUTH,
            cookies={"auth_sid": new_auth_sid_cookie},
            headers={"x-csrf-token": new_csrf_token_header}
        )

        Assertions.assert_json_value_by_key(response_4, "user_id", self.created_user_id)


class TestUserUnsuccessfulEdit(BaseCase):
    condition = ["no_token", "no_cookie"]
    params_to_edit = ["firstName", "lastName", "username", "email", "password"]
    invalid_value_types = ["empty_value", "too_long_value"]
    max_length = 250

    def setup(self):
        # Register new user
        self.register_data = self.prepare_registration_data()
        response_1 = SendRequest.post(API_USER_CREATE, data=self.register_data)

        Assertions.assert_status_code(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

        self.email = self.register_data["email"]
        self.password = self.register_data["password"]
        self.created_user_id = int(self.get_json_value(response_1, "id"))

        # Login registered user
        self.login_data = {
            "email": self.email,
            "password": self.password
        }
        response_2 = SendRequest.post(API_USER_LOGIN, data=self.login_data)
        self.auth_sid_cookie = self.get_cookie(response_2, "auth_sid")
        self.csrf_token_header = self.get_header(response_2, "x-csrf-token")

        self.api_update_user = f"{API_USER_CREATE}/{self.created_user_id}"

    @allure.description("Tests if user is unable to edit his data if he is unauthorized "
                        "(cookie or auth token is missing)")
    @pytest.mark.parametrize("condition", condition)
    @pytest.mark.parametrize("random_param", [choice(params_to_edit)])
    def test_edit_created_user_data_as_unauthorized_user(self, condition, random_param):
        # Edit random parameter of user data without token and cookie separately
        new_param_value = self.prepare_registration_data()[random_param]
        old_param_value = self.register_data[random_param]
        error_message = "Auth token not supplied"

        if condition == "no_token":
            response_3 = SendRequest.put(
                self.api_update_user,
                cookies={"auth_sid": self.auth_sid_cookie},
                data={random_param: new_param_value}
            )
            Assertions.assert_status_code(response_3, 400)
            Assertions.assert_response_text(response_3, error_message)

        else:
            response_3 = SendRequest.put(
                self.api_update_user,
                headers={"x-csrf-token": self.csrf_token_header},
                data={random_param: new_param_value}
            )
            Assertions.assert_status_code(response_3, 400)
            Assertions.assert_response_text(response_3, error_message)

        # Check that the parameter is not changed
        response_4 = SendRequest.get(
            self.api_update_user,
            cookies={"auth_sid": self.auth_sid_cookie},
            headers={"x-csrf-token": self.csrf_token_header}
        )
        Assertions.assert_json_value_by_key(
            response_4,
            random_param,
            old_param_value
        )

    @allure.description("Tests if user is unable to edit his data if he passes empty or too long value")
    @pytest.mark.parametrize("param_to_edit", params_to_edit)
    @pytest.mark.parametrize("invalid_value_type", invalid_value_types)
    def test_edit_created_user_data_with_invalid_values(self, param_to_edit, invalid_value_type):
        # Edit parameter of user data and replace it with empty/too long value
        old_param_value = self.register_data[param_to_edit]
        if invalid_value_type == "empty_value":
            new_param_value = ""
            error_message = f"Too short value for field {param_to_edit}"
        else:
            new_param_value = self.random_sting(length=self.max_length + 1)
            error_message = f"Too long value for field {param_to_edit}"

        response_1 = SendRequest.put(
            self.api_update_user,
            cookies={"auth_sid": self.auth_sid_cookie},
            headers={"x-csrf-token": self.csrf_token_header},
            data={param_to_edit: new_param_value}
        )

        Assertions.assert_status_code(response_1, 400)

        if param_to_edit == "email":
            Assertions.assert_response_text(response_1, expected_text="Invalid email format")
        else:
            Assertions.assert_json_value_by_key(response_1, "error", error_message)

        # If password is changed, check that user can successfully login with the old one
        # Else, get user data and verify the parameter wasn't changed
        if param_to_edit == "password":
            response_2 = SendRequest.post(API_USER_LOGIN, data=self.login_data)

            Assertions.assert_status_code(response_2, 200)
            Assertions.assert_json_value_by_key(response_2, "user_id", self.created_user_id)

        else:
            response_2 = SendRequest.get(
                self.api_update_user,
                cookies={"auth_sid": self.auth_sid_cookie},
                headers={"x-csrf-token": self.csrf_token_header}
            )

            Assertions.assert_json_value_by_key(
                response_2,
                param_to_edit,
                old_param_value
            )
