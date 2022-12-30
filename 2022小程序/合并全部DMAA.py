# coding=utf-8
import arcpy
import F
arcpy.env.overwriteOutput = True
path = r'E:\2022年项目\1116小程序\ok\WKID4326'
outPath = r'E:\2022年项目\1116小程序\ok'
dmaas = F.listFiles(path,'','m')
pList = []
for dmaa in dmaas:
    with arcpy.da.SearchCursor(dmaa, ['SHAPE@','名称','省','市（州）','区（县）','乡镇']) as yb:
        for row in yb:
            cn = [row[0],row[1],row[2],row[3],row[4],row[5]]
            pList.append(cn)
Dmaa_all = arcpy.CreateFeatureclass_management(outPath,'雅江县河流管理范围面.shp', 'POLYGON')
arcpy.DefineProjection_management(Dmaa_all, coor_system='4326')
arcpy.AddField_management(Dmaa_all, '名称', 'TEXT')
arcpy.AddField_management(Dmaa_all, '省', 'TEXT')
arcpy.AddField_management(Dmaa_all, '市（州）', 'TEXT')
arcpy.AddField_management(Dmaa_all, '区（县）', 'TEXT')
arcpy.AddField_management(Dmaa_all, '乡镇', 'TEXT')
cs = arcpy.da.InsertCursor(Dmaa_all, ['SHAPE@', '名称', '省', '市（州）', '区（县）', '乡镇'])
for cn in pList:
    cs.insertRow(cn)