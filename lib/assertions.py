from json.decoder import JSONDecodeError
from requests import Response


class Assertions:
    @staticmethod
    def assert_json_has_key(response: Response, key):
        try:
            response_obj = response.json()
            assert key in response_obj, f"Response for '{response.url}' doesn't have expected key '{key}'"
        except JSONDecodeError:
            raise AssertionError(f"Response for {response.url} is not in JSON format. "
                                 f"Response text is {response.text}") from None

    @staticmethod
    def assert_json_has_keys(response: Response, *args):
        try:
            response_obj = response.json()
            for key in args:
                assert key in response_obj, f"Response for '{response.url}' doesn't have expected key '{key}'"
        except JSONDecodeError:
            raise AssertionError(f"Response for {response.url} is not in JSON format. "
                                 f"Response text is {response.text}") from None

    @staticmethod
    def assert_json_has_not_keys(response: Response, *args):
        try:
            response_obj = response.json()
            for key in args:
                assert key not in response_obj, f"Response for '{response.url}' has unexpected key '{key}'"
        except JSONDecodeError:
            raise AssertionError(f"Response for '{response.url}' is not in JSON format. "
                                 f"Response text is {response.text}") from None

    @staticmethod
    def assert_json_value_by_key(response: Response, key, expected_value):
        Assertions.assert_json_has_key(response, key)
        actual_value = response.json()[key]
        assert actual_value == expected_value, \
            f"Unexpected '{key}' value: '{actual_value}' should be '{expected_value}'"

    @staticmethod
    def assert_equal_json_objects(response: Response, expected_result: dict):
        try:
            assert response.json() == expected_result, "JSON objects are not equal!"
        except JSONDecodeError:
            raise AssertionError(f"Response for {response.url} is not in JSON format. "
                                 f"Response text is {response.text}") from None

    @staticmethod
    def assert_status_code(response: Response, expected_code: int):
        actual_code = response.status_code
        assert actual_code == expected_code, f"Response status code for '{response.url}' " \
                                             f"is '{actual_code}', should be '{expected_code}'"

    @staticmethod
    def assert_different_json_values_by_key(response: Response, key, expected_value):
        Assertions.assert_json_has_key(response, key)
        actual_value = response.json()[key]
        assert actual_value != expected_value, \
            f"Unexpected equal '{key}' values: '{actual_value}' should not be '{expected_value}'"
