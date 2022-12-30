# coding=utf-8
import arcpy
import os
import math
import pandas as pd
path = r'D:\2021年项目\0924预检数据\湖泊\mdb'
arcpy.env.workspace = path
def listFiles_Mdb(path,keyword,type):
    shps = []
    if type == 'd':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Point')
    elif type == 'x':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Polyline')
    elif type == 'm':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Polygon')
    for path, name, file in walk:
        for a in file:
            if keyword in a:
                shp = os.path.join(path, a)
                shps.append(shp)
    return shps
df = pd.read_excel(r'C:\Users\Administrator\Desktop\Test.xlsx'.decode('utf-8'),sheetname='行政代码'.decode('utf-8'))
dmList = []
for name,value in df.iterrows():
    dm = [df.loc[name,'name'],df.loc[name,'dm']]
    dmList.append(dm)
shps = listFiles_Mdb(path,'','x')
for shp in shps:
    shpName = shp.split('\\')[-1]
    if '县'.decode('utf-8') in shpName:
        xqName = shpName.split('县'.decode('utf-8'))[0]
        lakeName =  shpName.split('县'.decode('utf-8'))[1]
        newShpName = lakeName + xqName + '县段'.decode('utf-8')
    elif '市'.decode('utf-8') in shpName:
        xqName = shpName.split('市'.decode('utf-8'))[0]
        lakeName = shpName.split('市'.decode('utf-8'))[1]
        newShpName = lakeName + xqName + '市段'.decode('utf-8')
    if '月亮湖'.decode('utf-8') in lakeName:
        arcpy.CreateFolder_management(path,lakeName + '(' + xqName + ')')
        newPath = path + '\\' + lakeName.encode('utf-8') + '(' + xqName.encode('utf-8') +')'
    elif  '五色海'.decode('utf-8') in lakeName:
        arcpy.CreateFolder_management(path,lakeName + '(' + xqName + ')')
        newPath = path + '\\' + lakeName.encode('utf-8') + '(' + xqName.encode('utf-8') + ')'
    else:
        arcpy.CreateFolder_management(path,lakeName)
        newPath = path + '\\' + lakeName.encode('utf-8')
    arcpy.env.workspace = newPath
    arcpy.CopyFeatures_management(shp,newShpName)
    print newPath,newShpName
