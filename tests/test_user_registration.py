import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from utils.data_for_tests import test_user_for_creation_data
from utils.urls import API_USER_CREATE
from lib.send_requests import SendRequest


class TestUserRegistration(BaseCase):
    params_to_send = ["email", "password", "username", "firstName", "lastName"]
    max_length = 250

    def setup(self):
        self.user_data = self.prepare_registration_data()

    def test_user_registration_with_valid_data(self):
        response = SendRequest.post(API_USER_CREATE, data=self.user_data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_user_creation_with_existing_email(self):
        existing_email = test_user_for_creation_data['email']

        response = SendRequest.post(API_USER_CREATE, data=test_user_for_creation_data)

        Assertions.assert_status_code(response, 400)
        api_error_text = f"Users with email '{existing_email}' already exists"
        assert response.text == api_error_text, f"Unexpected response: {response.text}"

    @pytest.mark.parametrize("param_to_send", params_to_send)
    def test_user_creation_without_required_params(self, param_to_send):
        self.user_data.pop(param_to_send)
        error_message = f"The following required params are missed: {param_to_send}"

        response = SendRequest.post(API_USER_CREATE, data=self.user_data)

        Assertions.assert_status_code(response, 400)
        assert response.text == error_message, f"Included param is '{param_to_send}', " \
                                               f"error message should be {error_message}"

    @pytest.mark.parametrize("invalid_param", params_to_send)
    def test_user_creation_with_empty_params(self, invalid_param):
        self.user_data.update({invalid_param: ""})
        error_message = f"The value of '{invalid_param}' field is too short"

        response = SendRequest.post(API_USER_CREATE, data=self.user_data)

        Assertions.assert_status_code(response, 400)
        assert response.text == error_message, f"Invalid param is '{invalid_param}', " \
                                               f"error message should be '{error_message}'"

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
        assert response.text == error_message, f"Invalid param is '{too_long_param}', " \
                                               f"error message should be '{error_message}', but " \
                                               f"'{response.text}' is returned"

    # To-do: add test to check invalid email less than max_length
