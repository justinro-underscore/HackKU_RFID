import requests
import json
from app.pull_schedule import retrieve_schedule

def get_token():
    try:
        f = open("../local_data/private_key.txt", "r")
        if f:
            pswd = f.readline()
        else:
            raise RuntimeError("Error, an issue occured in reading the private key")
    except FileNotFoundError as e:
        raise Exception("You must have the private key file to run this program.")
    except RuntimeError as e:
        raise Exception(e)

    get_url = "https://census.hackku.org/token?username=admin&password={}".format(pswd)

    for _ in range(10):
        res = requests.get(get_url)

        if res:
            obj = json.loads(res.text)
            if obj:
                if "+" in obj["token"]:
                    # Get a new token. For some reason this won't work
                    print("Token has an invalid character. Trying again...")
                else:
                    return obj["token"]
    raise RuntimeError("Error, could not get token")

def pull_schedule():
    return retrieve_schedule()

class data_holder:
    def __init__(self):
        self.token = get_token()
        self.schedule_data = pull_schedule()
        self.rfid_to_student = dict()
        self.rfid_to_event = dict()

data_h = data_holder()

def get_schedule():
    if data_h.schedule_data:
        return json.dumps(data_h.schedule_data)
    try:
        return json.dumps(pull_schedule())
    except Exception as e:
        print("Could not pull schedule data!")
        print("Error: \"{}\"".format(e))

def retrieve_student(rfid):
    get_url = "https://census.hackku.org/rfid"
    print(rfid.strip())

    for i in range(2):
        if i == 1:
            data_h.token = get_token()
        res = requests.get(get_url, params={"token": data_h.token, "rfid": rfid.strip()})
        if res:
            return json.loads(res.text)
        elif i == 1:
            raise RuntimeError("Error, could not find student")

def get_student(rfid):
    if rfid in data_h.rfid_to_student:
        return json.dumps(data_h.rfid_to_student[rfid])
    try:
        data_h.rfid_to_student[rfid] = retrieve_student(rfid)
        return json.dumps(data_h.rfid_to_student[rfid])
    except Exception as e:
        raise Exception(e)

def log_rfid_event(rfid, event_num):
    if rfid in data_h.rfid_to_event:
        data_h.rfid_to_event[rfid].append(event_num)
    else:
        data_h.rfid_to_event[rfid] = [event_num]

def get_rfid_logs(rfid):
    if rfid in data_h.rfid_to_student:
        event_counts = dict()
        for event_log in data_h.rfid_to_event[rfid]:
            if event_log in event_counts:
                event_counts[event_log] += 1
            else:
                event_counts[event_log] = 1

        res = dict()
        for event_num, val in event_counts.items():
            res[data_h.schedule_data[event_num]["name"]] = val
        return json.dumps(res)
    return "RFID number not registered"

def get_event_logs(event_num):
    try:
        event_num = int(event_num)
    except:
        return "Invalid event number (not a valid integer)"
    if event_num < len(data_h.schedule_data):
        count = 0
        for event_log_arr in data_h.rfid_to_event.values():
            for event_log in event_log_arr:
                if event_log == event_num:
                    count += 1
        return "{} logs for event {}".format(count, data_h.schedule_data[event_num])
    return "Invalid event number (not a valid event index)"