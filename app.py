from flask import Flask, render_template, jsonify, redirect, url_for, request

# from calculations import calculate_output
from handlers import read_weather_data, process_cities, process_cities_days
from handlers import city_list
from calculations import calculate_solar_output, calculate_simple_output


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    city_list_json = []
    for city_name in city_list:
        city_json = read_weather_data(city_name)
        if city_json:
            city_list_json.append(city_json)

    return render_template('index.html', city_list=city_list_json)

if L <= X <= R:
@app.route('/cities_list', methods=['GET', 'POST'])
def cities_list():
    query = request.args.get('query', '')
    city_list_json = []
    for city_name in city_list:
        if query.lower() in city_name.lower():
            city_json = read_weather_data(city_name)
            if city_json:
                city_list_json.append(city_json)

    return render_template('cities_list.html', city_list=city_list_json)


@app.route('/cities_list/update_cities_list', methods=['GET', 'POST'])
def update_cityies_list():
    process_cities()
    return redirect(url_for('cities_list'), code=302)


@app.route('/cities_list/calculate', methods=['GET', 'POST'])
def calculate():
    city_name = request.args.get('city_name')
    city_weather = read_weather_data(city_name)

    return render_template('calculate.html', city=city_weather)


@app.route('/cities_list/calculate/update_city_data', methods=['GET', 'POST'])
def update_city():
    data = request.get_json()
    city_name = data.get('city_name')
    process_cities(city_name)
    city = read_weather_data(city_name)
    return jsonify(city), 200


@app.route('/cities_list/calculate/create_chart', methods=['GET', 'POST'])
def create_chart():
    data = request.get_json()
    city_name = data.get('city_name')
    process_cities_days(city_name, days=10)
    city_data_days = read_weather_data(city_name, directory="cities_weather_per_hours")
    data = city_data_days['forecast']
    
    for day_i in range(len(data['forecastday'])):
        for hour_i in range(len(data['forecastday'][day_i]['hour'])):
            output_power = calculate_simple_output(data['forecastday'][day_i]['hour'][hour_i])
            data['forecastday'][day_i]['hour'][hour_i]['output_power'] = output_power
            
    return jsonify(data), 200


@app.route('/calculate', methods=['GET', 'POST'])
def calculate_start():
    # try:
    data = request.get_json()
    output = None
    city_name = data.get('city_name')

    # if request.method == 'POST':
    city_dict_from_page = {
        'current': {
            'uv': data.get('uv_index'),
            'temp_c': data.get('temp_c'),
            'cloud': data.get('cloud'),
            'last_updated': data.get('last_updated')
        },
        'location': {
            'lat': data.get('lat'),
            'lon': data.get('lon')
        }
    }
    panel_area = data.get('panel_area')
    panel_efficiency = data.get('panel_efficiency')
    azimuth_angle = data.get('azimuth_angle')
    tilt_angle = data.get('tilt_angle')
    is_tracking = data.get('is_tracking')
    if is_tracking:
        azimuth_angle = data.get('azimuth_angle')
        tilt_angle = data.get('tilt_angle')
    else:   
        azimuth_angle = None
        tilt_angle = None
    output = calculate_solar_output(city_dict_from_page, panel_area, panel_efficiency, azimuth_angle, tilt_angle, is_tracking)

    return jsonify(message=f"Результат: {output:.3f} Вольт"), 200
    # except Exception as e:
    #     return jsonify(error=str(e)), 400


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/update_city_list')
def update_city_list():
    updated_city_list = process_cities()
    return jsonify({
        "success": True,
        "message": "Список городов успешно обновлен.",
        "city_list": updated_city_list
    })


if __name__ == '__main__':
    app.run(debug=True)
