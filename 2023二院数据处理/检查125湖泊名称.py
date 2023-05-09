#coding=utf-8
import arcpy
import os
import pandas as pd
import F

df = pd.read_excel(r'D:\2021年项目\0618湖泊入库\lakeData.xls'.decode('utf-8'))
# def findPCDC(riverName,df):
#     for name, value in df.iterrows():
#         if riverName.decode('utf-8') in df.loc[name, 'name'.decode('utf-8')]:
#             print riverName
# # findPCDC("阿加弄洼",df)
#
#
# dmal = r'E:\2023年项目\0506二院数据\OK\甘孜州州管\124个湖泊.shp'
#
# with arcpy.da.UpdateCursor(dmal,'RIVER') as yb:
#     for row in yb:

riverList125 = []
for name, value in df.iterrows():
    riverList125.append(df.loc[name, 'name'.decode('utf-8')])

riverList123 = []
dmal = r'E:\2023年项目\0506二院数据\OK\甘孜州州管\124个湖泊.shp'
with arcpy.da.UpdateCursor(dmal, 'RIVER') as yb:
    for row in yb:
        riverList123.append(row[0])

for name in riverList123:
    print name