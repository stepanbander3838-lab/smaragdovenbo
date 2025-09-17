import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "data.json"

# === Глобальні дані ===
data = {}  # структура {ID: {...}}


# === Завантаження даних з файлу ===
def load_data():
    global data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}


# === Збереження даних у файл ===
def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# === Перерахунок чистого доходу ===
def calculate_net_income(worker_id):
    worker = data.get(worker_id, {})
    income = float(worker.get("income", 0))
    fuel = float(worker.get("fuel", 0))
    service = float(worker.get("service", 0))
    insurance = float(worker.get("insurance", 0))

    deduction = income * 0.15
    total_expenses = fuel + service + insurance
    net = income - deduction - total_expenses
    return income, deduction, total_expenses, net


# === Вікно Income ===
def open_income_window():
    income_window = tk.Toplevel(root)
    income_window.title("Income Table")
    income_window.geometry("1000x450")

    columns = ("ID", "Name", "CarNumber", "Route", "Income", "-15%", "Expenses", "NetIncome")
    tree_income = ttk.Treeview(income_window, columns=columns, show="headings")
    for col in columns:
        tree_income.heading(col, text=col)
        tree_income.column(col, width=120, anchor="center")
    tree_income.pack(fill="both", expand=True)

    def refresh_table():
        for row in tree_income.get_children():
            tree_income.delete(row)
        for worker_id, info in data.items():
            income, deduction, expenses, net = calculate_net_income(worker_id)
            tree_income.insert("", "end", values=(
                worker_id,
                info.get("name", ""),
                info.get("car", ""),
                info.get("route", ""),
                f"{income:.2f}",
                f"{deduction:.2f}",
                f"{expenses:.2f}",
                f"{net:.2f}"
            ))

    def add_income_data():
        def save_income():
            worker_id = entry_id.get()
            name = entry_name.get()
            car = entry_car.get()
            route = entry_route.get()
            try:
                income = float(entry_income.get())
            except ValueError:
                messagebox.showerror("Error", "Income must be a number!")
                return

            if worker_id not in data:
                data[worker_id] = {}
            data[worker_id].update({
                "name": name,
                "car": car,
                "route": route,
                "income": income
            })

            save_data()
            refresh_table()
            form.destroy()

        form = tk.Toplevel(income_window)
        form.title("Add Income Data")

        tk.Label(form, text="ID:").grid(row=0, column=0)
        entry_id = tk.Entry(form)
        entry_id.grid(row=0, column=1)

        tk.Label(form, text="ПІБ:").grid(row=1, column=0)
        entry_name = tk.Entry(form)
        entry_name.grid(row=1, column=1)

        tk.Label(form, text="Номер машини:").grid(row=2, column=0)
        entry_car = tk.Entry(form)
        entry_car.grid(row=2, column=1)

        tk.Label(form, text="Рейс:").grid(row=3, column=0)
        entry_route = tk.Entry(form)
        entry_route.grid(row=3, column=1)

        tk.Label(form, text="Заробіток:").grid(row=4, column=0)
        entry_income = tk.Entry(form)
        entry_income.grid(row=4, column=1)

        tk.Button(form, text="Save", command=save_income).grid(row=5, column=0, columnspan=2)

    # кнопки управління
    btn_frame = tk.Frame(income_window)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Add Data", command=add_income_data).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Refresh", command=refresh_table).grid(row=0, column=1, padx=5)

    refresh_table()


# === Вікно Expense ===
def open_expense_window():
    expense_window = tk.Toplevel(root)
    expense_window.title("Expense Table")
    expense_window.geometry("900x450")

    columns = ("ID", "CarNumber", "Fuel", "Service", "Insurance", "TotalExpense")
    tree_expense = ttk.Treeview(expense_window, columns=columns, show="headings")
    for col in columns:
        tree_expense.heading(col, text=col)
        tree_expense.column(col, width=140, anchor="center")
    tree_expense.pack(fill="both", expand=True)

    def refresh_table():
        for row in tree_expense.get_children():
            tree_expense.delete(row)
        for worker_id, info in data.items():
            fuel = float(info.get("fuel", 0))
            service = float(info.get("service", 0))
            insurance = float(info.get("insurance", 0))
            total = fuel + service + insurance
            tree_expense.insert("", "end", values=(
                worker_id,
                info.get("car", ""),
                f"{fuel:.2f}",
                f"{service:.2f}",
                f"{insurance:.2f}",
                f"{total:.2f}"
            ))

    def add_expense_data():
        def save_expense():
            worker_id = entry_id.get()
            car = entry_car.get()
            try:
                fuel = float(entry_fuel.get())
                service = float(entry_service.get())
                insurance = float(entry_insurance.get())
            except ValueError:
                messagebox.showerror("Error", "Costs must be numbers!")
                return

            if worker_id not in data:
                data[worker_id] = {}
            data[worker_id].update({
                "car": car,
                "fuel": fuel,
                "service": service,
                "insurance": insurance
            })

            save_data()
            refresh_table()
            form.destroy()

        form = tk.Toplevel(expense_window)
        form.title("Add Expense Data")

        tk.Label(form, text="ID:").grid(row=0, column=0)
        entry_id = tk.Entry(form)
        entry_id.grid(row=0, column=1)

        tk.Label(form, text="Номер машини:").grid(row=1, column=0)
        entry_car = tk.Entry(form)
        entry_car.grid(row=1, column=1)

        tk.Label(form, text="Витрати на пальне:").grid(row=2, column=0)
        entry_fuel = tk.Entry(form)
        entry_fuel.grid(row=2, column=1)

        tk.Label(form, text="Витрати на обслуговування:").grid(row=3, column=0)
        entry_service = tk.Entry(form)
        entry_service.grid(row=3, column=1)

        tk.Label(form, text="Витрати на страхування:").grid(row=4, column=0)
        entry_insurance = tk.Entry(form)
        entry_insurance.grid(row=4, column=1)

        tk.Button(form, text="Save", command=save_expense).grid(row=5, column=0, columnspan=2)

    # кнопки управління
    btn_frame = tk.Frame(expense_window)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Add Data", command=add_expense_data).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Refresh", command=refresh_table).grid(row=0, column=1, padx=5)

    refresh_table()


# === Головне вікно ===
root = tk.Tk()
root.title("Main Menu")
root.geometry("300x200")

load_data()

tk.Button(root, text="Income", command=open_income_window, width=20, height=2).pack(pady=20)
tk.Button(root, text="Expense", command=open_expense_window, width=20, height=2).pack(pady=20)

root.mainloop()
