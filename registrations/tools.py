import requests
import json
import urllib.parse

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

def get_registrant(email, token, encode_email=False):
    get_url = "https://census.hackku.org/registrant"

    if encode_email:
        email = urllib.parse.quote(email)

    res = requests.get(get_url, params={"token": token, "email": email})
    if res:
        return json.loads(res.text)
    else:
        raise RuntimeError("Error, could not find email")

def set_registrant_rfid(email, token, rfid, encode_email=False):
    post_url = "https://census.hackku.org/rfid"

    if encode_email:
        email = urllib.parse.quote(email)

    res = requests.post(post_url, params={"token": token, "email": email, "rfid": rfid})
    if not res:
        raise RuntimeError("Error, could not set RFID")
