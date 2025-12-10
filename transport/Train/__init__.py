from ..Vehicle import Vehicle
class Train(Vehicle):
    def __init__(self, vehicle_id: str, capacity: float, clients_list: list, number_of_cars: int, current_load=0):
        super().__init__(vehicle_id, capacity, clients_list, current_load)
        self.number_of_cars = number_of_cars