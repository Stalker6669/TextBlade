import os
import customtkinter as ctk
from tkinter import TclError


def set_app_icon(app, icon_path="icon.ico"):
    if os.path.exists("icon.ico"):
        try:
            app.iconbitmap("icon.ico")
        except Exception as e:
            print(f"Ошибка при установке иконки: {e}")
