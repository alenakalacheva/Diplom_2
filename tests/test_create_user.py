import pytest
import requests
import allure

from data.urls import URL, Endpoints
from data.messages import MessageText
from helpers import User


class TestCreateUser:
    @allure.title('Проверка создания нового пользователя')
    @allure.description('''
                            1. Отправляем запрос на создание пользователя;
                            2. Проверяем ответ;
                            3. Удаляем пользователя.
                            ''')
    def test_create_user(self, create_new_user):
        response = create_new_user
        assert response[1].json().get("success") == True and response[1].status_code == 200

    @allure.title('Проверка создания дублирующего пользователя')
    @allure.description('''
                            1. Отправляем запрос на создание пользователя;
                            2. Получаем данные для регистрации;
                            3. Отправляем повторный запрос на создание пользователя;
                            4. Проверяем ответ;
                            5. Удаляем пользователя.
                            ''')
    def test_create_duplicate_user(self, create_new_user):
        response = create_new_user
        payload = response[0]
        response_double_register = requests.post(URL.main_url + Endpoints.CREATE_USER, data=payload)
        assert response_double_register.status_code == 403 and (
                response_double_register.json().get("message") == MessageText.MESSAGE_EXISTING_USER
        )

    @allure.title('Проверка создания пользователя без обязательных полей')
    @allure.description('''
                            1. Отправляем запрос на создание пользователя без обязательных полей;
                            2. Проверяем ответ.
                            ''')
    @pytest.mark.parametrize('payload', [
        User.create_user_data_without_name(),
        User.create_user_data_without_email(),
        User.create_user_data_without_password(),
        {}

    ])
    def test_create_user_empty_fields(self, payload):
        response = requests.post(URL.main_url + Endpoints.CREATE_USER, data=payload)
        assert response.status_code == 403 and response.json().get("message") == MessageText.MESSAGE_EMPTY_FIELDS


