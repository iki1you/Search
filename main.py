import sys
from io import BytesIO
from size import getsize, lonlat_distance
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image

# Пусть наше приложение предполагает запуск:
# python main.py Нижневартовск, ул. Дзержинского, 10
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

delta = getsize(toponym)

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([delta, delta]),
    "l": "map"}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

address_ll = f"{toponym_longitude},{toponym_lattitude}"

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}
response = requests.get(search_api_server, params=search_params)
# Преобразуем ответ в json-объект
json_response = response.json()

# Получаем первую найденную организацию.
organization = json_response["features"][0]
# Название организации.
org_name = organization["properties"]["CompanyMetaData"]["name"]
# Адрес организации.
org_address = organization["properties"]["CompanyMetaData"]["address"]

# Получаем координаты ответа.
point = organization["geometry"]["coordinates"]

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    # позиционируем карту центром на наш исходный адрес
    "ll": address_ll,
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
    "pt": f'{toponym_longitude},{toponym_lattitude},pm2rdm~{point[0]},{point[1]}'
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
info = [organization["properties"]["CompanyMetaData"]["address"],
        organization["properties"]["CompanyMetaData"]["name"],
        ]
print('\n'.join(info))
print(organization["properties"]["CompanyMetaData"]["Hours"]['text'])
print(round(lonlat_distance((toponym_longitude, toponym_lattitude), (point[0], point[1]))), 'm')

# Определяем функцию, считающую расстояние между двумя точками, заданными координатами

response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(
    response.content)).show()

# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы
