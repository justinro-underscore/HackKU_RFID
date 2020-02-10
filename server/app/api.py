from flask import request, jsonify, Blueprint
from flask_api import status
from app.tools import get_student, log_rfid_event, get_schedule, get_rfid_logs, get_event_logs
# from app.data import registrant_data, schedule_data, rfid_to_student, rfid_to_event
from schema import Schema, SchemaError
from app.api_logging import log_rfid_log
import json
import os
import datetime

api = Blueprint("api", __name__)

@api.route("/", methods=['GET'])
def test():
    return "It works!"

@api.route("/schedule/", methods=['GET'])
def get_schedule_data():
    return get_schedule()

@api.route("/rfid_get/<rfid>", methods=['GET'])
def get_rfid(rfid):
    try:
        return json.dumps(get_student(rfid))
    except:
        return "Could not find student with RFID number {}".format(rfid)

rfid_log_schema = Schema({'rfid_num': str,
                          'event_num': int})

@api.route("/rfid_log/", methods=['POST'])
def log_rfid():
    try:
        json_obj = rfid_log_schema.validate(request.get_json())

        rfid = json_obj['rfid_num']

        try:
            student = json.loads(get_student(rfid))
        except:
            return "RFID {} has not been registered.".format(rfid), status.HTTP_404_NOT_FOUND

        log_rfid_event(rfid, json_obj['event_num'])

        if bool(int(request.args.get("log", default="1"))):
            log_rfid_log(json_obj)
        # else:
        #     return "Student {} logged for event {}".format(rfid_to_student[rfid], schedule_data[json_obj['event_num']]), status.HTTP_200_OK
        print("Student {} logged for event {}".format(student["first_name"], json.loads(get_schedule())[int(json_obj['event_num'])]["name"]))
        return student, status.HTTP_200_OK
    except SchemaError as err:
        return f'Invalid JSON: {err}', status.HTTP_400_BAD_REQUEST
    except KeyError:
        print('RFID {} has not been registered'.format(request.get_json()['rfid_num']))
        return 'RFID {} has not been registered'.format(request.get_json()['rfid_num']), status.HTTP_404_NOT_FOUND

@api.route("/rfid_logs/<rfid>", methods=['GET'])
def get_rfid_logs_data(rfid):
    return get_rfid_logs(rfid)

@api.route("/event_logs/<event_num>", methods=['GET'])
def get_event_logs_data(event_num):
    return get_event_logs(event_num)
