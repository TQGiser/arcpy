# coding=utf-8
import arcpy
import os
import F
import pandas as pd
path = r'E:\2021年项目\1216生断面'.decode('utf-8')
os.chdir(path)
cnList = []
for i,v,m in os.walk(path):
    for s in m:
        df = pd.read_csv(s,encoding='GB18030')
        for name,value in df.iterrows():
            cn = [s.replace('.dat','') + df.iloc[name,1],df.iloc[name,2],df.iloc[name,3],df.iloc[name,4]]
            cnList.append(cn)
p = arcpy.CreateFeatureclass_management(path,'a','POINT')
arcpy.AddField_management(p,'NAME','TEXT')
arcpy.AddField_management(p,'ELEV','TEXT')
yb = arcpy.da.InsertCursor(p,['NAME','SHAPE@Y','SHAPE@X','ELEV'])
for cn in cnList:
    yb.insertRow(cn)
del yb
