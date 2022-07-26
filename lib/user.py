from faker import Faker
from lib.base_case import BaseCase
from lib.send_requests import SendRequest
from lib.assertions import Assertions
from utils.urls import API_USER_LOGIN, API_USER_CREATE


class User:
    def __init__(self, password_length):
        # Prepare registration data
        fake = Faker()
        self.user_data = {
            "username": fake.user_name(),
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "email": fake.email(),
            "password": fake.pystr(password_length, password_length)
        }

        # Create a new user
        response = SendRequest.post(API_USER_CREATE, data=self.user_data)
        # Check if user with generated fake email already exists and repeat creation with new email
        if response.text == f"Users with email '{self.user_data['email']}' already exists":
            self.user_data["email"] = fake.email()
            response = SendRequest.post(API_USER_CREATE, data=self.user_data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

        self.username = self.user_data["username"]
        self.email = self.user_data["email"]
        self.firstName = self.user_data["firstName"]
        self.lastName = self.user_data["lastName"]
        self.password = self.user_data["password"]
        self.id = int(BaseCase.get_json_value(response, "id"))
        self.api_user = f"{API_USER_CREATE}/{self.id}"

        self.login_data = {
            "email": self.email,
            "password": self.password
        }

        response_2 = SendRequest.post(API_USER_LOGIN, data=self.login_data)
        self.auth_sid_cookie = BaseCase.get_cookie(response_2, "auth_sid")
        self.csrf_token_header = BaseCase.get_header(response_2, "x-csrf-token")

    def delete_user(self):
        response = SendRequest.delete(
            self.api_user,
            cookies={"auth_sid": self.auth_sid_cookie},
            headers={"x-csrf-token": self.csrf_token_header}
        )

        Assertions.assert_status_code(response, 200)

        response_2 = SendRequest.post(API_USER_LOGIN, data=self.login_data)

        Assertions.assert_status_code(response_2, 400)
        Assertions.assert_response_text(response_2, "Invalid username/password supplied")

        response_3 = SendRequest.get(self.api_user)

        Assertions.assert_status_code(response_3, 404)
        Assertions.assert_response_text(response_3, "User not found")
