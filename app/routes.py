from flask import Blueprint, request, jsonify, render_template
import requests
from database import Database

currency_routes = Blueprint('currency_routes', __name__)

class CurrencyAPI:
    BASE_URL = 'https://v6.exchangerate-api.com/v6/'
    ACCESS_KEY = '09b286905c746676575e5e0a'

    @classmethod
    def fetch_latest_rates(cls, base='USD'):
        url = f"{cls.BASE_URL}{cls.ACCESS_KEY}/latest/{base}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'conversion_rates' not in data:
                raise ValueError('Некорректный ответ от API')
            return base, data['conversion_rates']
        else:
            raise ValueError(f"Ошибка запроса: {response.status_code}")

@currency_routes.route('/')
def index():
    return render_template('index.html')

@currency_routes.route('/api/update_rates', methods=['POST'])
def update_rates():
    data = request.get_json()
    base = data.get('base', 'USD').upper()

    try:
        base, rates = CurrencyAPI.fetch_latest_rates(base)
        Database.update_rates(base, rates)
        return jsonify({'message': f'Курсы обновлены для {base}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@currency_routes.route('/api/last_update', methods=['GET'])
def last_update():
    last = Database.get_last_update()
    return jsonify({'last_update': last})

@currency_routes.route('/api/convert', methods=['POST'])
def convert():
    data = request.get_json()
    base = data.get('base')
    target = data.get('target')
    amount = data.get('amount')

    if not all([base, target, amount]):
        return jsonify({'error': 'Заполните все параметры'}), 400

    try:
        result = Database.convert_currency(base.upper(), target.upper(), float(amount))
        if result is None:
            return jsonify({'error': 'Курс не найден'}), 404
        return jsonify({'converted': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
