#coding=utf-8
import arcpy
import pandas as pd
import math
import os
import random
def listFiles_Mdb(path,type):
    shps = []
    if type == 'd':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Point')
    elif type == 'x':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Polyline')
    elif type == 'm':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Polygon')
    for path, name, file in walk:
        for a in file:
            if a == 'DMAP':
                shp = os.path.join(path, a)
                shps.append(shp)
            elif a == 'DMAL':
                shp = os.path.join(path, a)
                shps.append(shp)
            elif a == 'DMAA':
                shp = os.path.join(path, a)
                shps.append(shp)
    return shps
path = r'D:\2021年项目\0915改擦岗隆洼表格\擦岗隆洼'
df = pd.read_excel(r'D:\2021年项目\0915改擦岗隆洼表格\aaa.xlsx'.decode('utf-8'))
cnList = []
for name,value in df.iterrows():
    cn = [df.loc[name,'name'],df.loc[name,'x',],df.loc[name,'y'],df.loc[name,'h'],df.loc[name,'id'],df.loc[name,'gb']]
    cnList.append(cn)
shps = listFiles_Mdb(path,'d')
for shp in shps:
    with arcpy.da.UpdateCursor(shp,['NAME','SHAPE@X','SHAPE@Y','ELEV','RuleID','GB']) as yb:
        for row in yb:
            for cn in cnList:
                if row[0] == cn[0]:
                    row[1] = cn[1]
                    row[2] = cn[2]
                    row[3] = cn[3]
                    row[4] = cn[4]
                    row[5] = cn[5]
                    yb.updateRow(row)
                    print row[0]
