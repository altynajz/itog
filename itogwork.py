import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
from datetime import datetime

API_KEY = "YOUR_API_KEY"
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

HISTORY_FILE = "history.json"

currencies = [
    "USD", "EUR", "RUB", "KZT", "GBP",
    "JPY", "CNY", "TRY", "AED", "CHF"
]


class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("700x500")

        # Сумма
        tk.Label(root, text="Введите сумму:").pack(pady=5)

        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack(pady=5)

        # Валюта ИЗ
        tk.Label(root, text="Из валюты:").pack()

        self.from_currency = ttk.Combobox(root, values=currencies)
        self.from_currency.current(0)
        self.from_currency.pack(pady=5)

        # Валюта В
        tk.Label(root, text="В валюту:").pack()

        self.to_currency = ttk.Combobox(root, values=currencies)
        self.to_currency.current(1)
        self.to_currency.pack(pady=5)

        # Кнопка
        tk.Button(
            root,
            text="Конвертировать",
            command=self.convert_currency
        ).pack(pady=10)

        # Результат
        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        # Таблица истории
        columns = ("date", "operation")

        self.tree = ttk.Treeview(root, columns=columns, show="headings")

        self.tree.heading("date", text="Дата")
        self.tree.heading("operation", text="Операция")

        self.tree.column("date", width=150)
        self.tree.column("operation", width=500)

        self.tree.pack(fill="both", expand=True, pady=10)

        self.load_history()

    def convert_currency(self):
        amount = self.amount_entry.get()

        # Проверка ввода
        try:
            amount = float(amount)

            if amount <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Ошибка",
                "Введите положительное число!"
            )
            return

        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()

        try:
            response = requests.get(BASE_URL + from_curr)
            data = response.json()

            if data["result"] != "success":
                messagebox.showerror(
                    "Ошибка API",
                    "Не удалось получить курс валют."
                )
                return

            rate = data["conversion_rates"][to_curr]

            result = amount * rate

            text = f"{amount} {from_curr} = {round(result, 2)} {to_curr}"

            self.result_label.config(text=text)

            self.save_history(text)

        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                f"Произошла ошибка:\n{e}"
            )

    def save_history(self, operation):
        record = {
            "date": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "operation": operation
        }

        history = []

        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                try:
                    history = json.load(file)
                except:
                    history = []

        history.append(record)

        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(history, file, ensure_ascii=False, indent=4)

        self.tree.insert(
            "",
            tk.END,
            values=(record["date"], record["operation"])
        )

    def load_history(self):
        if not os.path.exists(HISTORY_FILE):
            return

        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            try:
                history = json.load(file)

                for item in history:
                    self.tree.insert(
                        "",
                        tk.END,
                        values=(item["date"], item["operation"])
                    )

            except:
                pass


root = tk.Tk()
app = CurrencyConverter(root)
root.mainloop()