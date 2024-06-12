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
def create_exact_user():
    payload = {
            "email": '589@mail.ru',
            "password": 555,
            "name": 'Ivan'
        }
    response = requests.post(URL.main_url + Endpoints.CREATE_USER, data=payload)
    yield payload, response
    token = response.json()["accessToken"]
    requests.delete(URL.main_url + Endpoints.DELETE_USER, headers={"Authorization": token})


@pytest.fixture
def create_list_of_ingredients():
    response = requests.get(URL.main_url + Endpoints.INGREDIENTS)
    data = {"ingredients": [response.json()["data"][0]["_id"]]}
    return data



