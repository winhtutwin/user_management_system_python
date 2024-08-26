import ast
import os

def load_user_data():
    """Load user data from a text file if it exists."""
    user_data = {}
    if os.path.exists("userlist.txt"):
        with open("userlist.txt", "r") as file:
            data = file.readlines()
            for line in data:
                try:
                    user_entry = ast.literal_eval(line.strip())
                    user_id = str(user_entry.get('id'))
                    if user_id:
                        user_data[user_id] = user_entry
                except (SyntaxError, ValueError) as e:
                    print(f"Skipping invalid line: {line.strip()} (Error: {e})")
    return user_data

def save_user_data(user_data):
    """Save user data to a text file, ensuring no duplicates."""
    user_info_lines = [f"{info}" for info in user_data.values()]
    user_info_lines = list(set(user_info_lines))
    
    with open("userlist.txt", "w") as file:
        for line in user_info_lines:
            file.write(f"{line}\n")

def get_next_user_id(user_data):
    """Determine the next user ID."""
    if user_data:
        max_id = max(int(user_id) for user_id in user_data)
    else:
        max_id = 0
    return max_id + 1

def is_name_taken(user_data, name):
    """Check if name is already taken."""
    for user in user_data.values():
        if user['name'] == name:
            return True
    return False

def register_user():
    """Handle user registration."""
    user_data = load_user_data()
    name = input("Enter name: ")
    passcode = input("Enter passcode: ")
    confirm_passcode = input("Confirm passcode: ")
    amount = input("Enter amount: ")

    if passcode != confirm_passcode:
        print("Error: Passcodes do not match.")
        return

    try:
        amount = float(amount)
    except ValueError:
        print("Error: Amount must be a number.")
        return

    if is_name_taken(user_data, name):
        print("Error: Name already taken. Please choose a different name.")
        return

    user_id = get_next_user_id(user_data)
    user_data[user_id] = {
        'id': user_id,
        'name': name,
        'passcode': passcode,
        'amount': amount
    }

    save_user_data(user_data)
    print(f"User registered successfully with ID: {user_id}")

def login_user():
    """Handle user login using username."""
    user_data = load_user_data()
    name = input("Enter your username: ")
    passcode = input("Enter your passcode: ")

    user_info = None
    for user in user_data.values():
        if user['name'] == name:
            user_info = user
            break

    if user_info:
        if user_info['passcode'] == passcode:
            print(f"Login successful! Welcome, {user_info['name']}.")
            user_menu(user_info, user_data)
        else:
            print("Error: Incorrect passcode.")
    else:
        print("Error: Username does not exist.")

def user_menu(current_user, user_data):
    """Display the user menu and handle user choices."""
    while True:
        print("\nUser Menu")
        print("1. Transfer Amount")
        print("2. Update Data")
        print("3. Withdraw")
        print("0. Logout")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            transfer_amount(current_user, user_data)
        elif choice == '2':
            update_data(current_user, user_data)
        elif choice == '3':
            withdraw_amount(current_user, user_data)
        elif choice == '0':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 0.")

def transfer_amount(current_user, user_data):
    """Handle the amount transfer between users using recipient username."""
    recipient_name = input("Enter recipient username: ")
    amount = input("Enter amount to transfer: ")

    try:
        amount = float(amount)
    except ValueError:
        print("Error: Amount must be a number.")
        return

    if amount <= 0:
        print("Error: Amount must be greater than zero.")
        return

    if current_user['amount'] < amount:
        print("Error: Insufficient funds.")
        return

    recipient_info = None
    for user in user_data.values():
        if user['name'] == recipient_name:
            recipient_info = user
            break

    if recipient_info:
        if recipient_info['id'] == current_user['id']:
            print("Error: Cannot transfer to yourself.")
            return

        current_user['amount'] -= amount
        recipient_info['amount'] += amount

        user_data[current_user['id']] = current_user
        user_data[recipient_info['id']] = recipient_info

        save_user_data(user_data)
        print(f"Transfer successful! Your new balance: {current_user['amount']}")
    else:
        print("Error: Recipient username does not exist.")

def update_data(current_user, user_data):
    """Handle the update of user data."""
    print("Update your information:")
    new_name = input(f"Enter new name (current: {current_user['name']}): ")
    new_passcode = input("Enter new passcode: ")
    confirm_new_passcode = input("Confirm new passcode: ")

    if new_passcode != confirm_new_passcode:
        print("Error: Passcodes do not match.")
        return

    current_user['name'] = new_name
    current_user['passcode'] = new_passcode

    user_data[current_user['id']] = current_user

    save_user_data(user_data)
    print("User information updated successfully!")

def withdraw_amount(current_user, user_data):
    """Handle withdrawal of funds."""
    amount = input("Enter amount to withdraw: ")

    try:
        amount = float(amount)
    except ValueError:
        print("Error: Amount must be a number.")
        return

    if amount <= 0:
        print("Error: Amount must be greater than zero.")
        return

    if current_user['amount'] < amount:
        print("Error: Insufficient funds.")
        return

    current_user['amount'] -= amount

    user_data[current_user['id']] = current_user

    save_user_data(user_data)
    print(f"Withdrawal successful! New balance: {current_user['amount']}")

def main_menu():
    """Display the main menu and handle user choices."""
    while True:
        print("Welcome to the User Management System")
        print("1. Login")
        print("2. Register")
        print("0. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            login_user()
        elif choice == '2':
            register_user()
        elif choice == '0':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 0.")

if __name__ == "__main__":
    main_menu()
