from ..Vehicle import Vehicle
class Truck(Vehicle):
    def __init__(self, vehicle_id: str, capacity: float, clients_list: list, color: str, current_load=0):
        super().__init__(vehicle_id, capacity, clients_list, current_load)
        self.color = color