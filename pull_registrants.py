import requests
import json
import time
import math
import os

try:
    f = open("private_key.txt", "r")
    if f:
        pswd = f.readline()
    else:
        raise RuntimeError("Error, an issue occured in reading the private key")
except FileNotFoundError as e:
    print("You must have the private key file to run this program.")
    exit()
except RuntimeError as e:
    print(e)
    exit()

get_url = "https://census.hackku.org/token?username=admin&password={}".format(pswd)

obj = None
token_valid = False
getting_registrants = False
while True:
    try:
        res = requests.get(get_url)
        
        if res:
            obj = json.loads(res.text)
            if obj:
                if not getting_registrants:
                    if "+" in obj["token"]:
                        # Get a new token. For some reason this won't work
                        print("Token has an invalid character. Trying again...")
                    else:
                        print(obj)
                        token_valid = True

                        # Next step: Get the registrants
                        getting_registrants = True
                        get_url = "https://census.hackku.org/registrations?token={}".format(obj["token"])
                        obj = None
                else:
                    # Do whatever you want with the registrants
                    csv_name = str(math.floor(time.time())) + ".csv"
                    if os.path.isdir("registrant_data"):
                        os.makedirs("registrant_data")
                    f = open("registrant_data/{}".format(csv_name), "w")
                    json.dump(obj, f)
                    print("Registrant data saved to {}".format(csv_name))
                    exit()
            else:
                raise RuntimeError("Error parsing response to JSON for {}".format(getting_registrants if "registrants" else "token"))
        else:
            raise RuntimeError("Error getting {}".format(getting_registrants if "registrants" else "token"))
    except Exception as e:
        print(e)
        exit()
