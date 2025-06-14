from storage import load_userdata, save_userdata, userdata
from auth import user_registration, user_login
from app_core import menu, create_routine

def login_prompt() -> None:
    user_type = input("Hello! Are you a new or returning user? (n/r): ").strip().lower()
    if user_type in ("n", "new"):
        user_registration()
    elif user_type in ("r", "returning"):
        user_login()
    else:
        print("Invalid input, please enter 'n' for new or 'r' for returning.")
        login_prompt()

if __name__ == "__main__":
    load_userdata()
    login_prompt()


def user_login():
    username = input("Enter username: ").strip().lower()
    password = input("Enter password: ").strip()

    if username in userdata and userdata[username]["password"] == password:
        print("Login successful!")
        menu(username)
    else: 
        print("Invalid credentials. Try again.")
        login_prompt()


def user_registration() -> None:
    username = input("Enter a username: ").strip().lower()
    password = input("Enter a password: ").strip()

    userdata[username] = {"routine": []}

    save_userdata()
    create_routine(username)


    save_userdata()
    create_routine(username)

