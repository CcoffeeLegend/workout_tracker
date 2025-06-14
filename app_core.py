from routine import add_exercise, remove_exercise, edit_exercise, view_routine
from workout import start_workout

def menu(username: str):
    while True:
        print("\nMenu:")
        print("1. Start workout")
        print("2. Add exercise")
        print("3. Remove exercise")
        print("4. Edit exercise")
        print("5. View routine")
        print("6. Quit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            start_workout(username)
        elif choice == "2":
            add_exercise(username)
        elif choice == "3":
            remove_exercise(username)
        elif choice == "4":
            edit_exercise(username)
        elif choice == "5":
            view_routine(username)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

def create_routine(username: str):
    print("Let's set up your initial routine.")
    add_exercise(username)