import os
import shutil
from PIL import Image
import customtkinter as ctk


def set_custom_file_icon(file_path, icon_path="icon2.png"):
    if os.path.exists(icon_path):
        try:
            img = Image.open(icon_path)
            img.thumbnail((32, 32))
            img.save(f"{file_path}.ico", format="ICO")
        except Exception as e:
            print(f"Ошибка при установке иконки для файла {file_path}: {e}")
    else:
        print(f"Файл иконки '{icon_path}' не найден.")


def save_custom_file(content, filename="new_file.txtb"):
    if not filename.endswith(".txtb"):
        filename += ".txtb"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

    set_custom_file_icon(filename)  # Иконка для нового файла
    print(f"Файл '{filename}' успешно сохранен.")
