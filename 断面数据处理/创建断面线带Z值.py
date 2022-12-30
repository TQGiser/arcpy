# coding=utf-8
import arcpy
import pandas as pd
import math
path = r'D:\2021年项目\0812创建三维断面线'
def listFile(path,type):
    arcpy.env.workspace = path
    if type == 'd':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Point')
    elif type == 'x':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Polyline')
    elif type == 'm':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Polygon')
    for path,name,file in walk:
        shp = file[0]
    return shp
d = listFile(path,'d')
cnLst = []
arcpy.env.overwriteOutput = True
with arcpy.da.SearchCursor(d,['SHAPE@X','SHAPE@Y','高程','点号','dmh']) as yb:
    for p in yb:
        cn = [p[0],p[1],p[2],p[3],p[4]]
        cnLst.append(cn)
dmh1Lst = [a[4] for a in cnLst]
dmhLst = list(set(dmh1Lst))
i = 0
lp = []
for i in range(0,len(dmhLst)):
    pg = []
    groupLst = []
    for cn in cnLst:
        if cn[4] == dmhLst[i]:
            groupLst.append(cn)
    for p in groupLst:
        xp = [p[0],p[1]]
        pg.append(xp)
    i+=1
    lp.append(arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in pg])))
arcpy.env.outputZFlag = 'Enabled'
Line = arcpy.CopyFeatures_management(lp,r"D:\2021年项 目\0812创建三维断面线\1.shp")
i = 0
with arcpy.da.UpdateCursor(Line,['SHAPE@','SHAPE@X','SHAPE@Z'],explode_to_points = True) as yb:
    for row in yb:
        for cn in cnLst:
            if round(row[1],2) ==round(cn[0],2):
                row[2] = cn[2]
                print i
                i += 1
        yb.updateRow(row)
