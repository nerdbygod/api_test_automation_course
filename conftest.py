from utils.data_for_tests import (test_user_credentials,
                                  test_user_for_creation_data,
                                  test_user_id,
                                  test_user_authorized_data)
import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.send_requests import SendRequest
from utils.urls import API_USER_LOGIN, API_USER_CREATE


base_case = BaseCase()


@pytest.fixture(scope="function")
def get_test_user_data_to_initial_state():
    ...
    yield

    del test_user_for_creation_data["email"]
    response = SendRequest.post(API_USER_LOGIN, data=test_user_credentials)
    Assertions.assert_status_code(response, 200)
    Assertions.assert_json_value_by_key(response, "user_id", test_user_id)

    auth_sid_cookie = base_case.get_cookie(response, "auth_sid")
    csrf_token = base_case.get_header(response, "x-csrf-token")
    api_update_user = f"{API_USER_CREATE}/{test_user_id}"

    response_2 = SendRequest.put(
        api_update_user,
        cookies={"auth_sid": auth_sid_cookie},
        headers={"x-csrf-token": csrf_token},
        data=test_user_for_creation_data
    )

    Assertions.assert_status_code(response_2, 200)

    response_3 = SendRequest.get(
        api_update_user,
        cookies={"auth_sid": auth_sid_cookie},
        headers={"x-csrf-token": csrf_token}
    )

    Assertions.assert_status_code(response_3, 200)
    Assertions.assert_equal_json_objects(response_3, test_user_authorized_data)
