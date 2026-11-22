import logging
import pytest
import requests
from requests.auth import HTTPBasicAuth

BASE_URL = 'http://127.0.0.1:8080'
AUTH_URL = BASE_URL + '/auth'
CARS_URL = BASE_URL + '/cars'

USERNAME = 'test_user'
PASSWORD = 'test_pass'
TOTAL_CARS = 25


logger = logging.getLogger('test_search')
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler('test_search.log', "w+", encoding='utf-8')
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)



@pytest.fixture(scope='class')
def session():
    s = requests.Session()
    logger.info('Аутентифікація користувача %s', USERNAME)

    response = s.post(AUTH_URL, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    logger.info('Відповідь /auth: %s', response.status_code)
    assert response.status_code == 200, f'Логін не вдався: {response.text}'

    token = response.json()['access_token']
    s.headers.update({'Authorization': f'Bearer {token}'})
    logger.info('Токен отримано')

    yield s

    s.close()
    logger.info('Сесію закрито')



class TestSearch:
    @pytest.mark.parametrize(
        'sort_by, limit',
        [
            (None, None),             # просто сортування за брендом
            ('price', 5),
            ('year', 10),
            ('engine_volume', 3),
            ('brand', 7),
            ('price', 25),            # коли ліміт такий ж як число машин
            ('price', 100),           # коли ліміт більше за число машин
        ],
    )
    def test_search_cars(self, session, sort_by, limit):
        params = {'sort_by': sort_by, 'limit': limit}
        logger.info('GET %s, params: sort_by=%s, limit=%s', CARS_URL, sort_by, limit)

        response = session.get(CARS_URL, params=params)
        logger.info('Статус: %s', response.status_code)
        assert response.status_code == 200, response.text

        cars = response.json()
        logger.info('Отримано автомобілів: %s', len(cars))

        expected_len = min(limit, TOTAL_CARS) if limit else TOTAL_CARS
        assert len(cars) == expected_len


        key = sort_by if sort_by else 'brand'
        values = [car[key] for car in cars]

        logger.info('Значення поля %s: %s', key, values)
        assert values == sorted(values)
    @pytest.mark.negative
    def test_search_without_token(self):
        logger.info('GET %s без токена', CARS_URL)
        response = requests.get(CARS_URL)
        logger.info('Статус: %s', response.status_code)
        assert response.status_code == 401
