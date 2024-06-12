import requests
import allure
from data.urls import URL, Endpoints
from data.messages import MessageText

class TestGetOrder:
    @allure.title('Проверка получения заказа авторизованным пользователем')
    @allure.description('''
                            1. Отправляем запрос на создание пользователя;
                            2. Отправляем запрос на создание заказа;
                            3. Отправляем запрос на получение заказа пользователя
                            4. Проверяем ответ;
                            5. Удаляем пользователя
                            ''')
    def test_get_order_with_auth(self, create_new_user, create_list_of_ingredients):
        data = create_list_of_ingredients
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        response = requests.post(URL.main_url + Endpoints.CREATE_ORDER, headers=headers,
                                 data=data)

        response_get_order = requests.get(URL.main_url + Endpoints.GET_ORDERS, headers=headers)
        assert response_get_order.status_code == 200 and (
                response.json()["order"]["number"] == response_get_order.json()["orders"][0]["number"]
        )

    @allure.title('Проверка получения заказа неавторизованным пользователем')
    @allure.description('''
                            1. Отправляем запрос на получение заказа;
                            2. Проверяем ответ.
                            ''')
    def test_get_order_without_auth(self):
        response_get_order = requests.get(URL.main_url + Endpoints.GET_ORDERS)
        assert response_get_order.status_code == 401 and (
                MessageText.MESSAGE_WITHOUT_AUTH in response_get_order.text
        )