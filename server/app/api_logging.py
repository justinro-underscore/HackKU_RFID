import os
import json

class logger_cls:
    def __init__(self):
        self.logger = None

logger_obj = logger_cls()
log_rfid_set = lambda json_obj: logger_obj.logger.write("rfid_set/ | {}\n".format(json.dumps(json_obj)))
log_rfid_log = lambda json_obj: logger_obj.logger.write("rfid_log/ | {}\n".format(json.dumps(json_obj)))

def start_logging():
    if os.path.exists("rfid_log.txt"):
        logger_obj.logger = open("rfid_log.txt", "r")
        commands = logger_obj.logger.readlines()
        logger_obj.logger.close()

        if len(commands) > 0:
            new_file = open("commands.txt", "w")
            new_file.writelines(commands)
            new_file.close()
            print("{0}\nWarning! Logger already has commands logged. Please run the update_api.py script before any commands are sent to the server!\n{0}".format("~-" * 30))
    logger_obj.logger = open("rfid_log.txt", "a")
    print("Logging started!")
