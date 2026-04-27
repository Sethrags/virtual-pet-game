#filename: auth_manager.py
#author: Seth
#description: This file manages user authentication for the Tamagotchi game. 
# functions to load and save user data, hash passwords, check for existing usernames, 
# create new accounts, and validate login credentials User data is stored in a JSON 
# file (users.json) with the following structure:
# {"users": [{ "username": "user1","password": "hashed_password1" }, ...]}   
# Passwords are hashed using SHA-256 for security.

  
import json
import hashlib
from pathlib import Path

# Define the path to the users.json file
FILE_NAME = Path("users.json")

#load_users
# This function loads user data from the users.json file. 
# If the file does not exist, it creates a new file with an empty users list. 
# It returns the loaded data as a dictionary.
def load_users():

    # create file if it doesn't exist
    if not FILE_NAME.exists():
        with open(FILE_NAME, "w") as file:
            json.dump({"users": []}, file, indent=4)

    # load json data
    with open(FILE_NAME, "r") as file:
        return json.load(file)

#save_users
# This function saves user data to the users.json file.
# It takes a dictionary (data) as input and writes it to the file in JSON format with indentation for readability.
def save_users(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)

# hash_password
# This function takes a plaintext password as input and returns its SHA-256 hash.
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# username_exists
# This function checks if a given username already exists in the users.json file.
# It returns True if the username exists, and False otherwise.
def username_exists(username):

    data = load_users() # Load user data from the JSON file

    # Iterate through the list of users to check if the username exists
    # Return True if the username is found in the users list
    for user in data["users"]:
        if user["username"] == username:
            return True 

    return False # Return False if the username is not found in the users list

# create_account
# This function creates a new user account with the given username and password.
# It checks if the username or password is empty, and if the username already exists.
# If the account is successfully created, it returns (True, "account created").
def create_account(username, password):

    # Check if username or password is empty, return False with an error message if either is empty
    if username.strip() == "" or password.strip() == "":
        return False, "username or password cannot be empty"

    # Check if the username already exists, return False with an error message if it does
    if username_exists(username):
        return False, "username already exists"

    data = load_users() # Load existing user data from the JSON file

    # Create a new user dictionary with the provided username and the hashed password
    new_user = {
        "username": username,
        "password": hash_password(password)
    }

    # Append the new user to the users list in the loaded data
    data["users"].append(new_user)

    save_users(data) # Save the updated user data back to the JSON file

    return True, "account created"

# login
# This function validates user login credentials. It checks if the provided username 
# and password match any existing user in the users.json file. It returns (True, "login successful") 
# if the credentials are valid, and (False, "invalid login") otherwise.
def login(username, password):

    data = load_users() # Load user data from the JSON file
    hashed_input = hash_password(password) # Hash the input password to compare with stored hashed passwords

    # Iterate through the list of users to find a matching username and password
    # If a match is found, return True with a success message
    for user in data["users"]:
        if user["username"] == username and user["password"] == hashed_input:
            return True, "login successful"

    return False, "invalid login" 