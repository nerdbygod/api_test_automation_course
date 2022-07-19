import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from utils.data_for_tests import test_user_for_creation_data
from urls import API_USER_CREATE
from faker import Faker


class TestUserRegistration(BaseCase):
    params_to_send = ["email", "password", "username", "firstName", "lastName"]

    def setup(self):
        fake = Faker()

        self.user_data = {"username": fake.user_name(),
                          "firstName": fake.first_name(),
                          "lastName": fake.last_name(),
                          "email": fake.email(),
                          "password": fake.pystr(5, 5)
                          }

    def test_user_registration_with_valid_data(self):
        response = requests.post(API_USER_CREATE, data=self.user_data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_user_creation_with_existing_email(self):
        existing_email = test_user_for_creation_data['email']
        response = requests.post(API_USER_CREATE, data=test_user_for_creation_data)

        Assertions.assert_status_code(response, 400)
        api_error_text = f"Users with email '{existing_email}' already exists"
        assert response.text == api_error_text, f"Unexpected response: {response.text}"

    @pytest.mark.parametrize("param_to_send", params_to_send)
    def test_user_creation_without_required_params(self, param_to_send):
        error_message = f"The following required params are missed: {param_to_send}"
        self.user_data.pop(param_to_send)
        response = requests.post(API_USER_CREATE, data=self.user_data)

        Assertions.assert_status_code(response, 400)
        assert response.text == error_message, f"Included param is {param_to_send}, " \
                                               f"error message should be {error_message}"
