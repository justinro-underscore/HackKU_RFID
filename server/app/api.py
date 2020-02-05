from flask import request, jsonify, Blueprint
from flask_api import status
from app.data import registrant_data, rfid_refrence, schedule_data
from schema import Schema, SchemaError, Optional
from app.api_logging import log_rfid_log
import os
import datetime

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
    except KeyError:
        return 'User at index {} was not found'.format(request.get_json()['r_index']), status.HTTP_404_NOT_FOUND

@api.route("/rfid_get/<rfid>", methods=['GET'])
def get_rfid(rfid):
    if rfid in rfid_refrence:
        return registrant_data[rfid_refrence[rfid]]
    return "No registrants for that defined rfid!"

@api.route("/schedule/", methods=['GET'])
def get_schedule():
    if schedule_data:
        return str(schedule_data)
    else:
        return "No schedule data found"

rfid_log_schema = Schema({'rfid_num': str,
                          Optional('event_num', default=-1): int,
                          Optional('time_stamp', default=''): str})

@api.route("/rfid_log/", methods=['POST'])
def log_rfid():
    try:
        json = rfid_log_schema.validate(request.get_json())

        # msg = ""
        # rfid = json['rfid_num']
        # if rfid in rfid_refrence:
        #     index = rfid_refrence[rfid]
        #     return "RFID num created for {}".format(json['r_index']), status.HTTP_200_OK

        print("RFID scanned: {} @ {}".format(json["rfid_num"], json["time_stamp"]))

        if bool(int(request.args.get("log", default="1"))):
            log_rfid_log(json)

        return "{}".format("Jason Mendoza"), status.HTTP_200_OK

    except SchemaError as err:
        return f'Invalid JSON: {err}', status.HTTP_400_BAD_REQUEST
    except IndexError:
        return 'User at index {} was not found'.format(request.get_json()['r_index']), status.HTTP_404_NOT_FOUND
