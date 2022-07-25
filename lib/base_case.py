from requests import Response
from lib.assertions import Assertions
from faker import Faker
from random import randint
from lib.send_requests import SendRequest
from utils.urls import API_USER_LOGIN, API_USER_CREATE


class BaseCase:
    def get_cookie(
            self,
            response: Response,
            cookie_name: str
    ):
        assert cookie_name in response.cookies, f"Cannot find {cookie_name} in response for {response.url}"
        return response.cookies[cookie_name]

    def get_header(
            self,
            response: Response,
            header_name: str
    ):
        assert header_name in response.headers, f"Cannot find {header_name} in response for {response.url}"
        return response.headers[header_name]

    def get_json_value(
            self,
            response: Response,
            key: int | str
    ):
        Assertions.assert_json_has_key(response, key)
        return response.json()[key]

    def prepare_registration_data(self, password_length=7) -> dict:
        fake = Faker()
        test_user_data = {
            "username": fake.user_name(),
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "email": fake.email(),
            "password": fake.pystr(password_length, password_length)
        }
        return test_user_data

    def create_user(self):
        register_data = self.prepare_registration_data()
        response_1 = SendRequest.post(API_USER_CREATE, data=register_data)

        Assertions.assert_status_code(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

        email = register_data["email"]
        password = register_data["password"]
        created_user_id = int(self.get_json_value(response_1, "id"))

        # Login registered user
        login_data = {
            "email": email,
            "password": password
        }
        response_2 = SendRequest.post(API_USER_LOGIN, data=login_data)
        auth_sid_cookie = self.get_cookie(response_2, "auth_sid")
        csrf_token_header = self.get_header(response_2, "x-csrf-token")

        api_update_user = f"{API_USER_CREATE}/{created_user_id}"

        return {
            "register_data": register_data,
            "login_data": login_data,
            "cookie": auth_sid_cookie,
            "header": csrf_token_header,
            "api_update_user": api_update_user,
            "user_id": created_user_id
        }

    def delete_user(self, user_id: int, auth_sid_cookie: str, csrf_token: str, login_data: dict):
        api_user_delete = f"{API_USER_CREATE}/{user_id}"
        response = SendRequest.delete(
            api_user_delete,
            cookies={"auth_sid": auth_sid_cookie},
            headers={"x-csrf-token": csrf_token}
        )

        Assertions.assert_status_code(response, 200)

        response_2 = SendRequest.post(API_USER_LOGIN, data=login_data)

        Assertions.assert_status_code(response_2, 400)
        Assertions.assert_response_text(response_2, "Invalid username/password supplied")

    def random_sting(self, length=7):
        fake = Faker()
        return fake.pystr(length, length)

    def random_int(self, length=6):
        return int(''.join([str(randint(1, 9)) for _ in range(length)]))
