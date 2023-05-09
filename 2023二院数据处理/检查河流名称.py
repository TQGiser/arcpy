#coding=utf-8
import arcpy
import os
import pandas as pd
import F

df = pd.read_excel(r'C:\Users\Administrator\Desktop\新建文件夹\雅江县18条河.xlsx'.decode('utf-8'))

excelList = []
for name, value in df.iterrows():
    excelList.append(df.loc[name, 'name'.decode('utf-8')])

shapeList = []
dmal = r'E:\2023年项目\0506二院数据\OK\雅江县\雅江县管理范围线.shp'
with arcpy.da.UpdateCursor(dmal, 'RIVER') as yb:
    for row in yb:
        shapeList.append(row[0])

for name in excelList:
    if name not in shapeList:
        print name