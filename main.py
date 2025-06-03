def login_prompt() -> None:
    
    newuser = input("Hello! Are you a new or returning user?")
    if newuser == "new":
        user_registration()
    else: 
        run_menu()

def user_registration() -> None
    username = input("Enter a username: ")
    password = input("Enter a password: ")

# print("What exercise would you like to do?")
# exercise = input()
    
# print("How many sets would you like to do?")
# sets = input()

# print("How many reps in each set?")
# reps = input()

# print(f"So you'd like to do {sets} sets of {reps} reps for {exercise}?")