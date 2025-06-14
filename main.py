from storage import load_userdata
from auth import login_prompt

if __name__ == "__main__":
    load_userdata()
    login_prompt()