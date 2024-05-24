import math

def calculate_solar_output(area, efficiency, solar_radiation, temperature, temp_coefficient, loss_factor):
    """
    Рассчитывает выход солнечных панелей.
    
    Параметры:
    area (float): Площадь панели в м².
    efficiency (float): Эффективность панели (в долях единицы, например, 0.18 для 18%).
    solar_radiation (float): Солнечная радиация в кВт·ч/м².
    temperature (float): Температура окружающей среды в °C.
    temp_coefficient (float): Температурный коэффициент (например, -0.005 для -0.5% на каждый градус выше 25°C).
    loss_factor (float): Общий коэффициент потерь (например, 0.9 для 10% потерь).
    
    Возвращает:
    float: Производимая энергия в кВт·ч.
    """
    
    # Температурная корректировка эффективности
    adjusted_efficiency = efficiency * (1 + temp_coefficient * (temperature - 25))
    
    # Производимая энергия до учета потерь
    energy_before_losses = area * solar_radiation * adjusted_efficiency
    
    # Окончательная производимая энергия с учетом потерь
    final_energy = energy_before_losses * loss_factor
    
    return final_energy


def calculate_output(area, efficiency, solar_irradiance, temperature, tilt_angle, orientation):
    efficiency /= 100  # Эффективность преобразуем в доли единицы

    # Коррекция эффективности в зависимости от температуры
    temperature_coefficient = -0.005  # Допустимая поправка на температуру
    nominal_temperature = 25  # Номинальная температура в градусах Цельсия
    efficiency *= 1 + temperature_coefficient * (temperature - nominal_temperature)

    # Коррекция на угол наклона и ориентацию
    optimal_tilt_angle = 30  # Допустим оптимальный угол наклона
    optimal_orientation = 180  # Оптимальная ориентация на юг
    tilt_loss = math.cos(math.radians(tilt_angle - optimal_tilt_angle))
    orientation_loss = math.cos(math.radians(orientation - optimal_orientation))

    total_loss = tilt_loss * orientation_loss

    return area * efficiency * solar_irradiance * total_loss