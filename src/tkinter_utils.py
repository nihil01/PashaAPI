import os
import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
from tkinter import messagebox

import sqlite3 as sql
from banks_api.kapital_bank_api import KapitalBankAPI
from banks_api.pasha_bank_api import PashaBankAPI
from db.db_utils import resource_path

def get_default_save_dir(destination: str):
    home_directory = Path.home()
    desktop = Path.joinpath(home_directory, 'Desktop', destination)

    if not os.path.exists(desktop):
        os.mkdir(desktop)
    return desktop.resolve()

pasha_client = PashaBankAPI(
    excel_path=get_default_save_dir("Pasha_Bank_Excel"),
)

kapital_client = KapitalBankAPI(
    excel_path=get_default_save_dir("Kapital_Bank_Excel"),
)


def add_to_pasha_tab(root, JWT_TOKEN, API_KEY):
    for widget in root.winfo_children():
        widget.destroy()

    frm = ttk.Frame(root, style="Modern.TFrame")
    frm.pack(fill="both", expand=True, padx=20, pady=20)

    ttk.Label(frm, text="Pasha Bank — Export Data", style="ModernTitle.TLabel").pack(anchor="w", pady=(0,15))

    # Date FROM
    ttk.Label(frm, text="Date FROM (YY-MM-DD)", style="Modern.TLabel").pack(anchor="w")
    entry_date_from = ttk.Entry(frm, style="Modern.TEntry")
    entry_date_from.pack(anchor="w", fill="x", pady=(0,10))

    # Date TO
    ttk.Label(frm, text="Date TO (YY-MM-DD)", style="Modern.TLabel").pack(anchor="w")
    entry_date_to = ttk.Entry(frm, style="Modern.TEntry")
    entry_date_to.pack(anchor="w", fill="x", pady=(0,10))

    # JWT
    ttk.Label(frm, text="JWT Token", style="Modern.TLabel").pack(anchor="w")
    entry_jwt = ttk.Entry(frm, style="Modern.TEntry")
    entry_jwt.pack(anchor="w", fill="x", pady=(0,10))
    if JWT_TOKEN:
        entry_jwt.insert(0, JWT_TOKEN)

    # API Key
    ttk.Label(frm, text="API Token", style="Modern.TLabel").pack(anchor="w")
    entry_api = ttk.Entry(frm, style="Modern.TEntry")
    entry_api.pack(anchor="w", fill="x", pady=(0,10))
    if API_KEY:
        entry_api.insert(0, API_KEY)

    # Path label
    tk.Label(frm, text=f"* Saved to: {get_default_save_dir('Pasha_Bank_Excel')}",
             fg="#7f8c8d", bg="#ffffff",
             font=("Segoe UI", 9)).pack(anchor="w", pady=(5,10))

    # Submit Button
    ttk.Button(
        frm,
        text="Generate Excel",
        style="Modern.TButton",
        command=lambda: send_request_pasha(entry_date_from, entry_date_to, entry_jwt, entry_api)
    ).pack(pady=10)


def add_to_kapital_tab(root, username, password):
    for widget in root.winfo_children():
        widget.destroy()

    frm = ttk.Frame(root, style="Modern.TFrame")
    frm.pack(fill="both", expand=True, padx=20, pady=20)

    ttk.Label(frm, text="Kapital Bank — Export Data", style="ModernTitle.TLabel").pack(anchor="w", pady=(0,15))

    # Username
    ttk.Label(frm, text="Username", style="Modern.TLabel").pack(anchor="w")
    entry_username = ttk.Entry(frm, style="Modern.TEntry")
    entry_username.pack(anchor="w", fill="x", pady=5)
    if username:
        entry_username.insert(0, username)

    # Password
    ttk.Label(frm, text="Password", style="Modern.TLabel").pack(anchor="w")
    entry_password = ttk.Entry(frm, style="Modern.TEntry", show="*")
    entry_password.pack(anchor="w", fill="x", pady=5)
    if password:
        entry_password.insert(0, password)

    # Date FROM
    ttk.Label(frm, text="Date FROM (DD-MM-YY)", style="Modern.TLabel").pack(anchor="w")
    entry_date_from = ttk.Entry(frm, style="Modern.TEntry")
    entry_date_from.pack(anchor="w", fill="x", pady=5)

    # Date TO
    ttk.Label(frm, text="Date TO (DD-MM-YY)", style="Modern.TLabel").pack(anchor="w")
    entry_date_to = ttk.Entry(frm, style="Modern.TEntry")
    entry_date_to.pack(anchor="w", fill="x", pady=5)

    tk.Label(
        frm,
        text=f"* Saved to: {get_default_save_dir('Kapital_Bank_Excel')}",
        fg="#7f8c8d",
        bg="#ffffff",
        font=("Segoe UI", 9)
    ).pack(anchor="w", pady=(5,10))

    ttk.Button(
        frm,
        text="Generate Excel",
        style="Modern.TButton",
        command=lambda: send_request_kapital(entry_username, entry_password, entry_date_from, entry_date_to)
    ).pack(pady=10)




