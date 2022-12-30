# coding=utf-8
import arcpy
import pandas as pd
import math
import F
arcpy.env.overwriteOutput =True
path = r'E:\测试文件夹\test'
glq = F.listFile(path,'功能区'.decode('utf-8'),'m')
tk = F.listFile(path,'图框'.decode('utf-8'),'m')
tempShps = []
with arcpy.da.SearchCursor(tk,'SHAPE@') as yb:
    for row in yb:
        with arcpy.da.SearchCursor(glq, 'SHAPE@') as yb2:
            for row2 in yb2:
                if row[0].overlaps(row2[0]):
                    shp = row2[0].clip(row[0].extent)
                elif row[0].contains(row2[0]):
                    shp = row2[0].clip(row[0].extent)
        tempShps.append(shp)
# arcpy.CopyFeatures_management(tempShps,path + '\\' + 'all.shp')
Aera = arcpy.CreateFeatureclass_management(path,'all.shp','POLYGON')
cs = arcpy.da.InsertCursor(Aera,['SHAPE@'])
for shp in tempShps:
    cs.insertRow([shp])