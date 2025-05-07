import json
import sqlite3
from datetime import datetime

class Database:
    DB_NAME = 'currency.db'

    @classmethod
    def init_db(cls):
        conn = sqlite3.connect(cls.DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rates (
                base TEXT,
                conversion_rates TEXT,
                updated_at TEXT
            )
        ''')
        conn.commit()
        conn.close()

    @classmethod
    def update_rates(cls, base, conversion_rates):
        now = datetime.utcnow().isoformat()
        conn = sqlite3.connect(cls.DB_NAME)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM rates WHERE base = ?', (base,))
        print("conversion_rates:", conversion_rates)
        for target, rate in conversion_rates.items():
            cursor.execute(
                'INSERT INTO rates (base, conversion_rates, updated_at) VALUES (?, ?, ?)',
                (base, json.dumps(conversion_rates), now)
            )
        conn.commit()
        conn.close()

    @classmethod
    def get_last_update(cls):
        conn = sqlite3.connect(cls.DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(updated_at) FROM rates')
        result = cursor.fetchone()[0]
        conn.close()
        return result

    @classmethod
    def convert_currency(cls, base, target, amount):
        conn = sqlite3.connect(cls.DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('SELECT conversion_rates FROM rates WHERE base = ?', (base,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            raw_conversion_rates = row[0]
            try:
                conversion_rates = json.loads(raw_conversion_rates)
                rate = conversion_rates.get(target)
                
                if rate is not None:
                    converted_amount = round(amount * float(rate), 4)
                    return converted_amount
                else:
                    return f'Нет курса обмена для валюты "{target}"'
            except Exception as e:
                return f'Ошибка обработки данных: {str(e)}'
        else:
            return f'Нет записей для базовой валюты "{base}"'