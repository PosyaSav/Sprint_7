import json
import pytest
import requests
import generators
from data import Url

@pytest.fixture
def create_courier():
    """Фикстура для создания курьера"""
    payload_create_courier = generators.payload_create_courier()
    response_create_courier = requests.post(Url.CREATE_COURIER, data=payload_create_courier)
    # Проверяем успешность создания пользователя
    if response_create_courier.status_code != 201:
        try:
            error_msg = response_create_courier.json().get('message', 'Неизвестная ошибка')
        except:
            error_msg = response_create_courier.text
        raise Exception(f"Не удалось создать курьера: {error_msg}")
    response_login_courier = requests.post(Url.LOGIN, data = payload_create_courier)
    payload_delete_courier = response_login_courier.json()    
    response_data = {
        'status_code': response_create_courier.status_code, 
        'response': response_create_courier.json(), 
        'payload': payload_create_courier,
        'id': payload_delete_courier['id'],
        'delete': payload_delete_courier
        }
    yield response_data
    requests.delete(f"{Url.DELETE_COURIER}{response_data['id']}", data = response_data['delete'])

@pytest.fixture
def delete_courier(create_courier):
    """Фикстура для удаления курьера"""
    response_create_courier = create_courier
    payload_delete_courier = response_create_courier['delete']
    response_delete_courier = requests.delete(f"{Url.DELETE_COURIER}{payload_delete_courier['id']}", data = payload_delete_courier)
    return {
        'courier_data': response_create_courier['payload'], 
        'response': response_delete_courier.json(),
        'payload': payload_delete_courier
        }

"""
Запрос на удаление курьера должен происходить после yield а не до.

нужно исправить: удалять курьеров нужно в фикстуре с постусловием, 
в предысловии такой фикстуры делаем пустой список куда запишем айди для удаления, 
или генерируем креды, по которым потом удалим


yield заменне на return. 
А в остальном фикстура используется чтобы удалить курьера и тем самым обеспечить трек номер несуществующего курьера.
В темах урока не объясняется что так делать нельзя
"""

@pytest.fixture
def create_order():
    """Фикстура для создания заказа"""
    payload_create_order = generators.order_data()
    json_string = json.dumps(payload_create_order)
    response_create_order = requests.post(Url.CREATE_ORDER, data=json_string)
    track_order = response_create_order.json()
    response_get_order = requests.get(f"{Url.GET_ORDER_BY_NUMBER}?t={track_order['track']}")    
    id_order = response_get_order.json()['order']['id']
    payload_cancel_order = response_create_order.json()
    yield {
        'status_code': response_create_order.status_code, 
        'response': response_create_order.json(),
        'payload': payload_create_order,
        'track': track_order['track'],
        'id_order': id_order
        }   
    requests.put(f"{Url.CANCEL_ORDER}?track={payload_cancel_order['track']}", data=payload_cancel_order)

"""
Нужно исправить: если не возвращаемся в фикстуру после теста, то нужен return а не yield

Возврат в фикстуру происходит чтобы удалить курьера
"""

@pytest.fixture
def cancel_order(create_order):
    """Фикстура для отмены заказа"""
    payload_cancel_order = create_order
    requests.put(f"{Url.CANCEL_ORDER}?track={payload_cancel_order['track']}", data=payload_cancel_order['response'])
    return payload_cancel_order['track']

"""
заказ удаляем в постусловии, после yield а не до

Фикстура используется чтобы получить номер несуществующего заказа.
"""