class Mailing:
    def __init__(self, to_adress, from_adress, cost, track):
        self.to_adress = to_adress
        self.from_adress = from_adress
        self.cost = cost
        self.track = track

    def __str__(self):
        return (f"Отправление {self.track} из "
                f"{self.from_adress.index}, {self.from_adress.city}, "
                f"{self.from_adress.street}, "
                f"{self.from_adress.building_number} - "
                f"{self.from_adress.apartment_number} в "
                f"{self.to_adress.index}, {self.to_adress.city}, "
                f"{self.to_adress.street}, {self.to_adress.building_number} - "
                f"{self.to_adress.apartment_number}. "
                f"Стоимость {self.cost} рублей.")
