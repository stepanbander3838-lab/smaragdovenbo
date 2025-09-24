import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from PIL import Image, ImageTk

DATA_FILE = "data.json"
data = {}

# ------------------ Работа с файлом ------------------
def load_data():
    global data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ------------------ Доходы ------------------
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
            if worker_id in data.get("trucks", {}):
                continue  # Пропускаем грузовики
            income, deduction, expenses_val, net = calculate_net_income(worker_id)
            tree_income.insert("", "end", values=(
                worker_id,
                info.get("name", ""),
                info.get("car", ""),
                info.get("route", ""),
                f"{income:.2f}",
                f"{deduction:.2f}",
                f"{expenses_val:.2f}",
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

    # кнопки управления
    btn_frame = tk.Frame(income_window)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Add Data", command=add_income_data).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Refresh", command=refresh_table).grid(row=0, column=1, padx=5)

    refresh_table()

# ------------------ Расходы ------------------
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
            if worker_id in data.get("trucks", {}):
                continue
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

    # кнопки управления
    btn_frame = tk.Frame(expense_window)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Add Data", command=add_expense_data).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Refresh", command=refresh_table).grid(row=0, column=1, padx=5)

    refresh_table()

# ------------------ Водители ------------------
def list_drivers():
    drivers_window = tk.Toplevel(root)
    drivers_window.title("Список водителей")
    drivers_window.geometry("600x400")

    columns = ("ID", "Name", "CarNumber",)
    tree_drivers = ttk.Treeview(drivers_window, columns=columns, show="headings")
    for col in columns:
        tree_drivers.heading(col, text=col)
        tree_drivers.column(col, width=150, anchor="center")
    tree_drivers.pack(fill="both", expand=True)

    def refresh_table():
        for row in tree_drivers.get_children():
            tree_drivers.delete(row)
        for worker_id, info in data.items():
            if worker_id in data.get("trucks", {}):
                continue
            tree_drivers.insert("", "end", values=(
                worker_id,
                info.get("name", ""),
                info.get("car", ""),
                info.get("route", "")
            ))

    btn_frame = tk.Frame(drivers_window)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Refresh", command=refresh_table).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Добавить водителя в базу данных ", command=add_driver).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Удалить водителя из базы данных", command=delete_driver).grid(row=0, column=2, padx=5)
    refresh_table()

def delete_driver():
    def confirm_delete():
        worker_id = entry_id.get()
        if worker_id in data:
            del data[worker_id]
            save_data()
            messagebox.showinfo("Success", f"Driver with ID {worker_id} deleted.")
            delete_window.destroy()
        else:
            messagebox.showerror("Error", "Driver ID not found.")

    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Driver")
    delete_window.geometry("300x150")

    tk.Label(delete_window, text="Enter Driver ID to delete:").pack(pady=10)
    entry_id = tk.Entry(delete_window)
    entry_id.pack(pady=5)
    tk.Button(delete_window, text="Удалить", command=confirm_delete).pack(pady=10)

# ------------------ Грузовики ------------------
def truck_list():
    truck_window = tk.Toplevel(root)
    truck_window.title("Truck List")
    truck_window.geometry("600x400")

    columns = ("ID", "CarNumber", "Model", "Year")
    tree_truck = ttk.Treeview(truck_window, columns=columns, show="headings")
    for col in columns:
        tree_truck.heading(col, text=col)
        tree_truck.column(col, width=150, anchor="center")
    tree_truck.pack(fill="both", expand=True)

    def refresh_table():
        for row in tree_truck.get_children():
            tree_truck.delete(row)
        for truck_id, info in data.get("trucks", {}).items():
            tree_truck.insert("", "end", values=(
                truck_id,
                info.get("car", ""),
                info.get("model", ""),
                info.get("year", "")
            ))

    tk.Button(truck_window, text="Добавить грузовик в базу данных ", 
              command=lambda: add_truck(truck_window, refresh_table),
              width=30, height=2).pack(pady=20)
    tk.Button(truck_window, text="Refresh", command=refresh_table).pack()

    refresh_table()

def add_truck(truck_window, refresh_table):
    def save_truck():
        truck_id = entry_id.get()
        car = entry_car.get()
        model = entry_model.get()
        year = entry_year.get()

        if "trucks" not in data:
            data["trucks"] = {}

        if truck_id in data["trucks"]:
            messagebox.showerror("Error", "Truck ID already exists!")
            return

        data["trucks"][truck_id] = {
            "car": car,
            "model": model,
            "year": year
        }

        save_data()
        messagebox.showinfo("Success", f"Truck with ID {truck_id} added.")
        add_window.destroy()
        refresh_table()

    add_window = tk.Toplevel(truck_window)
    add_window.title("Add Truck")
    add_window.geometry("300x250")

    tk.Label(add_window, text="ID:").grid(row=0, column=0)
    entry_id = tk.Entry(add_window)
    entry_id.grid(row=0, column=1)
    tk.Label(add_window, text="Номер машини:").grid(row=1, column=0)
    entry_car = tk.Entry(add_window)
    entry_car.grid(row=1, column=1)
    tk.Label(add_window, text="Модель:").grid(row=2, column=0)
    entry_model = tk.Entry(add_window)
    entry_model.grid(row=2, column=1)
    tk.Label(add_window, text="Рік випуску:").grid(row=3, column=0)
    entry_year = tk.Entry(add_window)
    entry_year.grid(row=3, column=1)
    tk.Button(add_window, text="Save", command=save_truck).grid(row=4, column=0, columnspan=2)

# ------------------ Водители ------------------
def add_driver():
    def save_driver():
        worker_id = entry_id.get()
        name = entry_name.get()
        car = entry_car.get()

        if worker_id in data:
            messagebox.showerror("Error", "Driver ID already exists!")
            return

        data[worker_id] = {
            "name": name,
            "car": car,
        }

        save_data()
        messagebox.showinfo("Success", f"Driver with ID {worker_id} added.")
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title("Add Driver")
    add_window.geometry("300x250")

    tk.Label(add_window, text="ID:").grid(row=0, column=0)
    entry_id = tk.Entry(add_window)
    entry_id.grid(row=0, column=1)

    tk.Label(add_window, text="ПІБ:").grid(row=1, column=0)
    entry_name = tk.Entry(add_window)
    entry_name.grid(row=1, column=1)

    tk.Label(add_window, text="Номер машини:").grid(row=2, column=0)
    entry_car = tk.Entry(add_window)
    entry_car.grid(row=2, column=1)

    tk.Button(add_window, text="Save", command=save_driver).grid(row=4, column=0, columnspan=2)

# ------------------ Главное окно ------------------
root = tk.Tk()
root.title("Система управления финансами и водителями")
root.geometry("1920x1080")

load_data()

tk.Button(root, text="Доход", command=open_income_window, width=20, height=2).pack(pady=20)
tk.Button(root, text="Расходы", command=open_expense_window, width=20, height=2).pack(pady=20)
tk.Button(root, text="Список водителей ", command=list_drivers, width=20, height=2).pack(pady=20)
tk.Button(root, text="Список грузовиков", command=truck_list, width=20, height=2).pack(pady=20)

root.mainloop()
