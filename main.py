import math
from math import copysign, fabs, floor, isfinite, modf

def float_to_bin_fixed(f):
    if not isfinite(f):
        return repr(f)
    sign = '-' * (copysign(1.0, f) < 0)
    frac, fint = modf(fabs(f))  # разбить на дробные, целые части
    n, d = frac.as_integer_ratio()  # frac = числитель / знаменатель
    assert d & (d - 1) == 0
    return f'{sign}{floor(fint):b}.{n:0{d.bit_length() - 1}b}'

def add_binary_decimals(a, b):
    a_int, a_frac = str(a).split('.')
    b_int, b_frac = str(b).split('.')
    a_int = bin(int(a_int))[2:]
    b_int = bin(int(b_int))[2:]
    a_frac = float_to_bin_fixed(float('0.' + a_frac))
    b_frac = float_to_bin_fixed(float('0.' + b_frac))
    len_diff = abs(len(a_frac) - len(b_frac))
    if len(a_frac) > len(b_frac):
        b_frac += '0' * len_diff
    else:
        a_frac += '0' * len_diff

    result_int = bin(int(a_int, 2) + int(b_int, 2))[2:]
    result_frac = ''
    carry = 0
    for i in range(len(a_frac) - 1, -1, -1):
        bit_sum = int(a_frac[i], 2) + int(b_frac[i], 2) + carry
        if bit_sum >= 2:
            bit_sum -= 2
            carry = 1
        else:
            carry = 0
        result_frac = str(bit_sum) + result_frac
    if carry:
        result_int = bin(int(result_int, 2) + 1)[2:]
    return result_int + '.' + result_frac

a = float(input("Введите первое число: "))
a1 = float_to_bin_fixed(a)
b = float(input("Введите второе число: "))
b1 = float_to_bin_fixed(b)
summa = a+b
summa1 = float_to_bin_fixed(summa)
diff = a-b
diff1 = float_to_bin_fixed(diff)
mult = a*b
mult1 = float_to_bin_fixed(mult)
dev = a/b
dev1 = float_to_bin_fixed(dev)

print("Сумма в двоичном виде: ", summa1)
print("Сумма в десятичном виде: ", summa)

print("Разность в двоичном виде: ", diff1)
print("Разность в десятичном виде: ", diff)

print("Произведение в двоичном виде: ", mult1)
print("Произведение в десятичном виде: ", mult)

print("Деление в двоичном виде: ", dev1)
print("Деление в десятичном виде: ", dev)