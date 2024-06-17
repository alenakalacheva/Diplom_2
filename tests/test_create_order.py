import requests
import allure
from data.urls import URL, Endpoints
from data.messages import MessageText


class TestCreateOrder:
    @allure.title('Проверка создания заказа авторизованным пользователем')
    @allure.description('''
                            1. Отправляем запрос на создание пользователя;
                            2. Отправляем запрос на создание заказа с авторизацией;
                            3. Проверяем ответ;
                            4. Удаляем пользователя.
                            ''')
    def test_create_order_with_auth(self, create_new_user, create_list_of_ingredients):
        data = create_list_of_ingredients
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        response = requests.post(URL.main_url + Endpoints.CREATE_ORDER, headers=headers,
                                 data=data)
        assert response.status_code == 200 and response.json().get("success") == True

    @allure.title('Проверка создания заказа без авторизации')
    @allure.description('''
                            1. Отправляем запрос на создание заказа без авторизации;
                            2. Проверяем ответ;
                            ''')
    def test_create_order_without_auth(self, ingredients_for_order):
        data = ingredients_for_order
        response = requests.post(URL.main_url + Endpoints.CREATE_ORDER, data=data)
        assert response.status_code == 401 and response.json().get("message") == MessageText.MESSAGE_WITHOUT_AUTH

    @allure.title('Проверка создания заказа авторизованным пользователем без ингредиентов')
    @allure.description('''
                            1. Отправляем запрос на создание пользователя;
                            2. Отправляем запрос на создание заказа без передачи ID ингредиентов с авторизацией;
                            3. Проверяем ответ;
                            4. Удаляем пользователя.
                            ''')
    def test_create_order_without_ingredients(self, create_new_user):
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        response = requests.post(URL.main_url + Endpoints.CREATE_ORDER, headers=headers)
        assert response.status_code == 400 and response.json().get(
            "message") == MessageText.CREATE_ORDER_WITHOUT_INGREDIENTS

    @allure.title('Проверка создания заказа авторизованным пользователем с невалидным хэшем ингредиента')
    @allure.description('''
                            1. Отправляем запрос на создание пользователя;
                            2. Отправляем запрос на создание заказа с невалидным хэшем ингредиентов с авторизацией;
                            3. Проверяем ответ;
                            4. Удаляем пользователя.
                            ''')
    def test_create_order_incorrect_hash(self, create_new_user):
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        data = {
            "ingredients": ["60d3b41fabdacab0026a533c6"]
        }

        response = requests.post(URL.main_url + Endpoints.CREATE_ORDER, headers=headers,
                                 data=data)
        assert response.status_code == 500
