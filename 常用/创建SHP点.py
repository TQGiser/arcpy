# coding=utf-8
import arcpy
import os
import math
import pandas as pd
# arcpy.env.workspace = r'D:\Test'
# arcpy.env.overwriteOutput = True
# def creatPoint(p_cn):
#     point = arcpy.Point()
#     pointList = []
#     for p in p_cn:
#         point.X = p[0]
#         point.Y = p[1]
#         pg = arcpy.PointGeometry(point)
#         pointList.append(pg)
#         arcpy.CopyFeatures_management(pointList, r'D:\Test\np.shp')
# df = pd.read_excel(r'D:\2021年项目\1008定曲2年水位\2年一遇水面线（汇总）0917.xlsx'.decode('utf-8'),sheetname='定曲'.decode('utf-8'))
# p_cn = []
# for name,value in df.iterrows():
#     x = df.loc[name,'x']
#     y = df.loc[name,'y']
#     p = [x,y]
#     p_cn.append(p)
# creatPoint(p_cn)
import arcpy
import pandas as pd
import math
import os
arcpy.env.overwriteOutput = True
path = r'C:\Users\Administrator\Desktop\新建文件夹'
arcpy.env.workspace = path
xlsx = path + '\\' + '1.xlsx'
df = pd.read_excel(xlsx.decode('utf-8'))
p_cn = []
for name,value in df.iterrows():
    cn = [df.loc[name,'x'],df.loc[name,'y'],df.loc[name,'name']]
    p_cn.append(cn)
p = arcpy.CreateFeatureclass_management(path,'转坐标3','POINT')
# arcpy.AddField_management(p,'dh','TEXT')
arcpy.AddField_management(p,'name','TEXT')# arcpy.AddField_management(p,'dmh','TEXT')
# arcpy.AddField_management(p,'GB','LONG')
# arcpy.AddField_management(p,'NUM','TEXT')
# arcpy.AddField_management(p,'ELEV','DOUBLE')
# arcpy.AddField_management(p,'RuleID','LONG')
# arcpy.AddField_management(p,'BANK','TEXT')
yb = arcpy.da.InsertCursor(p,['SHAPE@X','SHAPE@Y','name'])
for cn in p_cn:
    yb.insertRow(cn)
del yb