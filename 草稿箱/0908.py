# coding=utf-8
import arcpy
import F
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r'E:\workData\20230908XXD\测试\84'
path = r'E:\workData\20230908XXD\测试\84\HBS'
repath = r'E:\workData\20230908XXD\测试\84\rst2'

tp2 = r'E:\workData\20230908XXD\测试\84\植被类型84.shp'

hbs = F.listFiles(path,'','m')
i=0
for hb in hbs:

    ofp = repath + '\\' + '植被类型{:02}.shp'.format(i)
    print ofp
    arcpy.Clip_analysis(tp2,hb,ofp,cluster_tolerance="")
    i+=1










# for boua in bouas:
#     print boua
#     with arcpy.da.SearchCursor(boua,'SHAPE@') as yb2:
#         for row2 in yb2:
#             cs.insertRow(row2)
# Shp = arcpy.Dissolve_management(aL,path + '\\' + 'DMAA.shp')
# arcpy.Delete_management(aL)