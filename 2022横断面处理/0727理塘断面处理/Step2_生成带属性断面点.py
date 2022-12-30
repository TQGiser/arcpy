#coding=utf-8
import os
import pandas as pd
import arcpy
arcpy.env.overwriteOutput=True
path = r'E:\2022年项目\0815理塘断面表格\xls\99'
allXls = path + '\\' + 'all.xlsx'
df = pd.read_excel(allXls.decode('utf-8'))
cnList = []
for name,value in df.iterrows():
    cn = [df.loc[name,'x'],df.loc[name,'y'],df.loc[name,'elev'],df.loc[name,'dh'],df.loc[name,'dmh'],df.loc[name,'bz']]
    cnList.append(cn)
p = arcpy.CreateFeatureclass_management(path,'allPoint','POINT')
arcpy.AddField_management(p,'elev','TEXT')
arcpy.AddField_management(p,'dh','TEXT')
arcpy.AddField_management(p,'dmh','TEXT')
arcpy.AddField_management(p,'bz','TEXT')
yb = arcpy.da.InsertCursor(p,['SHAPE@X','SHAPE@Y','elev','dh','dmh','bz'])
for cn in cnList:
    print cn
    if not pd.isnull(cn[0]):
        yb.insertRow(cn)
del yb
