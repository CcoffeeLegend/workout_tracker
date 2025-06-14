import json
from storage import userdata, save_userdata
from utils import yes_no_prompt

def load_userdata() -> dict:
    global userdata
    try:
        with open("userdata.json", "r") as file:
            userdata = json.load(file)
            return userdata
    except FileNotFoundError:
        userdata = {}
        return userdata

def save_userdata() -> None:
    global userdata
    with open("userdata.json", "w") as file:
        json.dump(userdata, file, indent=4)

def add_exercise(username: str) -> None:
    exercise = input("What exercise would you like to do? ").strip()
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
                break
            else:
                print("Please enter zero or a positive integer.")
        except ValueError:
            print("Invalid input; please enter a number.")

    print(f"So you'd like to do {sets} sets of {reps} reps of {exercise} with auto-increment {auto_inc} lbs?")
    if yes_no_prompt("Confirm (yes/no): "):
        userdata[username]["routine"].append({
            "exercise": exercise,
            "sets": sets,
            "reps": reps,
            "weights": weights,
            "auto_increment": auto_inc
        })
        save_userdata()
        if yes_no_prompt("Would you like to add another exercise? (yes/no): "):
            add_exercise(username)
    # else: return

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
