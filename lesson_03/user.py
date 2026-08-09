class User:
    first_name = "Name"
    last_name = "Last Name"

    def __init__(self, name, lastname):
        self.first_name = name
        self.last_name = lastname

    def sayFirstName(self):
        print("меня зовут ", self.first_name)

    def sayLastName(self):
        print("моя фамилия ", self.last_name)

    def sayName(self):
        print("мое имя и фамилия ", self.first_name, " ", self.last_name)
