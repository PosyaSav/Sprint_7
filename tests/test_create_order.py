import json
import pytest
import requests
import allure
from data import  Url
import generators

class TestCreateOrder:

    @pytest.mark.parametrize('colour',['None','Black','Grey','Both'])
    @allure.title('Тест успешного создания заказа с различными выборами цвета самоката')
    def test_successful_create_order(self, colour):
        payload_create_order = generators.order_data()
        payload_create_order["colour"] = generators.scooter_colour(colour) 
        json_string = json.dumps(payload_create_order)
        response_create_order = requests.post(Url.CREATE_ORDER, data=json_string)
        payload_cancel_order = response_create_order.json()
        requests.put(f"{Url.CANCEL_ORDER}?track={payload_cancel_order['track']}", data=payload_cancel_order)

        assert 201 == response_create_order.status_code
        assert 'track' in response_create_order.json()
