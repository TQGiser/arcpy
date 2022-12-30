#coding=utf-8
import arcpy
import F
import os
path = r'E:\2022年项目\0512巴塘断面'.decode('utf-8')
arcpy.env.workspace = path
mdbPathList = []
for i,v,m in os.walk(path):
    for f in m :
        if f.endswith('.shp'):
            arcpy.Delete_management(os.path.join(i,f))
