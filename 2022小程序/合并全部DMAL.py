# coding=utf-8
import arcpy
import F
arcpy.env.overwriteOutput = True
path = r'E:\2022年项目\1116小程序\ok\WKID4326'
outPath = r'E:\2022年项目\1116小程序\ok'
dmals = F.listFiles(path,'','x')
pList = []
for dmal in dmals:
    with arcpy.da.SearchCursor(dmal, ['SHAPE@','名称','省','市（州）','区（县）','乡镇','岸别']) as yb:
        for row in yb:
            cn = [row[0],row[1],row[2],row[3],row[4],row[5],row[6]]
            pList.append(cn)
Dmal_all = arcpy.CreateFeatureclass_management(outPath,'雅江县河流管理范围线.shp', 'POLYLINE')
arcpy.DefineProjection_management(Dmal_all, coor_system='4326')
arcpy.AddField_management(Dmal_all, '名称', 'TEXT')
arcpy.AddField_management(Dmal_all, '省', 'TEXT')
arcpy.AddField_management(Dmal_all, '市（州）', 'TEXT')
arcpy.AddField_management(Dmal_all, '区（县）', 'TEXT')
arcpy.AddField_management(Dmal_all, '乡镇', 'TEXT')
arcpy.AddField_management(Dmal_all, '岸别', 'TEXT')
cs = arcpy.da.InsertCursor(Dmal_all, ['SHAPE@', '名称', '省', '市（州）', '区（县）', '乡镇','岸别'])
for cn in pList:
    cs.insertRow(cn)