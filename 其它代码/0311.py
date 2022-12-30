# coding=utf-8
import os
lst = []
for i,v,m in os.walk('Z:\\'):
    lst.append(i)
print(lst)
