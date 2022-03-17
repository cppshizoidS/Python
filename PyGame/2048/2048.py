def pretty_print(mas):
    print('-'*10)
    for row in mas:
        print(*row)
    print('-' * 10)
mas = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]

mas[1][2] = 2
mas[3][0] = 4
pretty_print(mas)
