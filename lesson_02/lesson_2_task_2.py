def is_year_leap(year):
    if (int(year) % 4 == 0):
        return True
    else:
        return False


year = input("Введите год: ")
print("Год: ", year, " ", is_year_leap(year))
