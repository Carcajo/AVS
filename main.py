import math
import re
from math import copysign, fabs, floor, isfinite, modf

def float_to_bin_fixed(f):
    if not isfinite(f):
        return repr(f)
    sign = '-' * (copysign(1.0, f) < 0)
    frac, fint = modf(fabs(f))  # разбить на дробные, целые части
    n, d = frac.as_integer_ratio()  # frac = числитель / знаменатель
    assert d & (d - 1) == 0
    return f'{sign}{floor(fint):b}.{n:0{d.bit_length() - 1}b}'

def add_binary_decimals(decimal_num1, decimal_num2):
    decimal_str1 = str(decimal_num1)
    decimal_str2 = str(decimal_num2)
    int_part1, frac_part1 = decimal_str1.split('.')
    int_part2, frac_part2 = decimal_str2.split('.')
    max_len = max(len(frac_part1), len(frac_part2))
    frac_part1 = frac_part1.ljust(max_len, '0')
    frac_part2 = frac_part2.ljust(max_len, '0')
    frac_sum = int(frac_part1, 2) + int(frac_part2, 2)
    int_part_sum = frac_sum // 2
    frac_sum_binary = bin(frac_sum % 2**max_len).replace("0b", "").rjust(max_len, '0')
    int_sum = int(int_part1) + int(int_part2) + int_part_sum
    int_sum_binary = float_to_bin_fixed(int_sum)
    return int_sum_binary + '.' + frac_sum_binary

def frange(start, stop, step):
    i = 0
    while True:
        value = start + i * step
        if value >= stop:
            break
        yield value
        i += 1
a = float(input("Введите начальное значение аргумента x: "))
b = float(input("Введите конечное значение аргумента x: "))
h = float(input("Введите шаг изменения аргумента x: "))
eps = input("Введите требуемую точность ε: ")
while re.match(r'^[-0-9]*$', eps) is None:
    print("Error. Try again")
    eps = input()

# Создаем пустые списки для хранения результатов
x_list = []
y_list = []
s_list = []
n_list = []

# Вычисляем значения функции Y(x), суммы S(x) и число итераций n
for x in frange(a, b, h):
    y = math.sin(x) + math.cos(x)
    s = 0
    n = 0
    while True:
        n += 1
        s += (-1)**(n+1) * x**(2*n-1) / math.factorial(2*n-1)
        if abs(y - s) < int(eps):
            break
    x_list.append(x)
    y_list.append(y)
    s_list.append(s)
    n_list.append(n)

# Выводим результаты в виде таблицы
print("{:<10} {:<10} {:<10} {:<10}".format("x", "Y(x)", "S(x)", "n"))
for i in range(len(x_list)):
    print("{:<10.3f} {:<10.3f} {:<10.3f} {:<10}".format(x_list[i], y_list[i], s_list[i], n_list[i]))
