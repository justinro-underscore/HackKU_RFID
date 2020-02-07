from flask import request, jsonify, Blueprint
from flask_api import status
from app.data import registrant_data, schedule_data, rfid_to_student, rfid_to_event
from schema import Schema, SchemaError, Optional
from app.api_logging import log_rfid_set, log_rfid_log
import json
import os
import datetime

api = Blueprint("api", __name__)

@api.route("/", methods=['GET'])
def test():
    return "It works!"

@api.route("/registrants/", methods=['GET'])
def get_registrants():
    if registrant_data:
        return json.dumps(registrant_data)
    return "No registrants available! Please check the app."

rfid_set_schema = Schema({'rfid_num': str,
                          'r_index': int})

@api.route("/schedule/", methods=['GET'])
def get_schedule():
    if schedule_data:
        return json.dumps(schedule_data)
    else:
        return "No schedule data found"

@api.route('/rfid_set/', methods=['POST'])
def set_registrant_rfid():
    try:
        json_obj = rfid_set_schema.validate(request.get_json())

        msg = ""
        rfid = json_obj['rfid_num']
        if rfid in rfid_to_student and rfid_to_student[rfid] != json_obj['r_index']:
            msg += "WARNING: RFID reference overwritten."
        rfid_to_student[rfid] = json_obj['r_index']
        rfid_to_event[rfid] = [] # TODO Add check if there is already data

        if bool(int(request.args.get("log", default="1"))):
            log_rfid_set(json_obj)
        return "RFID num created for {}".format(json_obj['r_index']), status.HTTP_201_CREATED

    except SchemaError as err:
        return f'Invalid JSON: {err}', status.HTTP_400_BAD_REQUEST
    except KeyError:
        return 'User at index {} was not found'.format(request.get_json()['r_index']), status.HTTP_404_NOT_FOUND

@api.route("/rfid_get/<rfid>", methods=['GET'])
def get_rfid(rfid):
    if rfid in rfid_to_student:
        return json.dumps(registrant_data[rfid_to_student[rfid]])
    return "RFID number not registered"

rfid_log_schema = Schema({'rfid_num': str,
                          'event_num': int})

@api.route("/rfid_log/", methods=['POST'])
def log_rfid():
    try:
        json_obj = rfid_log_schema.validate(request.get_json())

        rfid = json_obj['rfid_num']
        rfid_to_event[rfid].append(json_obj['event_num'])

        if bool(int(request.args.get("log", default="1"))):
            log_rfid_log(json_obj)
        # else:
        #     return "Student {} logged for event {}".format(rfid_to_student[rfid], schedule_data[json_obj['event_num']]), status.HTTP_200_OK
        print("Student {} logged for event {}".format(registrant_data[rfid_to_student[rfid]]["first_name"], schedule_data[json_obj['event_num']]["name"]))
        return json.dumps(registrant_data[rfid_to_student[rfid]]), status.HTTP_200_OK
    except SchemaError as err:
        return f'Invalid JSON: {err}', status.HTTP_400_BAD_REQUEST
    except KeyError:
        print('RFID {} has not been registered'.format(request.get_json()['rfid_num']))
        return 'RFID {} has not been registered'.format(request.get_json()['rfid_num']), status.HTTP_404_NOT_FOUND

@api.route("/rfid_logs/<rfid>", methods=['GET'])
def get_rfid_log(rfid):
    if rfid in rfid_to_student:
        event_counts = dict()
        for event_log in rfid_to_event[rfid]:
            if event_log in event_counts:
                event_counts[event_log] += 1
            else:
                event_counts[event_log] = 1

        res = dict()
        for event_num, val in event_counts.items():
            res[schedule_data[event_num]["name"]] = val
        return json.dumps(res)
    return "RFID number not registered"

@api.route("/event_logs/<event_num>", methods=['GET'])
def get_event_logs(event_num):
    try:
        event_num = int(event_num)
    except:
        return "Invalid event number (not a valid integer)"
    if event_num < len(schedule_data):
        count = 0
        for event_log_arr in rfid_to_event.values():
            for event_log in event_log_arr:
                if event_log == event_num:
                    count += 1
        return "{} logs for event {}".format(count, schedule_data[event_num])
    return "Invalid event number (not a valid event index)"
