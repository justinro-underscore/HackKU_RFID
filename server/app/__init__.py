from flask import Flask
from app.api import api
from app.api_logging import start_logging
import random
import string

def app_factory():
    app = Flask(__name__)

    try:
        f = open('../local_data/private_key.txt', 'r')
        token = f.read()
        f.close()

        app.register_blueprint(api, url_prefix='/token={}'.format(token))

        start_logging()

        return app
    except Exception as e:
        print(e)
        print("Error occurred! Could not start app")
        return None
