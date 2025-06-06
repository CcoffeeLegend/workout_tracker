import json

userdata = {}

def load_users():
    try:
        with open("userdata.json", "r") as file:
            global userdata
            userdata = json.load(file)
            return userdata
    except FileNotFoundError:
        return {}
    
def save_users():
    global userdata
    with open("userdata.json", "w") as file:
        json.dump(userdata, file, indent=4)

def user_login():
    global userdata
    input("Enter username: ").strip()
    input("Enter password: ").strip()


def login_prompt() -> None:
    #This function runs on startup, checks whether the user is new or not, then runs user_registration or  user_login respectively            

    newuser = input("Hello! Are you a new or returning user?").strip()
    if newuser == "new":
        user_registration()
    else: 
        user_login()


def user_registration() -> None:
    #This function runs for new users, prompting for username and password, saving that to json, then heading to create_routine    

    username = input("Enter a username: ").strip()
    password = input("Enter a password: ").strip()

    userdata[username] = {
        "password": password,
        "routine": []
    }

    save_users()
    create_routine(username)


def create_routine(username: str) -> None:
    #This function runs for new users
    add_exercise(username)


def add_exercise(username: str) -> None:
    #This function adds exercises to the routine
    print("What exercise would you like to do?")
    exercise = input().strip()
        
    sets = int(input("How many sets would you like to do? ").strip())
    reps = int(input("How many reps in each set? ").strip())
    weights = []
    for i in range(1, sets + 1):
        weight = int(input(f"Enter weight for set {i}: ").strip())
        weights.append(weight)

    print(f"So you'd like to do {sets} sets of {reps} reps of {exercise}?")
    add_confirm = input("Confirm (yes/no): " ).strip()
    if add_confirm.lower() in ['yes', 'y']:
        #implement adding the exercise to the routine here
        print(f"{exercise} added. Would you like to add another exercise?")
        add_another = input("Confirm (yes/no): ").strip()
        if add_another.lower() in ['yes', 'y']:
            add_exercise(username)
        else:
            menu(username)
    else:
        menu(username)
