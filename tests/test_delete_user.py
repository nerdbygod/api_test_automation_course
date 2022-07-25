import allure
from lib.send_requests import SendRequest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from utils.urls import API_USER_LOGIN, API_USER_CREATE
from utils.data_for_tests import (test_user_for_creation_data,
                                  test_user_credentials,
                                  test_user_authorized_data,
                                  test_user_id)


class TestSuccessfulUserDeletion(BaseCase):
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

    @allure.description("Test if it's possible to create user and delete it")
    def test_delete_created_user(self):
        response = SendRequest.delete(
            self.api_update_user,
            cookies={"auth_sid": self.auth_sid_cookie},
            headers={"x-csrf-token": self.csrf_token_header}
        )
        Assertions.assert_status_code(response, 200)

        # Attempt to get user data by id and make sure it's not found
        response_1 = SendRequest.get(
            self.api_update_user,
            cookies={"auth_sid": self.auth_sid_cookie},
            headers={"x-csrf-token": self.csrf_token_header}
        )
        Assertions.assert_status_code(response_1, 404)
        Assertions.assert_response_text(response_1, "User not found")

        # Attempt to login as deleted user
        response_2 = SendRequest.post(API_USER_LOGIN, data=self.login_data)
        Assertions.assert_status_code(response_2, 400)
        Assertions.assert_response_text(response_2, "Invalid username/password supplied")


class TestUnsuccessfulUserDeletion(BaseCase):
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

    @allure.description("Tests if it's not possible to delete undeletable user")
    def test_delete_undeletable_user(self):
        # Login as undeletable user
        undeletable_user_login_data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        undeletable_user_id = 2

        login_as_undeletable_user_response = SendRequest.post(
            API_USER_LOGIN,
            data=undeletable_user_login_data
        )
        Assertions.assert_status_code(login_as_undeletable_user_response, 200)
        Assertions.assert_json_value_by_key(
            login_as_undeletable_user_response,
            "user_id",
            undeletable_user_id
        )
        undeletable_user_auth_cookie = self.get_cookie(
            login_as_undeletable_user_response,
            "auth_sid")
        undeletable_user_csrf_token = self.get_header(
            login_as_undeletable_user_response,
            "x-csrf-token"
        )

        # Attempt to delete undeletable user
        error_message = "Please, do not delete test users with ID 1, 2, 3, 4 or 5."
        api_delete_user = f"{API_USER_CREATE}/{undeletable_user_id}"
        delete_response = SendRequest.delete(
            api_delete_user,
            cookies={"auth_sid": undeletable_user_auth_cookie},
            headers={"x-csrf-token": undeletable_user_csrf_token}
        )
        Assertions.assert_status_code(delete_response, 400)
        Assertions.assert_response_text(delete_response, error_message)

        # Get user data to make sure it's still there
        expected_params = ("id", "username", "email", "firstName", "lastName")
        get_data_response = SendRequest.get(
            api_delete_user,
            cookies={"auth_sid": undeletable_user_auth_cookie},
            headers={"x-csrf-token": undeletable_user_csrf_token}
        )
        Assertions.assert_json_has_keys(get_data_response, *expected_params)
        Assertions.assert_json_value_by_key(get_data_response, "username", "Vitaliy")
        Assertions.assert_json_value_by_key(get_data_response, "email", "vinkotov@example.com")

        # Login to make sure user is not deleted
        login_after_delete_attempt_response = SendRequest.post(
            API_USER_LOGIN,
            data=undeletable_user_login_data
        )
        Assertions.assert_status_code(login_after_delete_attempt_response, 200)
        Assertions.assert_json_value_by_key(
            login_as_undeletable_user_response,
            "user_id",
            undeletable_user_id
        )

    # @pytest.mark.xfail
    @allure.description("Tests if authorized user can't delete another user")
    def test_delete_created_user_authorized_as_different_user(self):
        # Login as test user
        api_test_user = f"{API_USER_CREATE}/{test_user_id}"

        error_message = "Auth token not supplied"
        # Attempt to delete test user authorized as created user
        delete_test_user_data_response = SendRequest.delete(
            api_test_user,
            cookies={"auth_sid": self.auth_sid_cookie},
            headers={"x-csrf-token": self.csrf_token_header},
        )

        # Check status code and error message
        # Assertions.assert_status_code(delete_test_user_data_response, 400)
        # Assertions.assert_response_text(delete_test_user_data_response, error_message)

        # Check that test user can login
        test_user_login_response_after_deletion_attempt = SendRequest.post(
            API_USER_LOGIN,
            data=test_user_credentials
        )
        Assertions.assert_status_code(test_user_login_response_after_deletion_attempt, 200)
        Assertions.assert_json_value_by_key(
            test_user_login_response_after_deletion_attempt,
            "user_id",
            test_user_id
        )
        test_user_auth_cookie = self.get_cookie(test_user_login_response_after_deletion_attempt, "auth_sid")
        test_user_csrf_token = self.get_header(test_user_login_response_after_deletion_attempt, "x-csrf-token")

        # Check that test user's data hasn't been deleted
        # the test fails here, but it shouldn't. Needs to be refactored
        get_test_user_data_response = SendRequest.get(
            self.api_update_user,
            cookies={"auth_sid": test_user_auth_cookie},
            headers={"x-csrf-token": test_user_csrf_token}
        )
        Assertions.assert_status_code(get_test_user_data_response, 200)
        Assertions.assert_equal_json_objects(get_test_user_data_response, test_user_authorized_data)

        # Check that created user can login
        created_user_login_response_after_deletion_attempt = SendRequest.post(
            API_USER_LOGIN,
            data=self.register_data
        )
        auth_sid_cookie = self.get_cookie(
            created_user_login_response_after_deletion_attempt,
            "auth_sid"
        )
        csrf_token_header = self.get_header(
            created_user_login_response_after_deletion_attempt,
            "x-csrf-token"
        )

        # Check that created user data hasn't been deleted
        get_created_user_data_response = SendRequest.get(
            self.api_update_user,
            cookies={"auth_sid": auth_sid_cookie},
            headers={"x-csrf-token": csrf_token_header}
        )
        Assertions.assert_status_code(get_created_user_data_response, 200)
        Assertions.assert_json_value_by_key(
            get_created_user_data_response,
            "username",
            self.register_data["username"]
        )
        Assertions.assert_json_value_by_key(
            get_created_user_data_response,
            "email",
            self.register_data["email"]
        )