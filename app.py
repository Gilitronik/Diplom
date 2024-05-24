from flask import Flask, render_template, jsonify, request

from calculations import calculate_output
from handlers import read_weather_data, process_cities
from handlers import city_list


app = Flask(__name__)

# {'location': {'name': 'Vereya', 'region': 'Moskva', 'country': 'Russia', 'lat': 55.77, 'lon': 39.1, 'tz_id': 'Europe/Moscow', 'localtime_epoch': 1715025588, 'localtime': '2024-05-06 22:59'}, 'current': {'last_updated_epoch': 1715024700, 'last_updated': '2024-05-06 22:45', 'temp_c': 2.2, 'temp_f': 35.9, 'is_day': 0, 'condition': {'text': 'Partly Cloudy', 'icon': '//cdn.weatherapi.com/weather/64x64/night/116.png', 'code': 1003}, 'wind_mph': 6.9, 'wind_kph': 11.2, 'wind_degree': 68, 'wind_dir': 'ENE', 'pressure_mb': 1010.0, 'pressure_in': 29.83, 'precip_mm': 0.0, 'precip_in': 0.0, 'humidity': 69, 'cloud': 48, 'feelslike_c': -1.0, 'feelslike_f': 30.2, 'vis_km': 10.0, 'vis_miles': 6.0, 'uv': 1.0, 'gust_mph': 13.6, 'gust_kph': 22.0}}
@app.route('/')
def index():
    city_list_json = []
    for city_name in city_list:
        city_json = read_weather_data(city_name)
        if city_json:
            city_list_json.append(city_json)

    return render_template('index.html', city_list=city_list_json)


@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    output = None
    error = None
    city_name = request.args.get('city')

    if not city_name:
        error = 'Параметр "city" обязателен.'
        return render_template('calculate.html', output=output, error=error)

    if request.method == 'POST':
        try:
            area = float(request.form['area'])
            efficiency = float(request.form['efficiency'])
            tilt_angle = float(request.form['tilt_angle'])
            orientation = float(request.form['orientation'])

            city_weather = read_weather_data(city_name)

            # Проверяем наличие ключей в данных погоды
            if 'current' not in city_weather or 'uv' not in city_weather['current'] or 'temp_c' not in city_weather['current']:
                raise KeyError('Отсутствует ключ "current", "uv" или "temp_c" в данных погоды.')

            uv_index = city_weather['current']['uv']
            solar_irradiance = uv_index * 10  # Условное значение в Вт/м²
            temperature = city_weather['current']['temp_c']

            output = calculate_output(area, efficiency, solar_irradiance, temperature, tilt_angle, orientation)
            output = f"{output:.3f}"
        except (ValueError, KeyError, FileNotFoundError) as e:
            error = str(e)
    
    return render_template('calculate.html', output=output, error=error)


@app.route('/update_city_list')
def update_city_list():
    updated_city_list = process_cities(city_list)
    return jsonify({
        "success": True,
        "message": "Список городов успешно обновлен.",
        "city_list": updated_city_list
    })


if __name__ == '__main__':
    app.run(debug=True)
