from routine import save_userdata, userdata

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

        while True:
            success = input("Did you complete all sets and reps successfully? (yes/no): ").strip().lower()
            if success in ['yes', 'y']:
                increment = exercise.get("auto_increment", 0)
                if increment > 0:
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