def send_request_kapital(entry_username, entry_password, entry_date_from, entry_date_to):
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    date_from = entry_date_from.get().strip()
    date_to = entry_date_to.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Username and Password cannot be empty!")
        return

    save_data("Kapital_Bank", username, password)


    kapital_client.process_data(date_from, date_to, username, password)
    messagebox.showinfo("Info", "Request has been sent. Check destination folder")

def send_request_pasha(entry_date_from, entry_date_to, entry_jwt_to, entry_api):
    jwt_val = entry_jwt_to.get().strip()
    api_val = entry_api.get().strip()

    if not jwt_val or not api_val:
        messagebox.showerror("Error", "JWT and API Token cannot be empty!")
        return

    save_data("Pasha_Bank", jwt_val, api_val)


    date_from = entry_date_from.get().strip()
    date_to = entry_date_to.get().strip()

    pasha_client.process_data(date_from, date_to, jwt_val, api_val)
    messagebox.showinfo("Info", "Request has been sent. Check destination folder")


def save_data(bank:str, jwt: str, api_key: str):

    db_path = resource_path("db/bank.db")

    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    try:
        with sql.connect(db_path) as connection:
            cursor = connection.cursor()

            match bank:
                case "Pasha_Bank":
                    cursor.execute("UPDATE pasha_credentials SET jwt=?, api_key=?", (jwt, api_key))
                    connection.commit()
                    return
                case "Kapital_Bank":
                    cursor.execute("UPDATE kapital_credentials SET username=?, password=?", (jwt, api_key))
                    connection.commit()
                    return
                case _:
                    print("Invalid bank name")
    except sql.ProgrammingError as e:
        print("Error:", str(e))


def apply_modern_style(root):
    root.configure(bg="#f2f4f7")

    style = ttk.Style()
    style.theme_use("clam")

    # ====== Notebook ======
    style.configure(
        "TNotebook",
        background="#f2f4f7",
        borderwidth=0
    )
    style.configure(
        "TNotebook.Tab",
        padding=[10, 5],
        font=("Segoe UI", 11),
        background="#e6e9ef",
        foreground="#2c3e50"
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", "#ffffff")],
        foreground=[("selected", "#000")],
    )

    # ====== Frames ======
    style.configure(
        "Modern.TFrame",
        background="#ffffff",
        relief="flat"
    )

    # ====== Labels ======
    style.configure(
        "Modern.TLabel",
        background="#ffffff",
        foreground="#2c3e50",
        font=("Segoe UI", 11)
    )

    style.configure(
        "ModernTitle.TLabel",
        background="#ffffff",
        foreground="#1a252f",
        font=("Segoe UI", 13, "bold")
    )

    # ====== Entry ======
    style.configure(
        "Modern.TEntry",
        padding=8,
        relief="flat",
        borderwidth=2,
        foreground="#333",
        fieldbackground="#ffffff",
        font=("Segoe UI", 11)
    )
    style.map(
        "Modern.TEntry",
        bordercolor=[("focus", "#4b7bec")],
        foreground=[("disabled", "#aaa")],
    )

    # ====== Button ======
    style.configure(
        "Modern.TButton",
        font=("Segoe UI", 11, "bold"),
        padding=8,
        background="#4b7bec",
        foreground="white",
        borderwidth=0
    )
    style.map(
        "Modern.TButton",
        background=[("active", "#3867d6")],
    )
