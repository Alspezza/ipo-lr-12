class Client:
    def __init__(self, name: str, cargo_weight: float, is_vip):
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip
    def __str__(self):
        return f"Имя клиента:{self.name} | Масса его груза: {self.cargo_weight} | Наличие вип: {self.is_vip}"