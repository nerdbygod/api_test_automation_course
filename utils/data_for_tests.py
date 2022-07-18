from faker import Faker

fake = Faker()


def random_string(min_length, max_length):
    return fake.pystr(min_length, max_length)


username = fake.user_name()
firstName = fake.first_name()
lastName = fake.last_name()
email = fake.email()
password = random_string(5, 5)

test_user = {
    "username": "JohnDoe2001",
    "firstName": "John",
    "lastName": "Doe",
    "email": "johndoe2001@qa.qa",
    "password": "johndoe123",
    "id": 38880
}

test_user_credentials = {
    "email": "johndoe2001@qa.qa",
    "password": "johndoe123"
}

random_user = {
    "username": username,
    "firstName": firstName,
    "lastName": lastName,
    "email": email,
    "password": password
}
