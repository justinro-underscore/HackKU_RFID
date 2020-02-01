from flask import Flask
from app.api import api
import random
import string

def app_factory():

    app = Flask(__name__)

    try:
        f = open('../private_key.txt', 'r')
        token = f.read()
        f.close()

        app.register_blueprint(api, url_prefix='/token={}'.format(token))

        return app
    except Exception as e:
        print(e)
        print("Error occurred! Could not start app")
        return None
