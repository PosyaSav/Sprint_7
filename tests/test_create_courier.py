import pytest
import requests
import allure
from data import  Url, ResponseMessages
import generators

class TestCreateCourier:

    @allure.title('Тест успешного создания курьера')
    def test_successful_create_courier(self):
        payload_create_courier = generators.payload_create_courier()
        response_create_courier = requests.post(Url.CREATE_COURIER, data=payload_create_courier)
        response_login_courier = requests.post(Url.LOGIN, data = payload_create_courier)
        payload_delete_courier = response_login_courier.json()    
        requests.delete(f"{Url.DELETE_COURIER}{payload_delete_courier['id']}", data = payload_delete_courier)      

        assert 201 == response_create_courier.status_code
        assert ResponseMessages.SUCCESS == response_create_courier.json()

    @allure.title('Тест создания одинаковых курьеров')
    def test_create_same_couriers_failed(self, create_courier):
        payload_create_courier = create_courier['payload']
        response_create_same = requests.post(Url.CREATE_COURIER, data = payload_create_courier)
        message = response_create_same.json()

        assert 409 == response_create_same.status_code
        assert ResponseMessages.COURIER_EXISTS == message['message']   

    @pytest.mark.parametrize('field',['login','password'])
    @allure.title('Тест создания курьера, с пустыми логином или паролем')
    def test_create_courier_without_login_or_password(self, create_courier, field):   
        payload_create  = create_courier['payload']
        del payload_create[field]
        response_create = requests.post(Url.CREATE_COURIER, data = payload_create)
        message = response_create.json()

        assert 400 == response_create.status_code
        assert ResponseMessages.FAILED_CREATE_COURIER == message['message']
