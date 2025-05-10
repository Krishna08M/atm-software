import sqlite3
from datetime import datetime

DB_NAME = 'atm_db.db'

def record_transaction(card_number, transaction_type, amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (card_number, transaction_type, amount, date)
        VALUES (?, ?, ?, ?)
    ''', (card_number, transaction_type, amount, datetime.now()))
    conn.commit()
    conn.close()

def get_balance(card_number):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT balance FROM users WHERE card_number = ?', (card_number,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def update_balance(card_number, new_balance):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET balance = ? WHERE card_number = ?', (new_balance, card_number))
    conn.commit()
    conn.close()

def deposit(card_number, amount):
    balance = get_balance(card_number)
    if balance is not None and amount > 0:
        new_balance = balance + amount
        update_balance(card_number, new_balance)
        record_transaction(card_number, 'Deposit', amount)
        return new_balance
    else:
        return None

def withdraw(card_number, amount):
    balance = get_balance(card_number)
    if balance is not None and 0 < amount <= balance:
        new_balance = balance - amount
        update_balance(card_number, new_balance)
        record_transaction(card_number, 'Withdraw', amount)
        return new_balance
    else:
        return None

def transfer(from_card, to_card, amount):
    from_balance = get_balance(from_card)
    to_balance = get_balance(to_card)

    if from_balance is not None and to_balance is not None and 0 < amount <= from_balance:
        update_balance(from_card, from_balance - amount)
        update_balance(to_card, to_balance + amount)
        record_transaction(from_card, f'Transfer to {to_card}', amount)
        record_transaction(to_card, f'Transfer from {from_card}', amount)
        return True
    else:
        return False
