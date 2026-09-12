import requests
import allure
from data import  ResponseMessages, Url

class TestGetOrderByNumber:
    
    @allure.title('Тест успешного получения заказа по его номеру')
    def test_get_order_by_number(self, create_order):    
        id_order = create_order['track']
        payload_get_order = create_order['response']
        response_get_order = requests.get(f"{Url.GET_ORDER_BY_NUMBER}?t={id_order}")
        requests.put(f"{Url.CANCEL_ORDER}?track={id_order}", data=payload_get_order)        

        assert 200 == response_get_order.status_code

    @allure.title('Тест получения заказа по его номеру без указания номера')
    def test_get_order_by_empty_track_number(self):
        id_order = ""
        response_get_order = requests.get(f"{Url.GET_ORDER_BY_NUMBER}?t={id_order}")
        message = response_get_order.json()

        assert 400 == response_get_order.status_code
        assert ResponseMessages.EMPTY_TRACK == message['message']    

    @allure.title('Тест получения заказа по его номеру по несуществующему номеру заказа')
    def test_get_order_by_empty_track_number(self, create_order, cancel_order):    
        track = create_order['track']
        cancel_order
        response_get_order = requests.get(f"{Url.GET_ORDER_BY_NUMBER}?t={track}")
        message = response_get_order.json()

        assert 404 == response_get_order.status_code
        assert ResponseMessages.BAD_TRACK == message['message']
