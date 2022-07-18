from requests import Response
from json.decoder import JSONDecodeError


class Assertions:
    @staticmethod
    def assert_json_has_key(
            response: Response,
            key
    ):
        try:
            response_obj = response.json()
        except JSONDecodeError:
            raise AssertionError(f"Response for {response.url} is not in JSON format. "
                                 f"Response text is {response.text}") from None
        assert key in response_obj, f"There is no field with the name {key} in the response body " \
                                    f"for {response.url}, response text is {response.text}"

    @staticmethod
    def assert_json_value_by_key(
            response: Response,
            key,
            expected_value,
            error_message: str
    ):
        Assertions.assert_json_has_key(response, key)
        assert response.json()[key] == expected_value, error_message

    @staticmethod
    def assert_status_code(
            response: Response,
            expected_code: int,
    ):
        actual_code = response.status_code
        assert actual_code == expected_code, f"Response status code for {response.url} " \
                                             f"is {actual_code}, should be {expected_code}"
