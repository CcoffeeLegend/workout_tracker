from app_core import menu, create_routine

def user_login():
    username = input("Enter username: ").strip().lower()
    password = input("Enter password: ").strip()
    if username in userdata and userdata[username]["password"] == password:
        print("Login successful!")
        menu(username)
    else:
        print("Invalid credentials. Try again.")
        user_login()

def user_registration():
    username = input("Enter a username: ").strip().lower()
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

