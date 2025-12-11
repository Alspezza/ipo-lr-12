from ..Vehicle import Vehicle
from ..Client import Client
class TransportCompany:
    def __init__(self, name):
        self.name = name 
        self.vehicles = []
        self.clients = []

    def add_vehicle(self, vehicle):
        if not isinstance(vehicle, Vehicle):
            raise TypeError(f"Введено некорректное название транспортного средства: {vehicle}")
        for exc_veh in self.vehicles:
            if exc_veh == vehicle:
                raise TypeError(f"Введенное средство уже существует")
            if exc_veh.vehicle_id == vehicle.vehicle_id:
                raise TypeError("Введено уже существующее ID")
        self.vehicles.append(vehicle)
        self.clients += vehicle.clients_list
        return print(f"\nВ компанию {self.name} добавлено новое транспортное средство {vehicle}\n")
    


    def list_vehicles(self):
        return self.vehicles
    


    def list_clients(self):
        return self.clients
    


    def add_client(self, client):
        if not isinstance(client, Client):
            raise TypeError(f"Некорректно введен клиент: {client}")
        for cl in self.clients:
            if cl == client:
                raise TypeError(f"Введенный клиент уже существует")
        self.clients.append(client)
        return print(f"В компанию {self.name} успешно добавлен клиент: {client}")



    def optimize_cargo_distribution(self):
        vip_clients = [c for c in self.clients if c.is_vip]
        regular_clients = [c for c in self.clients if not c.is_vip]

        #key lambda - ключ сортировки который использует функцию c.cargo_weight и применияет ее к обьекту с
        sorted_vip_clients = sorted(vip_clients, key=lambda c: c.cargo_weight, reverse=True)
        sorted_regular_clients = sorted(regular_clients, key=lambda c: c.cargo_weight, reverse=True)
        sorted_clients = sorted_vip_clients + sorted_regular_clients

        valid_s_clients = [c for c in sorted_clients if c.cargo_weight > 0]

        

        sorted_vehicles = sorted(self.vehicles, key= lambda w: w.capacity, reverse=True)

        complete_cl = 0

        for clnt in valid_s_clients:
            for  vehicl in sorted_vehicles:
                avaliable_w = vehicl.capacity - vehicl.current_load
                if avaliable_w >= clnt.cargo_weight:
                    vehicl.current_load += clnt.cargo_weight
                    clnt.cargo_weight = 0
                    complete_cl += 1
                    break

        if complete_cl != len(valid_s_clients):
            return print(f"Не удалось поместить все грузы в транспорт")
        elif complete_cl == len(valid_s_clients):
            return print("Загрузка товаров прошла успешно")
