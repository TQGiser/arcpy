# coding=utf-8
import arcpy
import F
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r'E:\workData\20230908XXD\测试\84'
path = r'E:\workData\20230908XXD\测试\84\HBS'
repath = r'E:\workData\20230908XXD\测试\84\rst3'

tp2 = r'E:\workData\20230908XXD\测试\84\土壤类型84.shp'

hbs = F.listFiles(path,'','m')
i=0
for hb in hbs:
    ofp = repath + '\\' + '土壤类型{:02}.shp'.format(i)
    print ofp
    arcpy.Clip_analysis(tp2,hb,ofp,cluster_tolerance="")
    i+=1
