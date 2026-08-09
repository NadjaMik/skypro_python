class Adress:
    def __init__(self, index, city, street, building_number, apartment_number):
        self.index = index
        self.city = city
        self.street = street
        self.building_number = building_number
        self.apartment_number = apartment_number

    def __str__(self):
        return (f"{self.index}, {self.city}"
                f"{self.street}, {self.building_number}"
                f" - {self.apartment_number}")
