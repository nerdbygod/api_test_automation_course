from requests import Response
from json.decoder import JSONDecodeError


class BaseCase:
    def get_cookie(
            self, 
            response: Response,
            cookie_name: str
    ):
        assert cookie_name in response.cookies, f"Cannot find {cookie_name} in the response"
        return response.cookies[cookie_name]

    def get_header(
            self,
            response: Response,
            header_name: str
    ):
        assert header_name in response.headers, f"Cannot find {header_name} in the response"
        return response.headers[header_name]

    def get_json_value(
            self,
            response: Response,
            name: int | str
    ):
        try:
            assert name in response.json(), f"There is no field with the name {name} in the response body"
        except JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is {response.text}"
        return response.json()[name]
