from datetime import datetime, timedelta


CLIENT_CREATE_VALID_DATA = (
    (
        {
            "email": "test_client_01@unexistingmail.ru",
            "password": "neverinmylife-123",
            "first_name": "Mr. Client",
            "birthday": "12.09.1970",
        },
        "имя и ДР",
    ),
    (
        {
            "email": "test_client_02@unexistingmail.ru",
            "password": "neverinmylife-123",
            "first_name": "Mr. Beast",
            "birthday": "12.09.1970",
            "phone": "89991234567",
        },
        "имя, ДР, номер телефона",
    ),
)

CLIENT_CREATE_INVALID_DATA = (
    (
        {
            "password": "neverinmylife-123",
            "first_name": "Mr. Client",
            "birthday": "12.09.1970",
        },
        "нет email",
    ),
    (
        {
            "email": "test_client_03@unexistingmail.ru",
            "first_name": "Mr. Beast",
            "birthday": "12.09.1970",
        },
        "нет пароля",
    ),
    (
        {
            "email": "test_client_04@unexistingmail.ru",
            "password": "neverinmylife-123",
            "birthday": "12.09.1970",
        },
        "нет имени",
    ),
    (
        {
            "email": "test_client_05@unexistingmail.ru",
            "password": "neverinmylife-123",
            "first_name": "Mr. Client",
        },
        "нет даты рождения",
    ),
    (
        {
            "email": "test_client_06",
            "password": "neverinmylife-123",
            "first_name": "Mr. Client",
            "birthday": "12.09.1970",
        },
        "некорректный email",
    ),
    (
        {
            "email": "test_client_07@unexistingmail.ru",
            "password": "12345",
            "first_name": "Mr. Client",
            "birthday": "12.09.1970",
        },
        "цифровой пароль",
    ),
    (
        {
            "email": "test_client_07@unexistingmail.ru",
            "password": "password",
            "first_name": "Mr. Client",
            "birthday": "12.09.1970",
        },
        "слишком простой пароль",
    ),
    (
        {
            "email": "test_client_08@unexistingmail.ru",
            "password": "neverinmylife-123",
            "first_name": "Mr. Client",
            "birthday": "12.09.2015",
        },
        "моложе 18 лет",
    ),
    (
        {
            "email": "test_client_09@unexistingmail.ru",
            "password": "neverinmylife-123",
            "first_name": "Mr. Client",
            "birthday": "12.09.1900",
        },
        "старше 120 лет",
    ),
)
