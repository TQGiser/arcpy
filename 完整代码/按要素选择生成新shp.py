#coding=utf-8
import arcpy
import os
path = r"D:\2021年项目\TEST\CpShp".decode('utf-8')
os.chdir(path)
arcpy.env.workspace = r"D:\2021年项目\TEST\CpShp".decode('utf-8')
ds = '管理线桩.shp'
out_path = r"D:\2021年项目\TEST\CpShp"
new_shp = '白龙柯.shp'
'''with arcpy.da.SearchCursor(ds,["NAME2","SHAPE@"],"NAME LIKE '白龙柯%'") as yb:        #每个要素都复制为shp
    for row in yb:
        name = row[0] + '.shp'
        name2 = name.encode('utf-8')
        arcpy.FeatureClassToFeatureClass_conversion(row[1],out_path,name2)
del yb'''
arcpy.Delete_management(new_shp)
arcpy.CreateFeatureclass_management(out_path,new_shp,'POINT',ds)
tt = arcpy.da.InsertCursor(new_shp,['NAME','SHAPE@'])
ys = arcpy.da.SearchCursor(ds,["NAME","SHAPE@"],"NAME LIKE '白龙柯%'")
for row in ys:
    tt.insertRow([row[0],row[1]])