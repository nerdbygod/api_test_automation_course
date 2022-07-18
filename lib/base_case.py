from requests import Response
from lib.assertions import Assertions


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
