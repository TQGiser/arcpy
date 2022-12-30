# coding=utf-8
import arcpy
import F
path = r'E:\2022年项目\0512巴塘断面\全部断面线'
shps = F.listFiles(path,'','x')
for shp in shps:
    arcpy.DefineProjection_management(shp,coor_system='4542')