import tkinter as tk
from tkinter import messagebox
import atm  # Import your ATM logic

def login():
    card_number = entry_card.get()
    pin = entry_pin.get()

    if atm.authenticate_user(card_number, pin):
        messagebox.showinfo("Login", "Login successful!")
        # Proceed to the next menu after successful login
    else:
        messagebox.showerror("Login", "Invalid card number or PIN")

# Set up the main window
window = tk.Tk()
window.title("ATM Login")

# Create labels and entry fields
label_card = tk.Label(window, text="Card Number:")
label_card.pack()
entry_card = tk.Entry(window)
entry_card.pack()

label_pin = tk.Label(window, text="PIN:")
label_pin.pack()
entry_pin = tk.Entry(window, show="*")
entry_pin.pack()

# Create login button
login_button = tk.Button(window, text="Login", command=login)
login_button.pack()

# Run the Tkinter event loop
window.mainloop()
