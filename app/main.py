from flask import Flask
from routes import currency_routes
from database import Database


def create_app():
    app = Flask(__name__,
                static_folder='static',
                template_folder='templates')
    app.config['JSON_SORT_KEYS'] = False

    Database.init_db()

    app.register_blueprint(currency_routes)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)