import pytest
import requests
import allure

from data.urls import URL, Endpoints
from data.messages import MessageText
from helpers import User


class TestChangeUserData:
    @allure.title('Проверка изменения имени и почты пользователя с авторизацией')
    @allure.description('''
                                1. Отправляем запрос на создание пользователя;
                                2. Отправляем запрос на изменение параметров пользователя;
                                3. Проверяем ответ;
                                4. Удаляем пользователя.
                                ''')
    @pytest.mark.parametrize('data, key', [
        [{"name": User.create_correct_user_data()["name"]}, "name"],
        [{"email": User.create_correct_user_data()["email"]}, "email"]
    ])
    def test_change_name_email(self, create_new_user, data, key):
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        response = requests.patch(URL.main_url + Endpoints.DATA_CHANGE, headers=headers, data=data)
        assert response.status_code == 200 and response.json().get("success") == True
        assert response.json().get("user")[key] == data[key]

    @allure.title('Проверка изменения пароля пользователя с авторизацией')
    @allure.description('''
                                        1. Отправляем запрос на создание пользователя;
                                        2. Отправляем запрос на изменение пароля;
                                        3. Разлогиниваем пользователя;
                                        4. Логинимся с новым паролем;
                                        5. Проверяем ответ;
                                        6. Удаляем пользователя.
                                        ''')
    def test_change_password(self, create_new_user):
        new_pass = {"password": 858585}
        payload = create_new_user[0]
        payload["password"] = 858585

        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        refresh_token = create_new_user[1].json()["refreshToken"]

        requests.patch(URL.main_url + Endpoints.DATA_CHANGE, headers=headers, data=new_pass)
        requests.post(URL.main_url + Endpoints.LOGOUT, headers=headers, data=refresh_token)
        response = requests.post(URL.main_url + Endpoints.LOGIN, data=payload)
        assert response.status_code == 200 and response.json().get("success") == True

    @allure.title('Проверка изменения почты пользователя на существующую')
    @allure.description('''
                                            1. Отправляем запрос на создание пользователя;
                                            2. Отправляем запрос на изменение почты уже зарегестрированный;
                                            3. Проверяем ответ
                                            4. Удаляем пользователей
                                            ''')
    def test_change_email_exist(self, create_exact_user, create_new_user):
        data = create_exact_user[0]
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        response = requests.patch(URL.main_url + Endpoints.DATA_CHANGE, headers=headers, data=data)
        assert response.status_code == 403 and response.json().get("message") == MessageText.MESSAGE_EXISTING_EMAIL

    @allure.title('Проверка изменения данных пользователя без авторизации')
    @allure.description('''
                                1. Отправляем запрос на изменение параметров пользователя;
                                2. Проверяем ответ.
                                ''')
    @pytest.mark.parametrize('data', [
        {"name": User.create_correct_user_data()["name"]},
        {"password": User.create_correct_user_data()["password"]},
        {"email": User.create_correct_user_data()["email"]}
    ])
    def test_change_person_data_without_auth(self, data):
        response = requests.patch(URL.main_url + Endpoints.DATA_CHANGE, data=data)
        assert response.status_code == 401 and (
                response.json().get("message") == MessageText.MESSAGE_WITHOUT_AUTH
        )
