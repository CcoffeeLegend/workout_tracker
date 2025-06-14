from storage import userdata, load_userdata, save_userdata
from main import menu, create_routine

def user_login():
    global userdata
    username = input("Enter username: ").strip().lower()  # ← normalize
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

def user_registration() -> None:
    username = input("Enter a username: ").strip().lower()  # ← normalize
    password = input("Enter a password: ").strip()

    if username in userdata:
        print("Username already taken. Try another.")
        return user_registration()

    userdata[username] = {
        "password": password,
        "routine": []
    }

    save_userdata()
    create_routine(username)

