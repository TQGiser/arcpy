# coding=utf-8
import arcpy
import F
arcpy.env.overwriteOutput = True
path = r'E:\数据\1229'
outPath = r'E:\数据\1229'
dmaas = F.listFiles(path,'','m')
pList = []
Dmaa_all = arcpy.CreateFeatureclass_management(outPath,'石渠县河流管理范围面1730.shp', 'POLYGON')
arcpy.DefineProjection_management(Dmaa_all, coor_system='4542')
arcpy.AddField_management(Dmaa_all, '名称', 'TEXT')
arcpy.AddField_management(Dmaa_all, '省', 'TEXT')
arcpy.AddField_management(Dmaa_all, '市（州）', 'TEXT')
arcpy.AddField_management(Dmaa_all, '区（县）', 'TEXT')
arcpy.AddField_management(Dmaa_all, '乡镇', 'TEXT')
cs = arcpy.da.InsertCursor(Dmaa_all, ['SHAPE@', '名称', '省', '市（州）', '区（县）', '乡镇'])
for cn in pList:
    cs.insertRow(cn)