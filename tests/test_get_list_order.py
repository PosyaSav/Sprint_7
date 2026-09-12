import requests
import allure
from data import  Url

class TestGetListOreder:
    
    @allure.title('Тест получения списка заказов с проверкой, что в тело ответа возвращается список заказов')
    def test_get_list_order_returnList(self):
        response_get_list_order = requests.get(Url.LIST_ORDER)
        response_dict = response_get_list_order.json()
        assert  isinstance(response_dict['orders'], list)
