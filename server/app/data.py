from app.pull_registrants import pull_registrants, retrieve_registrants
from app.pull_schedule import get_schedule

registrant_data = None
try:
    registrant_data = pull_registrants()
except Exception as e:
    print("Could not pull registration data!")
    print("Error: \"{}\"".format(e))
    try:
        print("Attempting to pull the most recent registration data...")
        registrant_data = retrieve_registrants()
    except Exception as e:
        print("Could not retrieve registration data")
        print(e)
        raise Exception("Cannot start app")

schedule_data = None
try:
    schedule_data = get_schedule()
except Exception as e:
    print("Could not pull schedule data!")
    print("Error: \"{}\"".format(e))

rfid_to_student = dict()
rfid_to_event = dict()