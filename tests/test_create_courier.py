import pytest
import requests
import allure
from data import  Url, ResponseMessages

class TestCreateCourier:

    @allure.title('Тест успешного создания курьера')
    def test_successful_create_courier(self,create_courier_delete_after_test):
        response_create = create_courier_delete_after_test
        
        assert 201 == response_create['status_code']
        assert ResponseMessages.SUCCESS == response_create['response']

    @allure.title('Тест создания одинаковых курьеров')
    def test_create_same_couriers_failed(self, create_same_courier):
        response_create_same = create_same_courier        
        message = response_create_same.json()

        assert 409 == response_create_same.status_code
        assert ResponseMessages.COURIER_EXISTS == message['message']   

    @pytest.mark.parametrize('field',['login','password'])
    @allure.title('Тест создания курьера, с пустыми логином или паролем')
    def test_create_courier_without_login_or_password(self, payload_create_courier, field):   
        payload_create  = payload_create_courier.copy()
        del payload_create[field]
        response_create = requests.post(Url.CREATE_COURIER, data = payload_create)
        message = response_create.json()

        assert 400 == response_create.status_code
        assert ResponseMessages.FAILED_CREATE_COURIER == message['message']
