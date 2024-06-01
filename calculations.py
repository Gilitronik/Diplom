from handlers import read_weather_data
import json
import math

import time
from datetime import datetime

def calculate_solar_output(data, panel_area, panel_efficiency, azimuth_angle, tilt_angle, is_tracking):
    
    temp_coeff = -0.005  # Коэффициент температуры панели (примерное значение)
    reference_temp = 25  # °C, температурная точка отсчета
    
    try:
        uv_index = float(data['current']['uv'])  # УФ индекс
        temp = float(data['current']['temp_c']) # Температура окружающей среды
        cloud = float(data['current']['cloud'])
        lat = float(data['location']['lat'])  # Широта в радианах
        lon = float(data['location']['lon']) # Долгота в радианах
    except:
        return None
    
    # if not all([data, panel_area, panel_efficiency]):
    #     return None

    # if panel_area <= 0 or panel_efficiency <= 0:
    #     return None

    # if azimuth_angle < 0 or azimuth_angle > 360:
    #     return None

    # if tilt_angle < 0 or tilt_angle > 90:
    #     return None
    
    # print("проверки пройдены")

    # Коррекция мощности на основе температуры панели
    temperature_factor = 1 + temp_coeff * (temp - reference_temp)
    
    # Вычисление времени года на основе localtime_epoch
    localtime_epoch = int(time.mktime(datetime.strptime(data['current']['last_updated'], "%Y-%m-%d %H:%M").timetuple()))
    year_progress = (localtime_epoch % 31536000) / 31536000  # Прогресс года в диапазоне [0, 1]
    # Положительное значение tilt_angle для летнего солнцестояния, отрицательное для зимнего
    tilt_angle = 23.5 * math.cos(2 * math.pi * year_progress)
    
    declination = 23.45 * math.sin(2 * math.pi * (284 + year_progress * 360) / 365)  # Деклинация солнца
    hour_angle = math.radians((localtime_epoch % 86400) / 240 - 180)  # Угол часового пояса
    altitude = math.asin(math.sin(lat) * math.sin(math.radians(declination)) +
                         math.cos(lat) * math.cos(math.radians(declination)) * math.cos(hour_angle))  # Высота солнца

    
    # Проверка типов данных и диапазона значений
    try:
        panel_area = float(panel_area)
        panel_efficiency = float(panel_efficiency)
        if azimuth_angle:
            azimuth_angle = float(azimuth_angle)
        if tilt_angle:
            tilt_angle = float(tilt_angle)
    except ValueError:
        return None
    
    if is_tracking:
        tilt_angle = math.degrees(altitude)  # Следящая панель всегда ориентирована на солнце
        azimuth_angle = math.degrees(math.atan2(-math.sin(hour_angle), math.tan(math.radians(declination)) * math.cos(lat) -
                                math.sin(lat) * math.cos(hour_angle)))  # Азимут солнца
    else:
        # azimuth_angle = 180  # Панель всегда ориентирована на юг
        # tilt_angle = 23.5 * math.cos(2 * math.pi * year_progress)  # Примерное упрощение для фиксированной панели
        try:
            azimuth_angle = float(azimuth_angle)
            tilt_angle = float(tilt_angle)
        except:
            return None


    # Учет углов наклона и азимута
    cos_theta = (math.sin(altitude) * math.sin(math.radians(tilt_angle)) * 
                math.cos(math.radians(azimuth_angle) - math.radians(180)) + 
                math.cos(altitude) * math.cos(math.radians(tilt_angle)))
    
    # Коррекция мощности на основе УФ индекса
    uv_power_correction = uv_index / 10  # Примерный коэффициент коррекции

    # Вычисление выходной мощности
    power_output = uv_power_correction * panel_area * panel_efficiency * temperature_factor * max(0, cos_theta) * (1 - cloud/100)

    return power_output


def calculate_simple_output(data):
    temp_coeff = -0.005
    reference_temp = 25  

    cloud = float(data['cloud'])
    temp = float(data['temp_c'])
    uv_index = float(data['uv'])

    temperature_factor = 1 + temp_coeff * (temp - reference_temp)

    power_output = uv_index * temperature_factor * (1 - cloud/100)

    return power_output