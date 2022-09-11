from math import floor

from config import config


def getbinarys(text):
    arr = []
    for c in text:
        b = bin(ord(c))[2:]
        b = int(config.NO_OF_BITS-len(b))*"0" + b
        arr.append(b)
    return arr


def insertbit(num, bit):
    if bit == '1':
        if num % 2 == 0:
            num += 1
    elif bit == '0':
        if num % 2 == 1:
            num -= 1
    return num


def getstr(arr):
    s = ""
    for i in arr:
        s += chr(i)
    return s


def insert_num(num1, num2):
    max_num_of_bits = 8
    first_num_of_bits = 4
    bin1 = bin(num1)[2:]
    bin2 = bin(num2)[2:]
    bin1 = (max_num_of_bits - len(bin1))*"0"+bin1
    bin2 = (max_num_of_bits - len(bin2))*"0"+bin2
    bin1 = bin1[:4]+bin2[4:]
    return int("".join(bin1), 2)


def extract_num(num):
    b = bin(num)[2:]
    b = (8-len(b))*"0"+b
    ans = b[4:]+"0000"
    return int(ans, 2)


def getpercent(n1, n2):
    p = n1*100/n2
    return str(floor(p))
