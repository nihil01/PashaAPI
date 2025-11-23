import datetime
import logging
import os
import sys
import tkinter as tk
from tkinter import ttk

import db.db_utils as db
from banks_api.api_logger import setup_api_logger
from tkinter_utils import add_to_pasha_tab, add_to_kapital_tab, apply_modern_style

setup_api_logger("MULTI_BANK_LOGGER")

db.setup_connection_bank()
logging.info("== DATABASE CONNECTIVITY HAS BEEN ESTABLISHED ==")

logging.info("== PASHA BANK & KAPITAL BANK API CLIENTS HAVE BEEN INITIALIZED ==")

logging.info(f"Program started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def resource_path(file):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, file)
    return file


def on_tab_changed(event):
    notebook_ = event.widget
    current_tab = notebook_.select()
    idx = notebook_.index(current_tab)

    # 0 — Pasha, 1 — Kapital и т.д.
    if idx == 0:
        for child in pasha_tab.winfo_children():
            child.destroy()
        add_to_pasha_tab(pasha_tab, db.JWT_TOKEN_PASHA, db.API_KEY_PASHA)

    elif idx == 1:
        for child in kapital_tab.winfo_children():
            child.destroy()
        add_to_kapital_tab(kapital_tab, db.KAPITAL_USER, db.KAPITAL_PASS)  # своя функция

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

notebook.bind("<<NotebookTabChanged>>", on_tab_changed)


#первая инициализация
add_to_pasha_tab(pasha_tab, db.JWT_TOKEN_PASHA, db.API_KEY_PASHA)

icon = tk.PhotoImage(file=resource_path("pasha.png"))
root.iconphoto(False, icon)


root.mainloop()