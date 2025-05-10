import database
from datetime import datetime

def authenticate_user(card_number, pin):
    user = database.get_user(card_number)
    if user and user[1] == pin:
        return True
    return False

def check_balance(card_number):
    user = database.get_user(card_number)
    return user[2]  # Return balance

def deposit(card_number, amount):
    user = database.get_user(card_number)
    if amount > 0:
        new_balance = user[2] + amount
        database.update_balance(card_number, new_balance)
        record_transaction(card_number, "Deposit", amount)
        return new_balance
    return None

def withdraw(card_number, amount):
    user = database.get_user(card_number)
    if amount <= user[2] and amount > 0:
        new_balance = user[2] - amount
        database.update_balance(card_number, new_balance)
        record_transaction(card_number, "Withdrawal", amount)
        return new_balance
    return None

def transfer(card_number_from, card_number_to, amount):
    user_from = database.get_user(card_number_from)
    user_to = database.get_user(card_number_to)
    if amount <= user_from[2] and amount > 0:
        new_balance_from = user_from[2] - amount
        new_balance_to = user_to[2] + amount
        database.update_balance(card_number_from, new_balance_from)
        database.update_balance(card_number_to, new_balance_to)
        record_transaction(card_number_from, "Transfer", amount)
        record_transaction(card_number_to, "Transfer", amount)
        return new_balance_from, new_balance_to
    return None

def record_transaction(card_number, transaction_type, amount):
    conn = database.connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO transactions (card_number, transaction_type, amount, date) VALUES (?, ?, ?, ?)",
              (card_number, transaction_type, amount, str(datetime.now())))
    conn.commit()
    conn.close()
def main():
    # Initialize database
    database.create_tables()

    print("Welcome to the ATM!")
    
    # User login process
    card_number = input("Enter your card number: ")
    pin = input("Enter your PIN: ")
    
    if authenticate_user(card_number, pin):
        print("Login successful!")
        while True:
            print("\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Transfer\n5. Exit")
            choice = input("Select an option: ")

            if choice == "1":
                print(f"Your current balance is: ${check_balance(card_number)}")
            elif choice == "2":
                amount = float(input("Enter amount to deposit: "))
                print(f"Your new balance is: ${deposit(card_number, amount)}")
            elif choice == "3":
                amount = float(input("Enter amount to withdraw: "))
                print(f"Your new balance is: ${withdraw(card_number, amount)}")
            elif choice == "4":
                card_number_to = input("Enter the recipient card number: ")
                amount = float(input("Enter amount to transfer: "))
                new_balance_from, new_balance_to = transfer(card_number, card_number_to, amount)
                if new_balance_from:
                    print(f"Transfer successful! Your new balance is: ${new_balance_from}")
                    print(f"Recipient's new balance is: ${new_balance_to}")
                else:
                    print("Transfer failed. Insufficient balance.")
            elif choice == "5":
                print("Thank you for using the ATM!")
                break
            else:
                print("Invalid option. Please try again.")
    else:
        print("Invalid card number or PIN!")

if __name__ == "__main__":
    main()
