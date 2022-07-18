import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from utils.data_for_tests import *
from urls import API_USER_CREATE


class TestUserRegistration(BaseCase):
    def test_user_registration_with_valid_data(self):
        response = requests.post(API_USER_CREATE, data=random_user)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_user_creation_with_existing_email(self):
        existing_email = test_user['email']
        response = requests.post(API_USER_CREATE, data=test_user)

        Assertions.assert_status_code(response, 400)
        api_error_text = f"Users with email '{existing_email}' already exists"
        assert response.text == api_error_text, f"Unexpected response: {response.text}"
