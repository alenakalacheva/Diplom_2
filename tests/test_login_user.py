import allure
import requests
from helpers import User
from data.urls import URL, Endpoints

class TestCreateUser:

    @allure.title('Проверка логина под существующим пользователем')
    @allure.description('''
                            1. Отправляем запрос на создание пользователя;
                            2. Отправляем запрос на разлогин пользователя;
                            3. Отправляем запрос на логин пользователя в системе;
                            4. Проверяем ответ;
                            5. Удаляем пользователя.
                            ''')
    def test_login_user(self, create_new_user):
        data = create_new_user

        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        refresh_token = create_new_user[1].json()["refreshToken"]
        requests.post(URL.main_url + Endpoints.LOGOUT, headers=headers, data=refresh_token)

        response = requests.post(URL.main_url + Endpoints.LOGIN, data=data[0])

        assert response.status_code == 200 and response.json().get("success") == True

    @allure.title('Проверка логина с неверными данными')
    @allure.description('''
                                1. Генерим случайные данные;
                                3. Оправляем запрос на логин;
                                3. Проверяем ответ;
                                ''')
    def test_login_incorrect_data(self):
        data = User.create_correct_user_data()
        response = requests.post(URL.main_url + Endpoints.LOGIN, data=data)
        assert response.status_code == 401 and response.json().get("success") == False