from tkinter import ttk


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