from json.decoder import JSONDecodeError
from requests import Response


class Assertions:
    @staticmethod
    def to_json(response: Response) -> dict:
        try:
            return response.json()
        except JSONDecodeError:
            raise AssertionError(f"Response for {response.url} is not in JSON format. "
                                 f"Response text is {response.text}") from None

    @staticmethod
    def assert_json_has_key(response: Response, key):
        response_obj = Assertions.to_json(response)
        assert key in response_obj, f"Response for '{response.url}' doesn't have expected key '{key}'"

    @staticmethod
    def assert_json_has_keys(response: Response, *args):
        response_obj = Assertions.to_json(response)
        for key in args:
            assert key in response_obj, f"Response for '{response.url}' doesn't have expected key '{key}'"

    @staticmethod
    def assert_json_has_not_keys(response: Response, *args):
        response_obj = Assertions.to_json(response)
        for key in args:
            assert key not in response_obj, f"Response for '{response.url}' has unexpected key '{key}'"

    @staticmethod
    def assert_json_value_by_key(response: Response, key, expected_value):
        Assertions.assert_json_has_key(response, key)
        actual_value = response.json()[key]
        assert type(actual_value) == \
               type(expected_value), f"Values have different types. " \
                                     f"Actual value '{actual_value}' is {type(actual_value)}, " \
                                     f"expected value '{expected_value}' is {type(expected_value)}"
        assert actual_value == expected_value, \
            f"Unexpected '{key}' value: '{actual_value}' should be '{expected_value}'"

    @staticmethod
    def assert_equal_json_objects(response: Response, expected_result: dict):
        response_obj = Assertions.to_json(response)
        assert response_obj == expected_result, f"JSON objects are not equal! Got '{response_obj}', " \
                                                f"expected '{expected_result}'"

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

    @staticmethod
    def assert_response_text(response: Response, expected_text: str):
        actual_text = response.text
        assert actual_text == expected_text, f"Unexpected response text for URL: '{response.url}': " \
                                             f"got '{actual_text}', expected '{expected_text}'"
