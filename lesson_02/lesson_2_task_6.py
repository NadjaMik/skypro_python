lst = [11, 5, 8, 32, 15, 3, 20, 132, 21, 4, 555, 9, 20]
le = len(lst)

for n in range(le):
    if lst[n] < 30 and lst[n] % 3 == 0:
        print(lst[n])
