# coding=utf-8
import pandas as pd
import matplotlib
import math
import os
from openpyxl import load_workbook
from openpyxl.styles import Border,Side,colors,Alignment
A = '执曲横断面测量成果表'.decode('utf-8')
path = r'C:\Users\Administrator\Desktop\热曲河道断面成果'.decode('utf-8')
outpath = r'C:\Users\Administrator\Desktop\a'.decode('utf-8')
os.chdir(path)
lst = []
for i,v,m in os.walk(path):
    lst=m
def get_dt(lst):
    for i in lst:
        df = pd.read_excel(i,header=1)
        yield df
print '正在合并所有断面数据'
df = pd.concat(get_dt(lst))
allexcel = outpath + '\\' + 'all2.xlsx'
df.to_excel(allexcel,index = False)

