from flask import request, jsonify, Blueprint
from flask_api import status
from app.data import registrant_data, rfid_refrence
from schema import Schema, SchemaError

api = Blueprint("api", __name__)

@api.route("/", methods=['GET'])
def test():
    return "It works!"

@api.route("/registrants/", methods=['GET'])
def get_registrants():
    if registrant_data:
        return str(registrant_data)
    return "No registrants available! Please check the app."

rfid_set_schema = Schema({'rfid_num': str,
                          'r_index': int})

@api.route('/rfid_set/', methods=['POST'])
def set_registrant_rfid():
    try:
        json = rfid_set_schema.validate(request.get_json())

        msg = ""
        rfid = json['rfid_num']
        if rfid in rfid_refrence and rfid_refrence[rfid] != json['r_index']:
            msg += "WARNING: RFID reference overwritten."
        rfid_refrence[rfid] = json['r_index']

        return "RFID num created for {}".format(json['r_index']), status.HTTP_201_CREATED

    except SchemaError as err:
        return f'Invalid JSON: {err}', status.HTTP_400_BAD_REQUEST
    except IndexError:
        return 'User at index {} was not found'.format(request.get_json()['r_index']), status.HTTP_404_NOT_FOUND

@api.route("/rfid_get/<rfid>", methods=['GET'])
def get_rfid(rfid):
    if rfid in rfid_refrence:
        return registrant_data[rfid_refrence[rfid]]
    return "No registrants for that defined rfid!"