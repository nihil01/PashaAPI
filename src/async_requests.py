import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tkinter import messagebox

from banks_api.abb_bank_api import AbbBankAPI
from banks_api.kapital_bank_api import KapitalBankAPI
from banks_api.pasha_bank_api import PashaBankAPI
from db.db_utils import save_data
from play_sound import play


# -------------------- Util function --------------------

def get_default_save_dir(destination: str):
    home_directory = Path.home()
    desktop = Path.joinpath(home_directory, 'Desktop', destination)

    if not os.path.exists(desktop):
        os.mkdir(desktop)
    return desktop.resolve()

# -------------------- Clients --------------------

pasha_client = PashaBankAPI(
    excel_path=get_default_save_dir("Pasha_Bank_Excel"),
)

kapital_client = KapitalBankAPI(
    excel_path=get_default_save_dir("Kapital_Bank_Excel"),
)

abb_client = AbbBankAPI(
    excel_path=get_default_save_dir("Abb_Bank_Excel"),
)


# -------------------- Executor & State --------------------

executor = ThreadPoolExecutor(max_workers=1)
background_busy = False


# -------------------- Background runner --------------------

def run_background(func, *args):
    global background_busy

    if background_busy:
        messagebox.showwarning("Busy", "Another request is already running")
        return None

    messagebox.showinfo("Info", "Request sent to background")

    background_busy = True
    future = executor.submit(func, *args)
    future.add_done_callback(_on_background_done)
    return future


def _on_background_done(future):
    global background_busy
    background_busy = False

    try:
        future.result()
        play()
        messagebox.showinfo("Info", "Request completed successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# -------------------- ABB --------------------

def send_request_abb(entry_username, entry_password, entry_date_from, entry_date_to):
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    date_from = entry_date_from.get().strip()
    date_to = entry_date_to.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Username and Password cannot be empty!")
        return

    save_data("ABB_Bank", username, password)

    run_background(
        abb_client.process_data, date_from, date_to, username, password
    )


# -------------------- Kapital --------------------

def send_request_kapital(entry_username, entry_password, entry_date_from, entry_date_to):
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    date_from = entry_date_from.get().strip()
    date_to = entry_date_to.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Username and Password cannot be empty!")
        return

    save_data("Kapital_Bank", username, password)

    run_background(
         kapital_client.process_data, date_from, date_to, username, password
    )


# -------------------- Pasha --------------------

def send_request_pasha(entry_date_from, entry_date_to, entry_jwt_to, entry_api):
    jwt_val = entry_jwt_to.get().strip()
    api_val = entry_api.get().strip()

    if not jwt_val or not api_val:
        messagebox.showerror("Error", "JWT and API Token cannot be empty!")
        return

    save_data("Pasha_Bank", jwt_val, api_val)

    date_from = entry_date_from.get().strip()
    date_to = entry_date_to.get().strip()

    run_background(
        pasha_client.process_data, date_from, date_to, jwt_val, api_val
    )
