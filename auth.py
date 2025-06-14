from storage import userdata, save_userdata
from routine import create_routine, menu

def user_login():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if username in userdata and userdata[username]["password"] == password:
        print("Login successful!")
        menu(username)
    else:
        print("Invalid credentials. Try again.")
        login_prompt()

def login_prompt():
    newuser = input("Hello! Are you a new or returning user? ").strip()
    if newuser == "new":
        user_registration()
    else:
        user_login()

def user_registration():
    username = input("Enter a username: ").strip()
    password = input("Enter a password: ").strip()

    userdata[username] = {
        "password": password,
        "routine": []
    }
    save_userdata()
    create_routine(username)
