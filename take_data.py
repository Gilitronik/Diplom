import requests, json, os

city_list = ['Dmitrov', 'Krasnozavodsk', 'Taldom', 'Rousa', 'Drezna', 'Vysokovsk', 'Vereya']


def take_city_weather_json(city='Moscow', lang='en', key='8c06e3650bfa4805864180042240505'):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    url = f'https://api.weatherapi.com/v1/current.json?q=q%3D{city}&lang={lang}&key={key}'
    response = requests.get(url, headers=headers)
    
    return json.loads(response.text)


def take_city_weather_days_json(city='Moscow', days='1', lang='en', key='8c06e3650bfa4805864180042240505'):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    url = f'https://api.weatherapi.com/v1/current.json?q=q{city}&lang={lang}&key={key}&days={days}&aqi=no&alerts=no'
    response = requests.get(url, headers=headers)

    return json.loads(response.test)


def save_weather_data(city_name, weather_data):
    directory = 'cities_weather'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    file_path = os.path.join(directory, f'{city_name}.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(weather_data, file, indent=4, ensure_ascii=False)

def process_cities(city_list):
    for city_name in city_list:
        weather_data = take_city_weather_json(city_name)
        if weather_data:
            save_weather_data(city_name, weather_data)
            print(f"Данные о погоде для города {city_name} сохранены.")
        else:
            print(f"Не удалось получить данные о погоде для города {city_name}.")


process_cities(city_list)
