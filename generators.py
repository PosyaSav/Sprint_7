import random
from faker import Faker
from data import Data

fake = Faker('ru_RU')

def email():
    generated_email = fake.email()
    return generated_email

def username():
    generated_username = fake.user_name()
    return generated_username

def password():
    generated_password = fake.password(length=10, special_chars=False, digits=True, upper_case=True, lower_case=True)
    return generated_password

def first_name():
    generated_name = fake.first_name()
    return generated_name

def last_name():
    return fake.last_name()

def address():
    return f"Москва, {fake.street_name()}"

def phone_number():
    remaining = ''.join([str(random.randint(0, 9)) for _ in range(9)])  
    return f"79{remaining}"

def date():
    return str(fake.future_date())

def rent_time():
    return random.randint(1, 7)

def metro_station():
    return Data.LIST_METRO_STATION[random.randint(0, (len(Data.LIST_METRO_STATION)-1))]

def scooter_colour(choise):
    return Data.COLOURS[choise]
