from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

def get_weather(location, date):
  
    forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={your_api}'
    response = requests.get(forecast_url)
    if response.status_code == 200:
        weather_data = response.json()
        # дістаємо список прогнозів погоди і шукаємо потрібний
        forecast_list = weather_data['list']
        target_date = datetime.fromisoformat(date)
        target_date += timedelta(hours=12) 
        for forecast in forecast_list:
            forecast_date = datetime.fromtimestamp(forecast['dt'])
            if forecast_date == target_date:
                temperature = forecast['main']['temp'] - 273.15 # конвертуємо в градуси по Цельсію
                wind_speed = forecast['wind']['speed'] * 3.6 # конвертуємо з гамбургерів/одного_орла у км/годину 
                pressure = forecast['main']['pressure']
                humidity = forecast['main']['humidity']
                # робимо респонс
                response_data = {
                    'temp_c': temperature,
                    'wind_kph': wind_speed,
                    'pressure_mb': pressure,
                    'humidity': humidity
                }
                return response_data
        return {'error': 'Unable to get weather data for the specified date'}
    else:
        return {'error': 'Unable to get weather data'}

@app.route('/weather', methods=['POST'])
def weather_endpoint():
    data = request.get_json()
    token = data['token']
    requester_name = data['requester_name']
    location = data['location']
    date = data['date']

    # перевіряємо наш токен
    if token != 'my secret token':
        return jsonify({'error': 'Invalid token'})

    #запит на погоду
    weather_data = get_weather(location, date)
    if 'error' in weather_data:
        return jsonify(weather_data)
    else:
        # робимо респонс
        response_data = {
            'requester_name': requester_name,
            'timestamp': datetime.utcnow().isoformat() + 'Z',  
            'location': location,
            'date': date,
            'weather': weather_data
        }
        return jsonify(response_data)

