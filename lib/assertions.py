from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(
            response: Response,
            name,
            expected_value,
            error_message: str
    ):
        try:
            response_obj = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is {response.text}"

        assert name in response_obj, f"There is no field with the name {name} in the response body"
        assert response_obj[name] == expected_value, error_message
