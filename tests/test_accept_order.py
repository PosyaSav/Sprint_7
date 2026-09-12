import pytest
import requests
import allure
from data import  ResponseMessages, Url

class TestAcceprtOrder:

    @allure.title('Тест успешного запроса принять заказ')
    def test_successful_accepr_order(self, login_courier, create_order, delete_courier):
        id_courier = login_courier['response']['id']
        id_order = create_order['id_order']
        response_accept_order = requests.put(f"{Url.ACCEPT_ORDER}{id_order}?courierId={id_courier}")
        payload_finish_order = {}
        payload_finish_order['id'] = id_order
        requests.put(f"{Url.FINISH_ORDER}{id_order}", data=payload_finish_order)
        delete_courier

        assert 200 == response_accept_order.status_code

    @pytest.mark.parametrize('choise_id',['id_courier','id_order'])
    @allure.title('Тест запроса принять заказ с пустыми id курьера и заказа')
    def test_successful_accepr_order(self, create_order, login_courier, choise_id, delete_courier, cancel_order):
        id_order = create_order['id_order']
        empty_id ={
            'id_courier': login_courier['response']['id'],
            'id_order': f"{id_order}?courierId="
        }
        empty_id[choise_id] = ''
        response_accept_order = requests.put(f"{Url.ACCEPT_ORDER}{empty_id['id_order']}{empty_id['id_courier']}")#
        message = response_accept_order.json()
        delete_courier
        cancel_order
        assert 400 == response_accept_order.status_code
        assert ResponseMessages.EMPTY_TRACK == message['message']

    @allure.title('Тест запроса принять заказ с неверными id курьера')
    def test_successful_accepr_order(self, create_order, login_courier, delete_courier, cancel_order):
        id_order = create_order['id_order']
        data_id ={
            'id_courier': login_courier['response']['id'],
            'id_order': f"{id_order}?courierId="
        }
        delete_courier
        response_accept_order = requests.put(f"{Url.ACCEPT_ORDER}{data_id['id_order']}{data_id['id_courier']}")
        message = response_accept_order.json()

        cancel_order
        assert 404 == response_accept_order.status_code
        assert ResponseMessages.COURIER_NOT_EXISTS == message['message']

    @allure.title('Тест запроса принять заказ с неверными id заказа')
    def test_accepr_order_bad_id_order(self, login_courier):
        response_login_courier = login_courier['response']
        payload_delete_courier = response_login_courier#json()
        id_courier = payload_delete_courier['id']
        id_order = 11111111 
        response_accept_order = requests.put(f"{Url.ACCEPT_ORDER}{id_order}?courierId={id_courier}")
        requests.delete(f"{Url.DELETE_COURIER}{payload_delete_courier['id']}", data = payload_delete_courier)
        message = response_accept_order.json()

        assert 404 == response_accept_order.status_code
        assert ResponseMessages.ORDER_NOT_EXISTS == message['message']
    
    @allure.title('Тест запроса принять заказ с неверными id курьера')   #   заказа
    def test_accepr_order_bad_id_courier(self, create_order, login_courier, delete_courier, cancel_order):
        id_order = create_order['id_order']
        data_id ={
            'id_courier': login_courier['response']['id'],
            'id_order': f"{id_order}?courierId="
        }
        delete_courier
        response_accept_order = requests.put(f"{Url.ACCEPT_ORDER}{data_id['id_order']}{data_id['id_courier']}")
        message = response_accept_order.json()

        cancel_order
        assert 404 == response_accept_order.status_code
        assert ResponseMessages.COURIER_NOT_EXISTS == message['message']
