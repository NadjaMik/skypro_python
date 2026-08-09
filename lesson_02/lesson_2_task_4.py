def fizz_buzz(n):
    n = int(n)
    for n in range(1, n):
        if (n % 3 == 0) and (n % 5 == 0):
            print("FizzBuzz")
        elif (n % 5 == 0):
            print("Buzz")
        elif (n % 3 == 0):
            print("Fizz")
        else:
            print(n)


n = input("Введите число ")
fizz_buzz(n)
