import pytest
import requests
import allure
from data import  ResponseMessages, Url

class TestLoginCourier:
    
    @allure.title('Тест успешной авторизации')
    def test_successful_login_courier(self, create_courier):
        payload_login_courier = create_courier['payload']
        response_login_courier = requests.post(Url.LOGIN, data = payload_login_courier)

        assert 200 == response_login_courier.status_code

    @pytest.mark.parametrize('field',['login','password'])
    @allure.title('Тест авторизации с пустыми логином или паролем')
    def test_login_courier_without_login_or_password(self, create_courier, field):
        response_create = create_courier['payload']
        payload_login_empty_field = response_create
        payload_login_empty_field[field] = ''
        response_login_empty_field = requests.post(Url.LOGIN, data = payload_login_empty_field)
        message = response_login_empty_field.json()

        assert 400 == response_login_empty_field.status_code
        assert ResponseMessages.EMPTY_LOGIN_DATA == message['message']

    @allure.title('Тест авторизации под несуществующим пользователем')
    def test_login_not_exists_courier(self, delete_courier):
        payload_login = delete_courier['courier_data']
        response_login = requests.post(Url.LOGIN, data = payload_login)
        message = response_login.json()
        
        assert 404 == response_login.status_code
        assert ResponseMessages.BAD_LOGIN == message['message']
