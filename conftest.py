import pytest
import requests
from helpers import User
from data.urls import URL, Endpoints


@pytest.fixture
def create_new_user():
    payload = User.create_correct_user_data()
    response = requests.post(URL.main_url + Endpoints.CREATE_USER, data=payload)
    yield payload, response
    token = response.json()["accessToken"]
    requests.delete(URL.main_url + Endpoints.DELETE_USER, headers={"Authorization": token})


@pytest.fixture
def create_two_users():
    payload_u1 = User.create_correct_user_data()  # создаем данные для пользователя 1
    payload_u2 = User.create_correct_user_data()  # создаем данные для пользователя 2
    response_u1 = requests.post(URL.main_url + Endpoints.CREATE_USER, data=payload_u1)  # создаем пользователя 1
    response_u2 = requests.post(URL.main_url + Endpoints.CREATE_USER, data=payload_u2)  # создаем пользователя 2
    token_u1 = response_u1.json()["accessToken"]
    token_u2 = response_u2.json()["accessToken"]
    yield payload_u1, token_u2
    requests.delete(URL.main_url + Endpoints.DELETE_USER, headers={"Authorization": token_u1})  # удаляем пользователя 1
    requests.delete(URL.main_url + Endpoints.DELETE_USER, headers={"Authorization": token_u2})  # удаляем пользователя 2


@pytest.fixture
def ingredients_for_order():
    response = requests.get(URL.main_url + Endpoints.INGREDIENTS)
    data = {"ingredients": [response.json()["data"][0]["_id"]]}
    return data
