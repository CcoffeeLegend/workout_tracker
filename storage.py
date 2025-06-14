import json

userdata = {}

def load_userdata():
    global userdata
    try:
        with open("userdata.json", "r") as file:
            userdata = json.load(file)
    except FileNotFoundError:
        userdata = {}
    return userdata

def save_userdata():
    global userdata
    with open("userdata.json", "w") as file:
        json.dump(userdata, file, indent=4)
