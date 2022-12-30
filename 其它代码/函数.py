# coding=utf-8
"""def cal(x1,x2):
    print(f'first is {x1} and second is {x2}')
cal("adfdas",'ewqr')
lst1 = [1,3,5,2,5,2,6]
def sum_func_js(x):
    lst2 = []
    n = 1
    for i in x:
        if n % 2 == 1:
            lst2.append(i)
        n += 1
    print(lst2)
sum_func_js(lst1)"""
s = 'adf 12 adkl adsf'
num = 0
space = 0
strs = 0
for i in s:
    if i.isdigit():
        num += 1
    elif i.isalpha():
        strs += 1
    elif i.isspace():
        space += 1
dict1 =[num, space, strs]
print('数字有{0}个，空格有{1}个，字母有{2}个'.format(dict1[0],dict1[1],dict1[2]))
type(dict1)