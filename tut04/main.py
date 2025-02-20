import hashlib
import os
import json

db_file = "user_db.json"

def load_users():
    if os.path.exists(db_file):
        with open(db_file, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(db_file, "w") as f:
        json.dump(users, f)

def hash_password(password):
    salt = os.urandom(16).hex()  # Generate a random 16-byte salt
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${hashed}"

def register(username, password):
    users = load_users()
    if username in users:
        print("Username already exists!")
        return False
    users[username] = hash_password(password)
    save_users(users)
    print("User registered successfully!")
    return True

def login(username, password):
    users = load_users()
    if username not in users:
        print("Invalid username or password!")
        return False
    
    stored_hash = users[username]
    salt, correct_hash = stored_hash.split("$")
    attempt_hash = hashlib.sha256((salt + password).encode()).hexdigest()
    
    if attempt_hash == correct_hash:
        print("Login successful!")
        return True
    else:
        print("Invalid username or password!")
        return False

if __name__ == "__main__":
    while True:
        choice = input("Choose an option (register/login/exit): ").strip().lower()
        if choice == "register":
            user = input("Enter username: ")
            pwd = input("Enter password: ")
            register(user, pwd)
        elif choice == "login":
            user = input("Enter username: ")
            pwd = input("Enter password: ")
            login(user, pwd)
        elif choice == "exit":
            break
        else:
            print("Invalid option! Try again.")
