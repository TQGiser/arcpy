#coding=utf-8
import arcpy
import os
import pandas as pd
import F

df = pd.read_excel(r'E:\资料\河流信息表.xlsx'.decode('utf-8'))
def findPCDC(riverName,df):
    for name, value in df.iterrows():
        if riverName.decode('utf-8') in df.loc[name, '河流名称'.decode('utf-8')]:
            return df.loc[name, '普查代码'.decode('utf-8')]
# findPCDC("阿加弄洼",df)


dmal = r'E:\2023年项目\0506二院数据\理塘县MDB\dmal_MDB.shp'

with arcpy.da.UpdateCursor(dmal,['RIVER','SXPCDC']) as yb:
    for row in yb:
        row[1] = findPCDC("%s"%row[0].encode('utf-8'),df)
        if(row[1] == None):
            pass
        else:
            yb.updateRow(row)
