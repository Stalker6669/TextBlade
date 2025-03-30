from tkinter import Menu, filedialog, END, messagebox
from config import load_config, save_config
from icon_loader import set_app_icon
from file_associations import save_custom_file
from docx import Document
import tkinter as tk
import tkinter.font as tkFont
import customtkinter as ctk

class TextEditor(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.default_zoom_factor = 1.0  # Исходный масштаб
        self.zoom_factor = self.default_zoom_factor  # Начальный масштаб

        # Установка иконки
        set_app_icon(self)

        # Загрузка настроек
        self.config_data = load_config()

        # Установка темы
        ctk.set_appearance_mode(self.config_data['theme'])

        # Размеры окна
        window_width = 800
        window_height = 450

        # Центрирование окна
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.title("TextBlade")

        # Меню
        self.create_menu()

        # Текстовая область
        self.text_area = ctk.CTkTextbox(self, font=(self.config_data['font'], 14), wrap="word")
        self.text_area.pack(expand=True, fill="both", padx=10, pady=10)

        # Состояние файла
        self.current_file = None

        # Перехват закрытия окна
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Сохранение исходного состояния текста
        self.saved_content = self.text_area.get("1.0", END).strip()

    def create_menu(self):
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        # Шрифт для элементов меню
        menu_font = tkFont.Font(family="Helvetica", size=11)

        # Файл
        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новый", command=self.new_file, font=menu_font)
        file_menu.add_command(label="Открыть", command=self.open_file_dialog, font=menu_font)
        file_menu.add_command(label="Сохранить", command=self.save_file, font=menu_font)
        file_menu.add_command(label="Сохранить как", command=self.save_as_file, font=menu_font)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.on_close, font=menu_font)

        # Вид
        view_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Вид", menu=view_menu)
        view_menu.add_command(label="Тёмная тема", command=lambda: self.set_theme("dark"), font=menu_font)
        view_menu.add_command(label="Светлая тема", command=lambda: self.set_theme("light"), font=menu_font)
        view_menu.add_command(label="Системная тема", command=lambda: self.set_theme("System"), font=menu_font)

        # Добавление настроек масштаба
        view_menu.add_separator()
        view_menu.add_command(label="Масштаб +", command=self.zoom_in)
        view_menu.add_command(label="Масштаб -", command=self.zoom_out)
        view_menu.add_command(label="Сбросить масштаб", command=self.reset_zoom)

        # Шрифт
        font_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Шрифт", menu=font_menu)
        font_menu.add_command(label="Выбрать шрифт", command=self.open_font_selection, font=menu_font)

    def open_font_selection(self):
        """Открывает окно выбора шрифта."""
        font_window = ctk.CTkToplevel(self)
        font_window.title("Выбор шрифта")

        # Привязка окна к основному
        font_window.transient(self)  # Устанавливает окно дочерним
        font_window.grab_set()  # Блокирует взаимодействие с основным окном, пока это открыто

        # Установка иконки
        try:
            font_window.iconbitmap("icon.ico")
        except Exception as e:
            print(f"Ошибка с иконкой: {e}")

        # Центрирование окна выбора шрифта
        window_width = 350
        window_height = 500
        x = self.winfo_x() + (self.winfo_width() // 2) - (window_width // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (window_height // 2)
        font_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Настройка темы окна выбора шрифта
        font_window.configure(fg_color=ctk.ThemeManager.theme["CTkToplevel"]["fg_color"])  # Соответствие основной теме

        # Список доступных шрифтов
        fonts = list(tkFont.families())

        # Увеличенный Listbox с прокруткой
        list_frame = ctk.CTkFrame(font_window)
        list_frame.pack(expand=True, fill="both", padx=10, pady=10)

        font_list = tk.Listbox(list_frame, height=20, width=40, bg="white", font=("Arial", 12))
        font_list.pack(side="left", fill="both", expand=True)

        # Добавление полосы прокрутки
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=font_list.yview)
        scrollbar.pack(side="right", fill="y")
        font_list.config(yscrollcommand=scrollbar.set)

        # Добавляем шрифты в Listbox
        for font in fonts:
            font_list.insert(tk.END, font)

        # Метка для предпросмотра
        preview_label = ctk.CTkLabel(font_window, text="1234567890\nПредпросмотр текста", font=("Arial", 14))
        preview_label.pack(pady=10)

        # Обработчик выбора шрифта
        def update_preview(event=None):
            """Обновляет предпросмотр текста при выборе шрифта."""
            selection = font_list.curselection()
            if selection:  # Если есть выбранный элемент
                selected_font = font_list.get(selection)
                preview_label.configure(font=(selected_font, 14))  # Обновляем шрифт предпросмотра

        font_list.bind("<<ListboxSelect>>", update_preview)

        # Кнопка для подтверждения выбора шрифта
        def apply_font():
            selection = font_list.curselection()
            if selection:  # Если выбран шрифт
                selected_font = font_list.get(selection)
                self.text_area.configure(font=(selected_font, 14))  # Применяем шрифт к тексту
                self.config_data["font"] = selected_font  # Сохраняем шрифт в конфигурации
                save_config(self.config_data)  # Сохраняем изменения
                font_window.destroy()  # Закрываем окно выбора шрифта

        apply_button = ctk.CTkButton(font_window, text="Применить", command=apply_font)
        apply_button.pack(pady=10)

    def zoom_in(self):
        """Увеличивает масштаб текста."""
        self.zoom_factor += 0.1
        self.update_font()

    def zoom_out(self):
        """Уменьшает масштаб текста."""
        self.zoom_factor -= 0.1
        if self.zoom_factor < 0.5:  # Ограничение минимального масштаба
            self.zoom_factor = 0.5
        self.update_font()

    def reset_zoom(self):
        """Сбрасывает масштаб текста по умолчанию."""
        self.zoom_factor = self.default_zoom_factor
        self.update_font()

    def update_font(self):
        """Обновляет размер шрифта в текстовой области в зависимости от масштаба."""
        new_font_size = int(14 * self.zoom_factor)  # Изменение размера шрифта
        self.text_area.configure(font=(self.config_data['font'], new_font_size))

    def set_theme(self, theme):
        """Устанавливает тему и сохраняет её в конфигурации."""
        ctk.set_appearance_mode(theme)
        self.config_data["theme"] = theme
        save_config(self.config_data)

    def new_file(self):
        if self.confirm_save():
            self.text_area.delete("1.0", END)
            self.current_file = None
            self.saved_content = ""
            self.title("Текстовый редактор - Новый файл")

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"),
                                                         ("Word Documents", "*.docx"),
                                                         ("TextBlade Files", "*.txtb"),
                                                         ("All Files", "*.*")])
        if file_path:
            self.open_file(file_path)

    def open_file(self, file_path):
        if file_path.endswith(".txt"):
            # Открытие текстового файла
            if self.confirm_save():
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                self.text_area.delete("1.0", END)
                self.text_area.insert("1.0", content)
                self.current_file = file_path
                self.saved_content = content
                self.title(f"Текстовый редактор - {file_path}")

        elif file_path.endswith(".docx"):
            # Открытие Word документа
            if self.confirm_save():
                doc = Document(file_path)
                content = "\n".join([para.text for para in doc.paragraphs])  # Извлечение текста из абзацев
                self.text_area.delete("1.0", END)
                self.text_area.insert("1.0", content)
                self.current_file = file_path
                self.saved_content = content
                self.title(f"Текстовый редактор - {file_path}")

        elif file_path.endswith(".txtb"):
            # Открытие формата .txtb
            if self.confirm_save():
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                self.text_area.delete("1.0", END)
                self.text_area.insert("1.0", content)
                self.current_file = file_path
                self.saved_content = content
                self.title(f"Текстовый редактор - {file_path}")

        else:
            messagebox.showerror("Ошибка", "Невозможно открыть этот файл. Неподдерживаемый формат.")

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as file:
                file.write(self.text_area.get("1.0", END).strip())
            self.saved_content = self.text_area.get("1.0", END).strip()
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txtb",
                                                 filetypes=[("TextBlade Files", "*.txtb"), ("All Files", "*.*")])
        if file_path:
            content = self.text_area.get("1.0", END).strip()
            save_custom_file(content, file_path)
            self.current_file = file_path
            self.saved_content = content
            self.title(f"Текстовый редактор - {file_path}")

    def confirm_save(self):
        current_content = self.text_area.get("1.0", END).strip()
        if current_content != self.saved_content:
            response = messagebox.askyesnocancel("Сохранить изменения?", "Вы хотите сохранить изменения перед выходом?")
            if response:  # Сохранить
                self.save_file()
                return True
            elif response is None:  # Отмена
                return False
        return True

    def on_close(self):
        if self.confirm_save():
            # Сохранение настроек перед выходом
            save_config(self.config_data)
            self.destroy()


if __name__ == "__main__":
    app = TextEditor()
    app.mainloop()
