import tkinter as tk
import tkinter.ttk as ttk

from async_requests import send_request_pasha, send_request_kapital, send_request_abb, get_default_save_dir


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

def add_to_abb_tab(root, username, password):
    for widget in root.winfo_children():
        widget.destroy()

    frm = ttk.Frame(root, style="Modern.TFrame")
    frm.pack(fill="both", expand=True, padx=20, pady=20)

    ttk.Label(frm, text="ABB Bank — Export Data", style="ModernTitle.TLabel").pack(anchor="w", pady=(0,15))

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
    ttk.Label(frm, text="Date FROM (YYYY-MM-DD)", style="Modern.TLabel").pack(anchor="w")
    entry_date_from = ttk.Entry(frm, style="Modern.TEntry")
    entry_date_from.pack(anchor="w", fill="x", pady=5)

    # Date TO
    ttk.Label(frm, text="Date TO (YYYY-MM-DD)", style="Modern.TLabel").pack(anchor="w")
    entry_date_to = ttk.Entry(frm, style="Modern.TEntry")
    entry_date_to.pack(anchor="w", fill="x", pady=5)

    tk.Label(
        frm,
        text=f"* Saved to: {get_default_save_dir('ABB_Bank_Excel')}",
        fg="#7f8c8d",
        bg="#ffffff",
        font=("Segoe UI", 9)
    ).pack(anchor="w", pady=(5,10))

    ttk.Button(
        frm,
        text="Generate Excel",
        style="Modern.TButton",
        command=lambda: send_request_abb(entry_username, entry_password, entry_date_from, entry_date_to)
    ).pack(pady=10)

