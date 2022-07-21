import allure
from lib.assertions import Assertions
from lib.base_case import BaseCase
from utils.urls import API_USER_CREATE, API_USER_LOGIN
from lib.send_requests import SendRequest


@allure.epic("Editing user data test cases")
class TestUserSuccessfulEdit(BaseCase):
    @allure.description("Tests if authorized user can successfully edit his first name")
    def test_edit_created_user_first_name(self):
        # Register new user
        register_data = self.prepare_registration_data()
        response_1 = SendRequest.post(API_USER_CREATE, data=register_data)

        Assertions.assert_status_code(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

        email = register_data["email"]
        password = register_data["password"]
        created_user_id = self.get_json_value(response_1, "id")

        # Login registered user
        login_data = {
            "email": email,
            "password": password
        }
        response_2 = SendRequest.post(API_USER_LOGIN, data=login_data)
        auth_sid_cookie = self.get_cookie(response_2, "auth_sid")
        csrf_token_header = self.get_header(response_2, "x-csrf-token")

        # Edit created user data
        api_update_user = f"{API_USER_CREATE}/{created_user_id}"
        new_first_name = "New first name"

        response_3 = SendRequest.put(
            api_update_user,
            cookies={"auth_sid": auth_sid_cookie},
            headers={"x-csrf-token": csrf_token_header},
            data={"firstName": new_first_name}
        )
        Assertions.assert_status_code(response_3, 200)

        # Check changed data
        response_4 = SendRequest.get(
            api_update_user,
            cookies={"auth_sid": auth_sid_cookie},
            headers={"x-csrf-token": csrf_token_header}
        )
        Assertions.assert_json_value_by_key(
            response_4,
            "firstName",
            new_first_name
        )

    @allure.description("Tests if authorized user can successfully edit his last name")
    def test_edit_create_user_last_name(self):
        # Register new user
        register_data = self.prepare_registration_data()
        response_1 = SendRequest.post(API_USER_CREATE, data=register_data)

        Assertions.assert_status_code(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

        email = register_data["email"]
        password = register_data["password"]
        created_user_id = self.get_json_value(response_1, "id")

        # Login registered user
        login_data = {
            "email": email,
            "password": password
        }
        response_2 = SendRequest.post(API_USER_LOGIN, data=login_data)
        auth_sid_cookie = self.get_cookie(response_2, "auth_sid")
        csrf_token_header = self.get_header(response_2, "x-csrf-token")

        # Edit created user data
        api_update_user = f"{API_USER_CREATE}/{created_user_id}"
        new_last_name = "New last name"

        response_3 = SendRequest.put(
            api_update_user,
            cookies={"auth_sid": auth_sid_cookie},
            headers={"x-csrf-token": csrf_token_header},
            data={"firstName": new_last_name}
        )
        Assertions.assert_status_code(response_3, 200)

        # Check changed data
        response_4 = SendRequest.get(
            api_update_user,
            cookies={"auth_sid": auth_sid_cookie},
            headers={"x-csrf-token": csrf_token_header}
        )
        Assertions.assert_json_value_by_key(
            response_4,
            "firstName",
            new_last_name
        )

#
# class TestUserUnsuccessfulEdit(BaseCase):
#     pass
#



# Успешная смена данных пользователя: firstName, lastName. Проверить, что поменялись
# Успешная смена данных пользователя: email, password. Проверить, что данные поменялись.
    # Проверить, что по старому email, паролю нельзя авторизоваться.
    # Проверить, что по новым данным авторизоваться можно.
# Неуспешная смена данных пользователя:
    # 1. Отсутствует cookie/header в заголовках
    # 2. Переданы пустые параметры в полях
    # 3. Переданы слишком длинные параметры в полях
    # 4. Авторизованный пользователь пытается поменять данные другого пользователя (id созданного пользователя
        # заменяется id другого существующего пользователя, при этом id созданного пользователя > id существующего пользователя.
        # Проверить сообщение об ошибке, статус код
        # Проверить, что данные пользователя не поменялись.
    # 5. Авторизованнный пользователь пытается поменять данные несуществующего пользователя (запрос на несуществующий id)
    # 6. Попытка поменять несуществующий параметр (например, "id", другой рандомный)
