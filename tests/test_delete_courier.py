import requests
import allure
from data import  Url
from data import  Url, ResponseMessages

class TestDeleteCourier:
    
    @allure.title('Тест удаления существующего курьера')
    def test_delete_exists_courier(self, create_courier):
        payload_delete_courier = create_courier['delete']
        response_delete_courier = requests.delete(f"{Url.DELETE_COURIER}{payload_delete_courier['id']}", data = payload_delete_courier)      

        assert 200 == response_delete_courier.status_code
        assert ResponseMessages.SUCCESS == response_delete_courier.json()

    @allure.title('Тест удаления не существующего курьера')
    def test_delete_courier_bad_id(self, delete_courier):
        response_delete = delete_courier
        response_delete_bad_id = requests.delete(f"{Url.DELETE_COURIER}{response_delete['payload']['id']}", data = response_delete['payload'])
        message = response_delete_bad_id.json()
        assert 404 == response_delete_bad_id.status_code
        assert ResponseMessages.BAD_ID == message['message']

    """
    Здесь удаление это не предусловие.

    мы просто можем удалять случайного курьера, зачем его было создавать и удалять в предусловии?

    Нет понимания откуда брать трек номер курьера для удаления. 
    При генерации может появиться существующий курьер и тест провалится. 
    Создать и удалить курьера гарантированно дает нам трек номер несуществующего курьера, тест всегда будет выполняться.
    """
    @allure.title('Тест удаления существующего курьера с запросом без id')
    def test_delete_courier_empty_id(self):
        response_delete_empty_id = requests.delete(f"{Url.DELETE_COURIER}")
        message = response_delete_empty_id.json()
        assert 404 == response_delete_empty_id.status_code
        assert ResponseMessages.EMPTY_ID == message['message']
