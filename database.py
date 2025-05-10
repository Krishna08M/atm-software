import sqlite3

DB_NAME = 'atm_db.db'

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            card_number TEXT PRIMARY KEY,
            pin TEXT NOT NULL,
            balance REAL DEFAULT 0.0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_number TEXT,
            transaction_type TEXT,
            amount REAL,
            date TEXT
        )
    ''')

    conn.commit()
    conn.close()

def create_user(card_number, pin, balance=0.0):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (card_number, pin, balance)
            VALUES (?, ?, ?)
        ''', (card_number, pin, balance))
        conn.commit()
        print(f"User {card_number} created successfully.")
    except sqlite3.IntegrityError:
        print("User already exists.")
    finally:
        conn.close()



def connect_db():
    return sqlite3.connect("atm_db.db")

def create_tables():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            card_number TEXT PRIMARY KEY,
            pin TEXT,
            balance REAL
        );
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_number TEXT,
            transaction_type TEXT,
            amount REAL,
            date TEXT
        );
    ''')
    conn.commit()
    conn.close()

def create_user(card_number, pin, balance=0.0):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO users (card_number, pin, balance) VALUES (?, ?, ?)", (card_number, pin, balance))
    conn.commit()
    conn.close()

def get_user(card_number):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE card_number = ?", (card_number,))
    user = c.fetchone()
    conn.close()
    return user

def update_balance(card_number, new_balance):
    conn = connect_db()
    c = conn.cursor()
    c.execute("UPDATE users SET balance = ? WHERE card_number = ?", (new_balance, card_number))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    create_user("1234567890", "1234", 1000.0)
