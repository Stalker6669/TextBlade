import json
import os

CONFIG_FILE = "config.json"

def load_config():
    """Загружает настройки из файла конфигурации."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        # Возвращаем настройки по умолчанию, если конфигурация не найдена
        return {
            "theme": "System",  # Тема по умолчанию
            "font": "Helvetica"  # Шрифт по умолчанию
        }

def save_config(config_data):
    """Сохраняет настройки в файл конфигурации."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(config_data, file, ensure_ascii=False, indent=4)
