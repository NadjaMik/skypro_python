def month_to_season(mn):
    winter = "Зима"
    autumn = "Осень"
    summer = "Лето"
    spring = "Весна"
    mn = int(mn)
    if mn == 12 or mn == 1 or mn == 2:
        return winter
    elif mn == 3 or mn == 4 or mn == 5:
        return spring
    elif mn == 6 or mn == 7 or mn == 8:
        return summer
    elif mn == 9 or mn == 10 or mn == 11:
        return autumn
    else:
        print("Неверный месяц")


mn = input("Введите номер месяца ")
print("Сезон: ", month_to_season(mn))
