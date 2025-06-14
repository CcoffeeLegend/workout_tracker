from routine import load_userdata, save_userdata, add_exercise, remove_exercise, edit_exercise, view_routine, userdata
from workout import start_workout


def user_login():
    username = input("Enter username: ").strip().lower()
    password = input("Enter password: ").strip()

    if username in userdata and userdata[username]["password"] == password:
        print("Login successful!")
        menu(username)
    else: 
        print("Invalid credentials. Try again.")
        login_prompt()



def login_prompt() -> None:
    user_type = input("Hello! Are you a new or returning user? (n/r): ").strip().lower()
    if user_type in ("n", "new"):
        user_registration()
    elif user_type in ("r", "returning"):
        user_login()
    else:
        print("Invalid input, please enter 'n' for new or 'r' for returning.")
        login_prompt()



def user_registration() -> None:
    username = input("Enter a username: ").strip().lower()
    password = input("Enter a password: ").strip()

    userdata[username] = {
        "password": password,
        "routine": []
    }

    save_userdata()
    create_routine(username)


    save_userdata()
    create_routine(username)


def create_routine(username: str) -> None:
    add_exercise(username)
    menu(username)


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
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    load_userdata()
    login_prompt()
