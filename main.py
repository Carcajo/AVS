import re


def from_dec_to_binary(num):
    sign = False
    if int(num) < 0:
        sign = True
    binary = ""
    num = abs(num)
    while num > 0:
        left = num % 2
        binary = binary + str(left)
        num //= 2
    while len(binary) != 32:
        binary = binary + "0"
    if sign:
        binary = binary[:31] + "1"
    return binary[::-1]


def from_addit_to_binary(additional):
    if additional[0] == "0":
        return additional
    i = 0
    additional = additional[::-1]
    for c in additional:
        if c != "1":
            i += 1
        else:
            break
    reverse = ("1" * i) + "0" + additional[i+1:]
    reverse = reverse[::-1]
    binary = reverse[0]
    for c in reverse[1:]:
        if c == "1":
            binary = binary + "0"
        else:
            binary = binary + "1"
    return binary


def to_additional(num):
    binary = from_dec_to_binary(num)
    if int(num) > 0:
        return binary
    reverse = binary[0]
    for c in binary[1:]:
        if c == "1":
            reverse = reverse + "0"
        else:
            reverse = reverse + "1"
    i = 0
    additional = reverse[::-1]
    for c in additional:
        if c != "0":
            i += 1
        else:
            break
    additional = ("0" * i) + "1" + additional[i+1:]
    if len(additional) > 32:
        additional = additional[1:]
    return additional[::-1]


def to_dec(binary):
    res = 0
    index = 0
    binary = binary[::-1]
    for c in binary[:31]:
        if c == "1":
            res += pow(2, index)
        index += 1
    if binary[31] == "1":
        res *= -1
    return res


def add(num1, num2):
    add1 = to_additional(num1)
    add2 = to_additional(num2)
    res = sum(add1, add2)
    return from_addit_to_binary(res)


def sub(num1, num2):
    return add(num1, -num2)


def div(num1, num2):
    sign = False
    if (num1 < 0 < num2) or (num1 > 0 > num2):
        sign = True
    num1 = abs(num1)
    num2 = abs(num2)
    bin1 = from_dec_to_binary(num1)
    bin2 = from_dec_to_binary(num2)
    k1 = 0
    for i in range(1, 32):
        if bin1[i] == "1":
            k1 = i
            break
    k2 = 0
    for i in range(1, 32):
        if bin2[i] == "1":
            k2 = i
            break
    k = k2 - k1
    for i in range(k):
        bin2 = bin2[:k2 - i - 1] + bin2[k2 - i:32] + "0"
    res_reg = ""
    minus_bin2 = ""
    for c in bin2:
        if c == "0":
            minus_bin2 = minus_bin2 + "1"
        else:
            minus_bin2 = minus_bin2 + "0"
    minus_bin2 = sum(minus_bin2, to_additional(1))

    sub_res = sum(to_additional(num1), minus_bin2)

    if sub_res[0] == "1":
        res_reg = res_reg + "0"
    else:
        res_reg = res_reg + "1"

    for i in range(k):
        sub_res = sub_res[0] + sub_res[2:32] + "0"
        if sub_res[0] == "1":
            sub_res = sum(sub_res, bin2)
        else:
            sub_res = sum(sub_res, minus_bin2)
        if sub_res[0] == "1":
            res_reg = res_reg + "0"
        else:
            res_reg = res_reg + "1"
    if sub_res[0] == "1":
        sub_res = sum(sub_res, bin2)
    for i in range(k):
        sub_res = sub_res[0] + "0" + sub_res[1: k2 + i + 2]
    while len(res_reg) != 32:
        res_reg = "0" + res_reg
    if sign:
        res_reg = "1" + res_reg[1:]
    return res_reg


def mul(num1, num2):
    sign = False
    if (num1 < 0 < num2) or (num1 > 0 > num2):
        sign = True
    add1 = to_additional(abs(num1))
    add2 = to_additional(abs(num2))
    res = ""
    temp_results = []
    for i in range(31, -1, -1):
        if add2[i] == "1":
            temp_results.append([add1, 31 - i])
    maxi = temp_results[len(temp_results) - 1][1]
    for t_res in temp_results:
        t_res[0] = "0" * (maxi - t_res[1]) + t_res[0] + "0" * (t_res[1])
    res = temp_results[0][0]
    for i in range(1, len(temp_results)):
        temp_res = temp_results[i][0]
        res = sum(res, temp_res)
    res = res[len(res) - 32:]
    if sign:
        res = "1" + res[1:]
    return res


def sum(add1, add2):
    res = ""
    temp = False
    for i in range(len(add1) - 1, -1, -1):
        match (add1[i], add2[i], temp):
            case ("1", "1", False):
                res = res + "0"
                temp = True
            case ("1", "1", True):
                res = res + "1"
            case ("0", "1", True):
                res = res + "0"
                temp = True
            case ("1", "0", True):
                res = res + "0"
                temp = True
            case ("0", "0", True):
                res = res + "1"
                temp = False
            case ("0", "0", False):
                res = res + "0"
            case (_):
                res = res + "1"
    return res[::-1]


def main():
    print("Enter the first num for operations: ")
    num1 = input()
    while re.match(r'^[-0-9]*$', num1) is None :
        print("Error. Try again")
        num1 = input()
    print("Enter the second num for operations: ")
    num2 = input()
    while re.match(r'^[-0-9]*$', num2) is None :
        print("Error. Try again")
        num2 = input()
    num1 = int(num1)
    num2 = int(num2)
    res1 = add(num1, num2)
    print(f"Res of add {num1} and {num2}:\n in Bin_code: {res1}\n in Dec_code: {to_dec(res1)}")
    res2 = sub(num1, num2)
    print(f"Res of sub {num1} and {num2}:\n in Bin_code: {res2}\n in Dec_code: {to_dec(res2)}")
    res3 = mul(num1, num2)
    print(f"Res of mul {num1} and {num2}:\n in Bin_code: {res3}\n in Dec_code: {to_dec(res3)}")
    res4 = div(num1, num2)
    print(f"Res of div {num1} and {num2}:\n in Bin_code: {res4}\n in Dec_code: {to_dec(res4)}")


if __name__ == "__main__":
    main()
