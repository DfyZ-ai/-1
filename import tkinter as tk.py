import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime


# ------------------ Файлы для хранения ------------------
QUOTES_FILE = "quotes.json"
HISTORY_FILE = "history.json"

# ------------------ Начальные цитаты ------------------
DEFAULT_QUOTES = [
    {"text": "Будь изменением, которое ты хочешь увидеть в мире.", "author": "Махатма Ганди", "theme": "Мотивация"},
    {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон", "theme": "Жизнь"},
    {"text": "Воображение важнее знания.", "author": "Альберт Эйнштейн", "theme": "Наука"},
    {"text": "Только тот, кто рискует идти далеко, может узнать, как далеко можно зайти.", "author": "Т.С. Элиот", "theme": "Смелость"},
    {"text": "Сложно победить того, кто никогда не сдаётся.", "author": "Бейб Рут", "theme": "Настойчивость"}
]

# ------------------ Загрузка / сохранение ------------------
def load_data(file, default):
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        save_data(file, default)
        return default

def save_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ------------------ Основное приложение ------------------
class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("700x550")
        self.root.resizable(True, True)

        # Данные
        self.quotes = load_data(QUOTES_FILE, DEFAULT_QUOTES)
        self.history = load_data(HISTORY_FILE, [])

        # Переменные для фильтров
        self.filter_author_var = tk.StringVar()
        self.filter_theme_var = tk.StringVar()

        # Интерфейс
        self.create_widgets()
        self.update_author_filter()
        self.update_theme_filter()

        # При закрытии — сохраняем историю
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # Рамка для отображения цитаты
        self.frame_quote = tk.LabelFrame(self.root, text="Случайная цитата", padx=10, pady=10)
        self.frame_quote.pack(fill="both", expand=True, padx=10, pady=5)

        self.lbl_quote_text = tk.Label(self.frame_quote, text="Нажмите «Сгенерировать»", font=("Arial", 12), wraplength=600, justify="left")
        self.lbl_quote_text.pack(pady=5)

        self.lbl_quote_author = tk.Label(self.frame_quote, text="", font=("Arial", 10, "italic"))
        self.lbl_quote_author.pack(pady=5)

        # Кнопка генерации
        self.btn_generate = tk.Button(self.root, text="✨ Сгенерировать цитату", command=self.generate_quote, font=("Arial", 11), bg="#4CAF50", fg="white")
        self.btn_generate.pack(pady=10)

        # Рамка фильтров
        self.frame_filters = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=5)
        self.frame_filters.pack(fill="x", padx=10, pady=5)

        # Фильтр по автору
        tk.Label(self.frame_filters, text="Автор:").grid(row=0, column=0, sticky="w", padx=5)
        self.author_combo = ttk.Combobox(self.frame_filters, textvariable=self.filter_author_var, state="readonly")
        self.author_combo.grid(row=0, column=1, padx=5, pady=5)
        self.author_combo.bind("<<ComboboxSelected>>", lambda e: self.filter_history())

        # Фильтр по теме
        tk.Label(self.frame_filters, text="Тема:").grid(row=0, column=2, sticky="w", padx=5)
        self.theme_combo = ttk.Combobox(self.frame_filters, textvariable=self.filter_theme_var, state="readonly")
        self.theme_combo.grid(row=0, column=3, padx=5, pady=5)
        self.theme_combo.bind("<<ComboboxSelected>>", lambda e: self.filter_history())

        # Кнопка сброса фильтров
        self.btn_reset_filters = tk.Button(self.frame_filters, text="Сбросить фильтры", command=self.reset_filters)
        self.btn_reset_filters.grid(row=0, column=4, padx=10)

        # История
        self.frame_history = tk.LabelFrame(self.root, text="История цитат", padx=10, pady=5)
        self.frame_history.pack(fill="both", expand=True, padx=10, pady=5)

        self.history_listbox = tk.Listbox(self.frame_history, height=10)
        self.history_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.frame_history, orient="vertical", command=self.history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_listbox.config(yscrollcommand=scrollbar.set)

        # Кнопка добавления новой цитаты
        self.btn_add_quote = tk.Button(self.root, text="➕ Добавить новую цитату", command=self.add_quote_dialog)
        self.btn_add_quote.pack(pady=5)

        self.update_history_display()

    def update_author_filter(self):
        authors = sorted(set(q["author"] for q in self.quotes))
        self.author_combo["values"] = ["Все"] + authors
        self.filter_author_var.set("Все")

    def update_theme_filter(self):
        themes = sorted(set(q["theme"] for q in self.quotes))
        self.theme_combo["values"] = ["Все"] + themes
        self.filter_theme_var.set("Все")

    def generate_quote(self):
        if not self.quotes:
            messagebox.showwarning("Нет цитат", "Добавьте хотя бы одну цитату.")
            return

        # Фильтруем цитаты для генерации (все цитаты доступны, но для истории оставим как есть)
        quote = random.choice(self.quotes)

        self.lbl_quote_text.config(text=f"«{quote['text']}»")
        self.lbl_quote_author.config(text=f"— {quote['author']} (Тема: {quote['theme']})")

        # Сохраняем в историю с датой
        history_entry = {
            "text": quote["text"],
            "author": quote["author"],
            "theme": quote["theme"],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(history_entry)
        self.update_history_display()

    def update_history_display(self):
        self.history_listbox.delete(0, tk.END)
        filtered = self.get_filtered_history()
        for entry in filtered:
            display = f"[{entry['date']}] {entry['author']}: «{entry['text'][:60]}...» (Тема: {entry['theme']})"
            self.history_listbox.insert(tk.END, display)

    def get_filtered_history(self):
        filtered = self.history
        author_filter = self.filter_author_var.get()
        theme_filter = self.filter_theme_var.get()

        if author_filter != "Все":
            filtered = [h for h in filtered if h["author"] == author_filter]
        if theme_filter != "Все":
            filtered = [h for h in filtered if h["theme"] == theme_filter]
        return filtered

    def filter_history(self):
        self.update_history_display()

    def reset_filters(self):
        self.filter_author_var.set("Все")
        self.filter_theme_var.set("Все")
        self.update_history_display()

    def add_quote_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить цитату")
        dialog.geometry("400x250")
        dialog.grab_set()

        tk.Label(dialog, text="Текст цитаты:").pack(pady=5)
        entry_text = tk.Text(dialog, height=5, width=50)
        entry_text.pack(pady=5)

        tk.Label(dialog, text="Автор:").pack(pady=5)
        entry_author = tk.Entry(dialog, width=40)
        entry_author.pack(pady=5)

        tk.Label(dialog, text="Тема:").pack(pady=5)
        entry_theme = tk.Entry(dialog, width=40)
        entry_theme.pack(pady=5)

        def save_new_quote():
            text = entry_text.get("1.0", tk.END).strip()
            author = entry_author.get().strip()
            theme = entry_theme.get().strip()

            # Проверка корректности ввода (пустые строки)
            if not text or not author or not theme:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
                return

            new_quote = {"text": text, "author": author, "theme": theme}
            self.quotes.append(new_quote)
            save_data(QUOTES_FILE, self.quotes)

            # Обновляем фильтры
            self.update_author_filter()
            self.update_theme_filter()

            messagebox.showinfo("Успех", "Цитата добавлена!")
            dialog.destroy()

        tk.Button(dialog, text="Сохранить", command=save_new_quote, bg="#4CAF50", fg="white").pack(pady=10)

    def on_close(self):
        save_data(HISTORY_FILE, self.history)
        self.root.destroy()

# ------------------ Запуск приложения ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()