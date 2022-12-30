#coding=utf-8
import arcpy
import pandas as pd
import math
arcpy.env.overwriteOutput = True
p_cn = []
file = r'D:\Test\1.dat'.decode('utf-8')
# df = pd.read_table(file, names=['name','X', 'Y', 'ELEV'], header=-1, sep=',',encoding = 'gb18030')
df = pd.read_table(file, names=['name','X', 'Y', 'ELEV'], header=-1, sep=',') # 不用解码
for index, value in df.iterrows():
    cn = [value['X'], value['Y'],value['ELEV'],value['name']]
    p_cn.append(cn)
point = arcpy.Point()
pointList = []
for p in p_cn:
    point.X = p[0]
    point.Y = p[1]
    point.Z = p[2]
    arcpy.env.outputZFlag = 'Enabled'
    pg = arcpy.PointGeometry(point)
    pointList.append(pg)
arcpy.env.outputZFlag = 'Enabled'
p = arcpy.CopyFeatures_management(pointList, r'D:\Test\hb.shp')
arcpy.AddField_management(p,'name','TEXT')
with arcpy.da.UpdateCursor(p,['SHAPE@X','name']) as yb:
    for row in yb:
        for cn in p_cn:
            if round(row[0],1) ==round(cn[0],1):
                row[1] = cn[3]
        yb.updateRow(row)

