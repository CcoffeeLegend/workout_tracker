userdata = {}
from routine import add_exercise

def user_registration() -> None:
    global userdata
    username = input("Enter a username: ").strip().lower()
    password = input("Enter a password: ").strip()

    if username in userdata:
        print("Username already exists. Please choose another.")
        return

    userdata[username] = {
        "password": password,
        "routine": []
    }
    save_userdata()
    create_routine(username)

def save_userdata():
    global userdata
    import json
    with open("userdata.json", "w") as file:
        json.dump(userdata, file, indent=4)

def create_routine(username: str) -> None:
    global userdata
    add_exercise(username)
