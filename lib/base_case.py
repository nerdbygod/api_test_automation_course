from requests import Response
from json.decoder import JSONDecodeError


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
            name: int | str
    ):
        try:
            response_as_dict = response.json()
        except JSONDecodeError:
            raise AssertionError(f"Response for {response.url} is not in JSON format. "
                                 f"Response text is {response.text}") from None
        assert name in response_as_dict, f"There is no field with the name {name} " \
                                         f"in the response body for {response.url}"
        return response_as_dict[name]
