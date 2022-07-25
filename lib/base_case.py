from requests import Response
from lib.assertions import Assertions
from faker import Faker
from random import randint


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

    def random_sting(self, length=7):
        fake = Faker()
        return fake.pystr(length, length)

    def random_int(self, length=6):
        return int(''.join([str(randint(1, 9)) for _ in range(length)]))
