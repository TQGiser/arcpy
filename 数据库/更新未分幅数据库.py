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
path = r'D:\2021年项目\0913州河数据库\temp'
df = pd.read_excel(path.decode('utf-8') + '\\' + 'aaa.xlsx'.decode('utf-8'))
shp = listFiles_Mdb(path,'d')[0]
cnList = []
for name,value in df.iterrows():
    cn = [df.loc[name,'name'],'%0.2f'%df.loc[name,'ds']]
    cnList.append(cn)
with arcpy.da.UpdateCursor(shp,['NAME','REASON']) as yb:
    for row in yb:
        for cn in cnList:
            if row[0] == cn[0]:
                row[1] = '原安装位置地基不牢固，无法安装，所以向外平移{}米。'.format(cn[1])
                yb.updateRow(row)
                print row[0]


#coding=utf-8
import arcpy
import pandas as pd
import math
import os
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
path = r'D:\2021年项目\0917江北图册\改数据库'
shps = listFiles_Mdb(path,'d')
df = pd.read_excel(path.decode('utf-8') + '\\' + 'z.xlsx',sheetname='stz')
cnList = []
for name,value in df.iterrows():
    cn = [df.loc[name,'name'],df.loc[name,'h']]
    cnList.append(cn)
for shp in shps:
    with arcpy.da.SearchCursor(shp,['NAME','SHAPE@Y','SHAPE@X','ELEV','RuleID']) as yb:
        for row in yb:
            if row[4] == 2:
                print row[0],row[1],row[2],row[3]

for shp in shps:
    with arcpy.da.UpdateCursor(shp,['NAME','ELEV']) as yb:
        for row in yb:
            for cn in cnList:
                if  row[0] == cn[0]:
                    row[1] = cn[1]
                    yb.updateRow(row)

