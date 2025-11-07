import os
import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sql

from pasha_bank_api import PashaBankAPIClient

JWT_TOKEN = None
API_KEY = None


def get_default_save_dir():
    home_directory = Path.home()
    desktop = Path.joinpath(home_directory, 'Desktop', "Pasha_Bank_Excel")

    if not os.path.exists(desktop):
        os.mkdir(desktop)
    return desktop.resolve()

def resource_path(file):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, file)
    return file

def setup_connection():
    global JWT_TOKEN, API_KEY

    try:
        with sql.connect("Pasha_Bank_Excel.db") as connection:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS credentials (
                    jwt TEXT,
                    api_key TEXT
                )
            """)

            cursor.execute("SELECT * FROM credentials")
            data = cursor.fetchall()

            if len(data) == 0:
                cursor.execute("INSERT INTO credentials (jwt, api_key) VALUES (?, ?)", ("REPLACE", "REPLACE"))
                print("Inserted default test credentials")
                JWT_TOKEN = "REPLACE"
                API_KEY = "REPLACE"
            else:
                JWT_TOKEN = data[0][0]
                API_KEY = data[0][1]

    except sql.ProgrammingError as e:
        print("Error:", str(e))


def save_data(jwt: str, api_key: str):
    try:
        with sql.connect("Pasha_Bank_Excel.db") as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE credentials SET jwt=?, api_key=?", (jwt, api_key))
            print("DATA SAVED:", cursor.rowcount)

    except sql.ProgrammingError as e:
        print("Error:", str(e))


setup_connection()

root = tk.Tk()
root.title("Pasha Bank API Client")
root.geometry("450x450")

label_date_from = tk.Label(root, text="Date FROM")
label_date_from.pack(anchor="nw", padx=5, pady=5)

entry_date_from = ttk.Entry(root)
entry_date_from.pack(anchor="nw", padx=8, pady=8)

label_date_to = tk.Label(root, text="Date TO")
label_date_to.pack(anchor="nw", padx=5, pady=5)

entry_date_to = ttk.Entry(root)
entry_date_to.pack(anchor="nw", padx=8, pady=8)

label_jwt = tk.Label(root, text="JWT Token")
label_jwt.pack(anchor="nw", padx=5, pady=5)

entry_jwt_to = ttk.Entry(root)
entry_jwt_to.pack(anchor="nw", padx=8, pady=8)

if JWT_TOKEN:
    entry_jwt_to.insert(0, JWT_TOKEN)

label_api = tk.Label(root, text="API Token")
label_api.pack(anchor="nw", padx=5, pady=5)

entry_api = ttk.Entry(root)
entry_api.pack(anchor="nw", padx=8, pady=8)

if API_KEY:
    entry_api.insert(0, API_KEY)

lb = tk.Label(root, text=f"* Default path for saved documents {get_default_save_dir()}", font=("Arial", 8))
lb.pack(anchor="n", padx=5, pady=5)

icon = tk.PhotoImage(file=resource_path("pasha.png"))
root.iconphoto(False, icon)


def send_request():
    jwt_val = entry_jwt_to.get().strip()
    api_val = entry_api.get().strip()

    if not jwt_val or not api_val:
        messagebox.showerror("Error", "JWT and API Token cannot be empty!")
        return

    save_data(jwt_val, api_val)

    client = PashaBankAPIClient(
        excel_path=get_default_save_dir(),
        jwt=jwt_val,
        api=api_val,
    )

    date_from = entry_date_from.get().strip()
    date_to = entry_date_to.get().strip()

    client.process_data(date_from, date_to)

    messagebox.showinfo("Info", "Request has been sent. Check destination folder")


btn = ttk.Button(root, text="GET DATA", command=send_request)
btn.pack(anchor="nw", padx=6, pady=6)

root.mainloop()
