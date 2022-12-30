# coding=utf-8
import random
b = random.randint(1,10)
i = 1
while i < 6:
    x = int(input('请输入整数'))
    if x > b:
        print("too big")
    elif x < b:
        print('too small')
    elif x == b:
        print('bingo')
    i += 1