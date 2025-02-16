import re

def is_valid_password(password, criteria):
    if len(password) < 8:
        return False, "Less than 8 characters. Skipping validation."
    
    if 1 in criteria and not re.search(r'[A-Z]', password):
        return False, "Missing uppercase letter."
    if 2 in criteria and not re.search(r'[a-z]', password):
        return False, "Missing lowercase letter."
    if 3 in criteria and not re.search(r'\d', password):
        return False, "Missing number."
    if 4 in criteria:
        special_chars = set("!@#")
        if not any(c in special_chars for c in password) or any(c not in special_chars and not c.isalnum() for c in password):
            return False, "Invalid special character."
    
    return True, "Valid password."

def get_selected_criteria():
    print("Select the criteria for password validation (comma-separated numbers):")
    print("1. Uppercase letters (A-Z)")
    print("2. Lowercase letters (a-z)")
    print("3. Numbers (0-9)")
    print("4. Special characters (!, @, #)")
    
    selected = input("Enter your choices (e.g., 1,3,4): ")
    return set(map(int, selected.split(',')))

def validate_passwords():
    criteria = get_selected_criteria()
    password_list = [
        "abc12345",
        "abc",
        "123456789",
        "abcdefg$",
        "abcdefgABHD!@313",
        "abcdefgABHD$$!@313"
    ]
    
    for password in password_list:
        valid, message = is_valid_password(password, criteria)
        print(f"Password: {password}\nResult: {message}")

def validate_passwords_from_file():
    criteria = get_selected_criteria()
    file_path = "/Users/vansh/Documents/CS457_Big-_Data/lab3/input.txt"
    
    valid_count = 0
    invalid_count = 0
    
    with open(file_path, "r") as file:
        passwords = file.readlines()
        
        for password in passwords:
            password = password.strip()
            valid, _ = is_valid_password(password, criteria)
            if valid:
                valid_count += 1
            else:
                invalid_count += 1
    
    print(f"Total Valid Passwords: {valid_count}")
    print(f"Total Invalid Passwords: {invalid_count}")

# User Interaction
print("Choose an option:")
print("1. Validate Password List")
print("2. Validate from File")
choice = input("Enter choice (1/2): ").strip()

if choice == "1":
    validate_passwords()
elif choice == "2":
    validate_passwords_from_file()
else:
    print("Invalid choice. Exiting.")
