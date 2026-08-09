from adress import Adress
from mailing import Mailing


from_address = Adress(
    index="123456",
    city="Москва",
    street="Тверская",
    building_number=15,
    apartment_number=42
)

to_address = Adress(
    index="654321",
    city="Санкт-Петербург",
    street="Невский проспект",
    building_number=10,
    apartment_number=7
)

mailing = Mailing(
    to_adress=to_address,
    from_adress=from_address,
    cost=350.50,
    track="ABC123456789"
)

print(mailing)
