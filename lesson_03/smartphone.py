class Smartphone:
    marka = "Marka"
    model = "Model"
    number = "+7-999-999-99-99"

    def __init__(self, marka, model, number):
        self.marka = marka
        self.model = model
        self.number = number

    def __str__(self):
        return f"{self.marka} - {self.model}. {self.number}"
