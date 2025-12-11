import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from transport.Vehicle import Vehicle
from transport.TransportCompany import TransportCompany
from transport.Client import Client

class TransportCompanyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Транспортная компания")
        self.root.geometry("800x600")
        
        self.company = TransportCompany("Транспортная компания")
        
        # Переменные для хранения данных
        self.vehicle_clients = []
        
        self.create_widgets()
        
    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(
            self.root, 
            text="Транспортная компания", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Вкладки
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Создаем вкладки
        tabs = [
            ("ТС", self.create_vehicles_tab),
            ("Клиенты", self.create_clients_tab),
            ("Добавить ТС", self.create_add_vehicle_tab),
            ("Добавить клиента", self.create_add_client_tab),
            ("Распределение", self.create_distribution_tab)
        ]
        
        for tab_name, tab_func in tabs:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=tab_name)
            tab_func(frame)
        
        # Кнопка выхода
        exit_btn = tk.Button(
            self.root,
            text="Выход",
            command=self.root.quit,
            width=20
        )
        exit_btn.pack(pady=10)
    
    def create_vehicles_tab(self, parent):
        # Кнопка обновления
        refresh_btn = tk.Button(
            parent,
            text="Обновить список",
            command=self.show_vehicles
        )
        refresh_btn.pack(pady=5)
        
        # Поле для отображения списка
        self.vehicles_text = scrolledtext.ScrolledText(
            parent,
            height=15,
            width=70,
            font=("Courier", 10)
        )
        self.vehicles_text.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.show_vehicles()
    
    def create_clients_tab(self, parent):
        # Кнопка обновления
        refresh_btn = tk.Button(
            parent,
            text="Обновить список",
            command=self.show_clients
        )
        refresh_btn.pack(pady=5)
        
        # Поле для отображения списка
        self.clients_text = scrolledtext.ScrolledText(
            parent,
            height=15,
            width=70,
            font=("Courier", 10)
        )
        self.clients_text.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.show_clients()
    
    def create_add_vehicle_tab(self, parent):
        # Поля ввода
        fields = [
            ("ID транспортного средства:", "vehicle_id"),
            ("Вместимость (тонны):", "capacity"),
            ("Загруженность (тонны):", "load")
        ]
        
        self.entries = {}
        
        for i, (label_text, name) in enumerate(fields):
            tk.Label(parent, text=label_text).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry = tk.Entry(parent, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[name] = entry
        
        # Список клиентов ТС
        tk.Label(parent, text="Клиенты этого ТС:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        
        self.clients_listbox = tk.Listbox(parent, height=6, width=40)
        self.clients_listbox.grid(row=3, column=1, rowspan=2, padx=10, pady=5, sticky="nsew")
        
        # Кнопки для управления клиентами
        btn_frame = tk.Frame(parent)
        btn_frame.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        
        tk.Button(btn_frame, text="Добавить клиента", 
                 command=self.add_client_to_vehicle).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Удалить", 
                 command=self.remove_client_from_vehicle).pack(side="left", padx=2)
        
        # Кнопка добавления ТС
        add_btn = tk.Button(
            parent,
            text="Добавить транспортное средство",
            command=self.add_vehicle,
            width=30
        )
        add_btn.grid(row=5, column=0, columnspan=2, pady=20)
    
    def create_add_client_tab(self, parent):
        # Поля ввода
        tk.Label(parent, text="Имя клиента:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.client_name = tk.Entry(parent, width=30)
        self.client_name.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(parent, text="Вес груза (тонны):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.client_weight = tk.Entry(parent, width=30)
        self.client_weight.grid(row=1, column=1, padx=10, pady=5)
        
        # VIP статус
        tk.Label(parent, text="VIP статус:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        
        self.vip_var = tk.BooleanVar(value=False)
        vip_frame = tk.Frame(parent)
        vip_frame.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        tk.Radiobutton(vip_frame, text="Обычный", variable=self.vip_var, 
                      value=False).pack(side="left")
        tk.Radiobutton(vip_frame, text="VIP", variable=self.vip_var, 
                      value=True).pack(side="left", padx=10)
        
        # Кнопка добавления
        add_btn = tk.Button(
            parent,
            text="Добавить клиента",
            command=self.add_client,
            width=20
        )
        add_btn.grid(row=3, column=0, columnspan=2, pady=20)
    
    def create_distribution_tab(self, parent):
        # Инструкция
        tk.Label(
            parent,
            text="Оптимизация распределения грузов",
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        tk.Label(
            parent,
            text="Нажмите кнопку для запуска оптимизации",
            font=("Arial", 10)
        ).pack(pady=5)
        
        # Кнопка оптимизации
        optimize_btn = tk.Button(
            parent,
            text="Запустить оптимизацию",
            command=self.optimize_distribution,
            width=25
        )
        optimize_btn.pack(pady=20)
        
        # Результаты
        tk.Label(parent, text="Результаты:").pack(pady=5)
        
        self.result_text = scrolledtext.ScrolledText(
            parent,
            height=15,
            width=70,
            font=("Courier", 10)
        )
        self.result_text.pack(pady=10, padx=10, fill="both", expand=True)
    
    def show_vehicles(self):
        """Показать список транспортных средств"""
        self.vehicles_text.delete(1.0, tk.END)
        
        vehicles = self.company.list_vehicles()
        
        if not vehicles:
            self.vehicles_text.insert(tk.END, "Нет транспортных средств\n")
            return
        
        for vehicle in vehicles:
            self.vehicles_text.insert(tk.END, f"ID: {vehicle.vehicle_id}\n")
            self.vehicles_text.insert(tk.END, f"  Вместимость: {vehicle.capacity} т\n")
            self.vehicles_text.insert(tk.END, f"  Загруженность: {vehicle.current_load} т\n")
            self.vehicles_text.insert(tk.END, f"  Клиентов: {len(vehicle.clients_list)}\n")
            
            if vehicle.clients_list:
                self.vehicles_text.insert(tk.END, "  Клиенты:\n")
                for client in vehicle.clients_list:
                    vip = "VIP" if client.is_vip else "обычный"
                    self.vehicles_text.insert(tk.END, f"    - {client.name} ({client.cargo_weight} т, {vip})\n")
            
            self.vehicles_text.insert(tk.END, "-" * 40 + "\n")
    
    def show_clients(self):
        """Показать список клиентов"""
        self.clients_text.delete(1.0, tk.END)
        
        clients = self.company.list_clients()
        
        if not clients:
            self.clients_text.insert(tk.END, "Нет клиентов\n")
            return
        
        for client in clients:
            vip = "VIP" if client.is_vip else "обычный"
            self.clients_text.insert(tk.END, f"Имя: {client.name}\n")
            self.clients_text.insert(tk.END, f"  Вес груза: {client.cargo_weight} т\n")
            self.clients_text.insert(tk.END, f"  Статус: {vip}\n")
            self.clients_text.insert(tk.END, "-" * 30 + "\n")
    
    def add_client_to_vehicle(self):
        """Добавить клиента к транспортному средству"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить клиента")
        dialog.geometry("300x250")
        
        # Поля ввода
        tk.Label(dialog, text="Имя:").pack(pady=5)
        name_entry = tk.Entry(dialog, width=25)
        name_entry.pack(pady=5)
        
        tk.Label(dialog, text="Вес груза:").pack(pady=5)
        weight_entry = tk.Entry(dialog, width=25)
        weight_entry.pack(pady=5)
        
        tk.Label(dialog, text="VIP:").pack(pady=5)
        vip_var = tk.BooleanVar(value=False)
        tk.Checkbutton(dialog, text="VIP клиент", variable=vip_var).pack()
        
        def save_client():
            try:
                name = name_entry.get()
                weight = float(weight_entry.get())
                is_vip = vip_var.get()
                
                if not name:
                    messagebox.showerror("Ошибка", "Введите имя")
                    return
                
                # Создаем клиента
                client = Client(name, weight, is_vip)
                self.vehicle_clients.append(client)
                
                # Добавляем в список
                self.clients_listbox.insert(tk.END, f"{name} ({weight} т)")
                
                # Добавляем в компанию
                #self.company.add_client(client)
                
                dialog.destroy()
                messagebox.showinfo("Успех", "Клиент добавлен")
                
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный вес")
        
        tk.Button(dialog, text="Добавить", command=save_client).pack(pady=20)
    
    def remove_client_from_vehicle(self):
        """Удалить клиента из списка"""
        selection = self.clients_listbox.curselection()
        if selection:
            index = selection[0]
            self.clients_listbox.delete(index)
            del self.vehicle_clients[index]
    
    def add_vehicle(self):
        """Добавить транспортное средство"""
        try:
            # Получаем данные из полей
            vehicle_id = self.entries["vehicle_id"].get()
            capacity = float(self.entries["capacity"].get())
            load = float(self.entries["load"].get())
            
            if not vehicle_id:
                messagebox.showerror("Ошибка", "Введите ID")
                return
            
            # Создаем ТС
            vehicle = Vehicle(vehicle_id, capacity, self.vehicle_clients.copy(), load)
            self.company.add_vehicle(vehicle)
            
            # Очищаем поля
            for entry in self.entries.values():
                entry.delete(0, tk.END)
            self.clients_listbox.delete(0, tk.END)
            self.vehicle_clients.clear()
            
            messagebox.showinfo("Успех", "ТС добавлено")
            self.show_vehicles()
            
        except ValueError:
            messagebox.showerror("Ошибка", "Неверные числовые значения")
    
    def add_client(self):
        """Добавить отдельного клиента"""
        try:
            name = self.client_name.get()
            weight = float(self.client_weight.get())
            is_vip = self.vip_var.get()
            
            if not name:
                messagebox.showerror("Ошибка", "Введите имя")
                return
            
            # Создаем клиента
            client = Client(name, weight, is_vip)
            self.company.add_client(client)
            
            # Очищаем поля
            self.client_name.delete(0, tk.END)
            self.client_weight.delete(0, tk.END)
            self.vip_var.set(False)
            
            messagebox.showinfo("Клиент добавлен")
            self.show_clients()
            
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный вес")
    
    def optimize_distribution(self):
        """Запустить оптимизацию распределения"""
        try:
            self.company.optimize_cargo_distribution()
            
            # Показываем результаты
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Оптимизация завершена!\n\n")
            
            # Показываем обновленные списки
            self.show_vehicles()
            self.show_clients()
            
            messagebox.showinfo("Успех", "Распределение оптимизировано")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")

def main():
    root = tk.Tk()
    app = TransportCompanyGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()