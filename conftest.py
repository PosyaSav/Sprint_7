import json
import pytest
import requests
import generators
from data import Url

@pytest.fixture
def payload_create_courier():
    """Фикстура для генерации данных курьера"""
    payload = {
        'login': generators.username(),
        'password': generators.password(),
        'firstName': generators.first_name()
    }
    yield payload

@pytest.fixture
def create_courier(payload_create_courier):
    """Фикстура для создания курьера"""
    response_create_courier = requests.post(Url.CREATE_COURIER, data=payload_create_courier)
    # Проверяем успешность создания пользователя
    if response_create_courier.status_code != 201:
        try:
            error_msg = response_create_courier.json().get('message', 'Неизвестная ошибка')
        except:
            error_msg = response_create_courier.text
        raise Exception(f"Не удалось создать курьера: {error_msg}")
    
    yield {
        'status_code': response_create_courier.status_code, 
        'response': response_create_courier.json(), 
        'payload': payload_create_courier
        }

@pytest.fixture
def login_courier(create_courier):
    """Фикстура для авторизации курьера"""
    payload_login_courier = create_courier['payload']
    # del payload_login_courier['firstName']
    response_login_courier = requests.post(Url.LOGIN, data = payload_login_courier)
    yield {
        'status_code': response_login_courier.status_code, 
        'response': response_login_courier.json(),
        'payload': payload_login_courier
        }

@pytest.fixture
def delete_courier(login_courier):
    """Фикстура для удаления курьера"""
    payload_delete_courier = login_courier['response']

    response_delete_courier = requests.delete(f"{Url.DELETE_COURIER}{payload_delete_courier['id']}", data = payload_delete_courier)

    yield {
        'status_code': response_delete_courier.status_code, 
        'response': response_delete_courier.json(),
        'payload': payload_delete_courier
        }

@pytest.fixture
def create_courier_delete_after_test(create_courier, login_courier, delete_courier):
    """Фикстура для создания, авторизации и удаления курьера"""
    yield create_courier
    # Удаление курьера после теста
    login_courier
    delete_courier

@pytest.fixture
def create_same_courier(payload_create_courier):
        """Фикстура для создания курьеров с одинаковыми данными"""
        requests.post(Url.CREATE_COURIER, data = payload_create_courier)
        response_create_same = requests.post(Url.CREATE_COURIER, data = payload_create_courier)
        yield response_create_same
        response_login = requests.post(Url.LOGIN, data = payload_create_courier)
        payload_delete = response_login.json()
        requests.delete(f"{Url.DELETE_COURIER}{payload_delete['id']}", data = payload_delete)

@pytest.fixture
def order_data():
    """Фикстура для генерации данных заказа"""
    payload_create_order = {
    "firstName": generators.first_name(),
    "lastName": generators.last_name(),
    "address": generators.address(),    
    "metroStation": generators.metro_station(),   
    "phone":generators.phone_number(),
    "rentTime": generators.rent_time(),
    "deliveryDate": generators.date(),  
    "comment": "123",
    "colour": "" 
    }
    yield payload_create_order

@pytest.fixture
def create_order(order_data):
    """Фикстура для создания заказа"""
    json_string = json.dumps(order_data)
    response_create_order = requests.post(Url.CREATE_ORDER, data=json_string)
    track_order = response_create_order.json()
    response_get_order = requests.get(f"{Url.GET_ORDER_BY_NUMBER}?t={track_order['track']}")    
    id_order = response_get_order.json()['order']['id']
    yield {
        'status_code': response_create_order.status_code, 
        'response': response_create_order.json(),
        'payload': order_data,
        'track': track_order['track'],
        'id_order': id_order
        }   

@pytest.fixture
def cancel_order(create_order):
    """Фикстура для отмены заказа"""
    payload_cancel_order = create_order['response']
    yield requests.put(f"{Url.CANCEL_ORDER}?track={payload_cancel_order['track']}", data=payload_cancel_order)
