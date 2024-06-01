import requests, json, os

# city_list = ['Podolsk', 'FC Khimki', 'Mytishchi', 'Korolev', 'Lubertsy', 'Krasnogorsk', 'Electric', 'Kolomna', 'Odintsovo', 'Domodedovo', 'Shchelkovo', 'Serpukhov', 'Ramenskoye', 'Orekhovo-Zuyevo', 'Dolgoprudny', 'Pushkino', 'Reutov', 'Zhukovsky', 'Noginsk', 'Sergiev', 'Voskresensk', 'Lobnya', 'Ivanteevka', 'Wedge', 'Prominent', 'Dubna', 'Yegoryevsk', 'Chekhov', 'Dmitrov', 'Naro-Fominsk', 'Stupino', 'Pavlovsky', 'Lytkarino', 'Fryazino', 'Dzerzhinsky', 'Kotelniki', 'Solnechnogorsk', 'Kashira', 'Krasnoznamensk', 'Protvino', 'Istra', 'Aprelevka', 'Shatura', 'Dedovsk', 'Lukhovitsy', 'Mozhaisk', 'Likino-Dulšvo', 'Krasnoarmeysk', 'Losino-Petrovsky', 'Lakes', 'Zvenigorod', 'Старая', 'Zaraisk', 'Elektrogorsk', 'Bronnitsy', 'Khotkovo', 'Chernogolovka', 'Electric', 'Pushchino', 'Kurovskoye', 'Kubinka', 'Roshal', 'Volokolamsk', 'Beloozerskiy', 'Golitsyno', 'Yakhroma', 'Peresvet', 'Krasnozavodsk', 'Taldom', 'Rousa', 'Drezna', 'Vysokovsk', 'Vereya']
city_list = ['Dmitrov', 'Moscow', 'Krasnozavodsk', 'Taldom', 'Rousa', 'Drezna', 'Vysokovsk', 'Vereya']


def take_city_weather_json(city='Moscow', lang='en', key='8c06e3650bfa4805864180042240505'):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    url = f'https://api.weatherapi.com/v1/current.json?q=q%3D{city}&lang={lang}&key={key}'
    response = requests.get(url, headers=headers)
    
    return json.loads(response.text)


def take_city_weather_days_json(city='Moscow', days='1', lang='en', key='8c06e3650bfa4805864180042240505'):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    url = f'https://api.weatherapi.com/v1/forecast.json?q={city}&lang={lang}&key={key}&days={days}&aqi=no&alerts=no'
    response = requests.get(url, headers=headers)

    return json.loads(response.text)


def save_weather_data(city_name, weather_data, directory='cities_weather'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    file_path = os.path.join(directory, f'{city_name}.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(weather_data, file, indent=4, ensure_ascii=False)


def read_weather_data(city_name, directory="cities_weather"):
    file_path = os.path.join(directory, f'{city_name}.json')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        print(f"Файл с данными о погоде для города {city_name} не найден.")
        return None


def process_cities(city_list=city_list):
    if isinstance(city_list, str):
        city_list = [city_list]

    for city_name in city_list:
        weather_data = take_city_weather_json(city_name, lang='ru')
        if weather_data:
            save_weather_data(city_name, weather_data)
            print(f"Данные о погоде для города {city_name} сохранены.")
        else:
            print(f"Не удалось получить данные о погоде для города {city_name}.")


def process_cities_days(city_object=city_list, days=1):
    if isinstance(city_object, str):
        city_list = [city_object]

    for city_name in city_list:
        weather_data = take_city_weather_days_json(city=city_name, days=days, lang='ru')
        if weather_data:
            save_weather_data(city_name, weather_data, directory='cities_weather_per_hours')
            print(f"Данные о погоде для города {city_name} сохранены.")
        else:
            print(f"Не удалось получить данные о погоде для города {city_name}.")



# Пример использования функции
# weather_data = read_weather_data('Vysokovsk')
# if weather_data:
#     print(weather_data['location']['region'])
