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
    menu(username) 


def add_exercise(username: str) -> None:
    #This function adds exercises to the routine
    exercise = input("What exercise would you like to do?").strip()
    sets = int(input("How many sets would you like to do? ").strip())
    reps = int(input("How many reps would you like to do in each set? ").strip())
    weights = []
    for i in range(1, sets + 1):
        weight = int(input(f"Enter weight for set {i}: ").strip())
        weights.append(weight)

    while True:
        try:
            auto_inc = int(input("Enter auto-increment weight for this exercise (lbs): ").strip())
            if auto_inc >= 0:
                break  # exit loop if input is valid (zero or positive integer)
            else:
                print("Please enter zero or a positive integer.")
        except ValueError:
            print("Invalid input; please enter a number.")

    print(f"So you'd like to do {sets} sets of {reps} reps of {exercise} with auto-increment {auto_inc} lbs?")
    add_confirm = input("Confirm (yes/no): " ).strip()
    if add_confirm.lower() in ['yes', 'y']:
        userdata[username]["routine"].append({
            "exercise": exercise,
            "sets": sets,
            "reps": reps,
            "weights": weights,
            "auto_increment": auto_inc   # <-- added here
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
        print("5. Remove exercise")
        print("6. Edit exercise")


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
        elif choice == "5":
            remove_exercise(username)
        elif choice == "6":
            edit_exercise(username)
            break
        else:
            print("Invalid choice. Try again.")


def remove_exercise(username: str) -> None:
    routine = userdata[username]["routine"]
    if not routine:
        print("No exercises to remove.")
        return

    print("Select the number of the exercise to remove:")
    for i, exercise in enumerate(routine, start=1):
        print(f"{i}. {exercise['exercise']}")

    try:
        choice = int(input("Enter choice: "))
        if 1 <= choice <= len(routine):
            removed = routine.pop(choice - 1)
            save_userdata()
            print(f"{removed['exercise']} removed.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Must be a number.")

def edit_exercise(username: str) -> None:
    routine = userdata[username]["routine"]
    if not routine:
        print("No exercises to edit.")
        return

    print("Select the number of the exercise to edit:")
    for i, exercise in enumerate(routine, start=1):
        print(f"{i}. {exercise['exercise']}")

    try:
        choice = int(input("Enter choice: "))
        if 1 <= choice <= len(routine):
            ex = routine[choice - 1]
            print(f"Editing {ex['exercise']}")
            sets = int(input("New number of sets: "))
            reps = int(input("New number of reps: "))
            weights = []
            for i in range(1, sets + 1):
                weight = int(input(f"Enter weight for set {i}: "))
                weights.append(weight)

            while True:
                try:
                    auto_inc = int(input("New auto-increment weight for this exercise (lbs): ").strip())
                    if auto_inc >= 0:
                        break
                    else:
                        print("Please enter zero or a positive integer.")
                except ValueError:
                    print("Invalid input; please enter a number.")


            ex["sets"], ex["reps"], ex["weights"], ex["auto_increment"] = sets, reps, weights, auto_inc
            save_userdata()
            print("Exercise updated.")
            menu(username)

        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")


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

        # Ask if exercise was completed successfully
        while True:
            success = input("Did you complete all sets and reps successfully? (yes/no): ").strip().lower()
            if success in ['yes', 'y']:
                # Only increment if auto_increment exists and > 0
                increment = exercise.get("auto_increment", 0)
                if increment > 0:
                    # Increase each set's weight by increment
                    exercise["weights"] = [w + increment for w in exercise["weights"]]
                    print(f"Weights increased by {increment} lbs for {exercise['exercise']}.")
                break
            elif success in ['no', 'n']:
                print(f"No weight increase for {exercise['exercise']}.")
                break
            else:
                print("Invalid input. Please enter yes or no.")

    save_userdata()
    print("Workout complete!")



if __name__ == "__main__":
    load_userdata()
    login_prompt()