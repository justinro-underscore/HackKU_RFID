import requests
import os
import json

try:
    f = open("../commands.txt", "r")
    commands = f.readlines()
    if len(commands) == 0:
        raise Exception()
except:
    print("No updates needed!")
    exit()

f = open('../../local_data/api_key.txt', 'r')
token = f.read()
f.close()
base_url = "http://127.0.0.1:5000/token={}/".format(token)

for command in commands:
    (ext, data) = command.split(" | ")
    print(json.loads(data))
    res = requests.post(base_url + ext, json=json.loads(data), params={'log': 0})
    if not res:
        print("Error! Update did not go through!")
