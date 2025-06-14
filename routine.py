from storage import userdata, save_userdata

def create_routine(username):
    add_exercise(username)
    menu(username)

def add_exercise(username):
    exercise = input("What exercise would you like to do? ").strip()
    sets = int(input("How many sets? ").strip())
    reps = int(input("How many reps per set? ").strip())
    weights = [int(input(f"Weight for set {i+1}: ").strip()) for i in range(sets)]

    while True:
        try:
            auto_inc = int(input("Enter auto-increment weight (lbs): ").strip())
            if auto_inc >= 0:
                break
            else:
                print("Enter zero or a positive number.")
        except ValueError:
            print("Invalid number.")

    print(f"{sets} sets of {reps} reps of {exercise} with auto-increment {auto_inc} lbs.")
    confirm = input("Confirm? (yes/no): ").strip().lower()
    if confirm in ['yes', 'y']:
        userdata[username]["routine"].append({
            "exercise": exercise,
            "sets": sets,
            "reps": reps,
            "weights": weights,
            "auto_increment": auto_inc
        })
        save_userdata()

        if input("Add another exercise? (yes/no): ").strip().lower() in ['yes', 'y']:
            add_exercise(username)

def remove_exercise(username):
    routine = userdata[username]["routine"]
    if not routine:
        print("No exercises to remove.")
        return
    print("Which exercise to remove?")
    for i, ex in enumerate(routine, 1):
        print(f"{i}. {ex['exercise']}")
    try:
        idx = int(input("Choice: ")) - 1
        if 0 <= idx < len(routine):
            removed = routine.pop(idx)
            save_userdata()
            print(f"Removed {removed['exercise']}.")
    except ValueError:
        print("Invalid input.")

def edit_exercise(username):
    routine = userdata[username]["routine"]
    if not routine:
        print("No exercises to edit.")
        return
    print("Which exercise to edit?")
    for i, ex in enumerate(routine, 1):
        print(f"{i}. {ex['exercise']}")
    try:
        idx = int(input("Choice: ")) - 1
        ex = routine[idx]
        sets = int(input("New sets: "))
        reps = int(input("New reps: "))
        weights = [int(input(f"Weight for set {i+1}: ")) for i in range(sets)]
        while True:
            try:
                auto_inc = int(input("New auto-increment: "))
                if auto_inc >= 0:
                    break
            except ValueError:
                print("Invalid.")
        ex.update({"sets": sets, "reps": reps, "weights": weights, "auto_increment": auto_inc})
        save_userdata()
        print("Exercise updated.")
    except (ValueError, IndexError):
        print("Invalid selection.")

def view_routine(username):
    routine = userdata[username].get("routine", [])
    if not routine:
        print("Routine is empty.")
        return
    for ex in routine:
        print(f"- {ex['exercise']}: {ex['sets']} sets x {ex['reps']} reps")
        print("  Weights:", ', '.join(str(w) for w in ex['weights']))

def start_workout(username):
    routine = userdata[username].get("routine", [])
    if not routine:
        print("No routine found.")
        return
    print("Starting workout...")
    for ex in routine:
        print(f"\n{ex['exercise']}")
        for i, weight in enumerate(ex['weights'], 1):
            print(f"Set {i}: {ex['reps']} reps at {weight} lbs")
            input("Type 'done' to continue: ")
        while True:
            complete = input("Did you complete all sets? (yes/no): ").strip().lower()
            if complete in ['yes', 'y']:
                inc = ex.get("auto_increment", 0)
                if inc > 0:
                    ex['weights'] = [w + inc for w in ex['weights']]
                    print(f"Increased by {inc} lbs.")
                break
            elif complete in ['no', 'n']:
                print("No increment applied.")
                break
    save_userdata()
    print("Workout complete!")

def menu(username: str) -> None:
    while True:
        print(f"\nWelcome, {username}! What would you like to do?")
        print("1. Start workout")
        print("2. Add exercise")
        print("3. View routine")
        print("4. Remove exercise")
        print("5. Edit exercise")
        print("6. Quit")

        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            start_workout(username)
        elif choice == "2":
            add_exercise(username)
        elif choice == "3":
            view_routine(username)
        elif choice == "4":
            remove_exercise(username)
        elif choice == "5":
            edit_exercise(username)
        elif choice == "6":
            print("Goodbye!")
            exit()
        else:
            print("Invalid choice. Try again.")
