#coding=utf-8
import arcpy
import os
path = "D:/2021年项目/TEST".decode('utf-8')
os.chdir(path)
arcpy.env.workspace = path
a = arcpy.ListRasters('','TIF')
yb = arcpy.da.SearchCursor('管理线桩.shp',"NAME","NAME LIKE '白龙柯%'")
for row in yb:
    name = row[0]
    print(name)

