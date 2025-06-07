import json

userdata = {}

def load_userdata():
    try:
        with open("userdata.json", "r") as file:
            global userdata
            userdata = json.load(file)
            return userdata
    except FileNotFoundError:
        return {}
    
def save_userdata():
    global userdata
    with open("userdata.json", "w") as file:
        json.dump(userdata, file, indent=4)

def user_login():
    global userdata
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if username in userdata and userdata[username]["password"] == password:
        print("Login successful!")
        menu(username)
    else: 
        print("Invalid credentials. Try again.")
        login_prompt()


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

    save_userdata()
    create_routine(username)


def create_routine(username: str) -> None:
    #This function runs for new users
    add_exercise(username)


def add_exercise(username: str) -> None:
    #This function adds exercises to the routine
    exercise = input("What exercise would you like to do?").strip()
    sets = int(input("How many sets would you like to do? ").strip())
    reps = int(input("How many reps would you like to do in each set? ").strip())
    weights = []
    for i in range(1, sets + 1):
        weight = int(input(f"Enter weight for set {i}: ").strip())
        weights.append(weight)

    print(f"So you'd like to do {sets} sets of {reps} reps of {exercise}?")
    add_confirm = input("Confirm (yes/no): " ).strip()
    if add_confirm.lower() in ['yes', 'y']:
        userdata[username]["routine"].append({
        "exercise": exercise,
        "sets": sets,
        "reps": reps,
        "weights": weights            
        })

        save_userdata()

        print(f"{exercise} added. Would you like to add another exercise?")
        add_another = input("Confirm (yes/no): ").strip()
        if add_another.lower() in ['yes', 'y']:
            add_exercise(username)
        else:
            return
    elif add_confirm.lower() in ['no', 'n']:
        return
    else:
        input("Invalid input. Try again.").strip()
        add_exercise(username)

def menu(username: str) -> None:
    while True:
        print(f"\nWelcome, {username}! What would you like to do?")
        print("1. Start workout")
        print("2. Add exercise")
        print("3. View routine")
        print("4. Quit")

        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            start_workout(username)
        elif choice == "2":
            add_exercise(username)
        elif choice == "3":
            view_routine(username)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

def view_routine(username: str) -> None:
    routine = userdata[username].get("routine", [])
    if not routine:
        print("No exercises in your routine.")
        return

    print("\nYour Routine:")
    for exercise in routine:
        print(f"- {exercise['exercise']}: {exercise['sets']} sets x {exercise['reps']} reps")
        print("  Weights:", ", ".join(str(w) for w in exercise['weights']))

def start_workout(username: str) -> None:
    routine = userdata[username].get("routine", [])
    if not routine:
        print("No exercises found. Add some first.")
        return

    print("\nStarting workout!")
    for exercise in routine:
        print(f"\n{exercise['exercise']}")
        for i, weight in enumerate(exercise['weights'], start=1):
            print(f"Set {i}: {exercise['reps']} reps at {weight} lbs")
            input("Type 'done' when complete: ")
    print("Workout complete!")

if __name__ == "__main__":
    load_userdata()
    login_prompt()