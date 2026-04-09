import json
import hashlib
from pathlib import Path


FILE_NAME = Path("users.json")


def load_users():

    # create file if it doesn't exist
    if not FILE_NAME.exists():
        with open(FILE_NAME, "w") as file:
            json.dump({"users": []}, file, indent=4)

    # load json data
    with open(FILE_NAME, "r") as file:
        return json.load(file)


def save_users(data):

    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def hash_password(password):

    return hashlib.sha256(password.encode()).hexdigest()


def username_exists(username):

    data = load_users()

    for user in data["users"]:
        if user["username"] == username:
            return True

    return False


def create_account(username, password):

    if username.strip() == "" or password.strip() == "":
        return False, "username or password cannot be empty"

    if username_exists(username):
        return False, "username already exists"

    data = load_users()

    new_user = {
        "username": username,
        "password": hash_password(password)
    }

    data["users"].append(new_user)

    save_users(data)

    return True, "account created"


def login(username, password):

    data = load_users()

    hashed_input = hash_password(password)

    for user in data["users"]:

        if user["username"] == username and user["password"] == hashed_input:
            return True, "login successful"

    return False, "invalid login"