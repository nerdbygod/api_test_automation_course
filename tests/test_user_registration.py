import pytest
import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from utils.data_for_tests import test_user_for_creation_data
from utils.urls import API_USER_CREATE
from lib.send_requests import SendRequest


@allure.epic("User registration test cases")
class TestUserRegistration(BaseCase):
    params_to_send = ["email", "password", "username", "firstName", "lastName"]
    max_length = 250

    def setup(self):
        self.user_data = self.prepare_registration_data()

    @allure.description("Tests if user can register with valid credentials")
    def test_user_registration_with_valid_data(self):
        response = SendRequest.post(API_USER_CREATE, data=self.user_data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("Tests if user is unable to register with existing email")
    def test_user_creation_with_existing_email(self):
        existing_email = test_user_for_creation_data['email']
        error_message = f"Users with email '{existing_email}' already exists"

        response = SendRequest.post(API_USER_CREATE, data=test_user_for_creation_data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_text(response, error_message)

    @allure.description("Tests if user is unable to register if one parameter is missing in request body")
    @pytest.mark.parametrize("param_to_send", params_to_send)
    def test_user_creation_without_required_params(self, param_to_send):
        self.user_data.pop(param_to_send)
        error_message = f"The following required params are missed: {param_to_send}"

        response = SendRequest.post(API_USER_CREATE, data=self.user_data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_text(response, error_message)

    @allure.description("Tests if user is unable to register if one parameter is empty")
    @pytest.mark.parametrize("invalid_param", params_to_send)
    def test_user_creation_with_empty_params(self, invalid_param):
        self.user_data.update({invalid_param: ""})
        error_message = f"The value of '{invalid_param}' field is too short"

        response = SendRequest.post(API_USER_CREATE, data=self.user_data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_text(response, error_message)

    @allure.description("Tests if user is unable to register if one parameter exceeds max length")
    @pytest.mark.parametrize("too_long_param", params_to_send)
    def test_user_creation_with_too_long_params(self, too_long_param):
        self.user_data.update(
            {
                too_long_param: self.random_sting(length=self.max_length + 1)
            }
        )
        error_message = f"The value of '{too_long_param}' field is too long"

        response = SendRequest.post(API_USER_CREATE, data=self.user_data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_text(response, error_message)

    @allure.description("Tests if user us unable to register if '@' is missing in email parameter")
    def test_user_creation_with_invalid_email(self):
        self.user_data["email"] = self.user_data["email"].replace("@", '')
        error_message = "Invalid email format"

        response = SendRequest.post(API_USER_CREATE, data=self.user_data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_text(response, error_message)
