import datetime
import logging
import os
import sys
import tkinter as tk
from tkinter import ttk

import db.db_utils as db
from banks_api.api_logger import setup_api_logger
from styles import apply_modern_style
from tkinter_utils import add_to_pasha_tab, add_to_kapital_tab, add_to_abb_tab

setup_api_logger("MULTI_BANK_LOGGER")

db.setup_connection_bank()
logging.info("[*] DATABASE CONNECTIVITY HAS BEEN ESTABLISHED")

logging.info("==== PASHA BANK & KAPITAL BANK & ABB BANK API CLIENTS HAVE BEEN INITIALIZED ====")

logging.info(f"[START] Program started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [START]")

def resource_path(file):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, file)
    return file

def clear_children(container):
    for child in container.winfo_children():
        child.destroy()

def on_tab_changed(event):
    notebook_ = event.widget
    current_tab = notebook_.select()
    idx = notebook_.index(current_tab)

    # 0 — Pasha, 1 — Kapital и т.д.
    if idx == 0:
        clear_children(pasha_tab)
        add_to_pasha_tab(pasha_tab, db.JWT_TOKEN_PASHA, db.API_KEY_PASHA)

    elif idx == 1:
        clear_children(kapital_tab)
        add_to_kapital_tab(kapital_tab, db.KAPITAL_USER, db.KAPITAL_PASS)
    elif idx == 2:
        clear_children(abb_tab)
        add_to_abb_tab(abb_tab, db.ABB_USER, db.ABB_PASS)


root = tk.Tk()
apply_modern_style(root)
root.title("Multibank API Client")
root.geometry("800x600")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

pasha_tab = ttk.Frame(notebook)
notebook.add(pasha_tab, text="Pasha Bank")

kapital_tab = ttk.Frame(notebook)
notebook.add(kapital_tab, text="Kapital Bank")

abb_tab = ttk.Frame(notebook)
notebook.add(abb_tab, text="ABB Bank")

notebook.bind("<<NotebookTabChanged>>", on_tab_changed)


#первая инициализация
add_to_pasha_tab(pasha_tab, db.JWT_TOKEN_PASHA, db.API_KEY_PASHA)

icon = tk.PhotoImage(file=resource_path("static/bank.png"))
root.iconphoto(False, icon)

if __name__ == "__main__":
    root.mainloop()