#coding=utf-8
import arcpy
import F
import os
from os.path import join,getsize
path = r'E:\数据整合\DLG\MDB\河湖划界'.decode('utf-8')
arcpy.env.workspace = path
mdbPathList = []
for i,v,m in os.walk(path):
    for f in m :
        mdb = os.path.join(i,f)
        mdbPath = '\\'.join(mdb.split('\\',7)[0:7])
        if mdbPath not in mdbPathList:
            mdbPathList.append(mdbPath)
shpList = []
for mdbPath in mdbPathList:
    shp = mdbPath.encode('utf-8') + '\\' + 'BOUA-84.shp'
    print shp
    with arcpy.da.SearchCursor(shp,['SHAPE@','GS','XMLX','XMMC','CS','SJRL','SX','ZBX']) as yb:
        for row in yb:
            cn = [row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]]
            shpList.append(cn)
all = arcpy.CreateFeatureclass_management(path,'DMAL','POLYLINE')
arcpy.AddField_management(all, 'GS', 'TEXT')
arcpy.AddField_management(all, 'XMLX', 'TEXT')
arcpy.AddField_management(all, 'XMMC', 'TEXT')
arcpy.AddField_management(all, 'CS', 'TEXT')
arcpy.AddField_management(all, 'SJRL', 'TEXT')
arcpy.AddField_management(all, 'SX', 'TEXT')
arcpy.AddField_management(all, 'ZBX', 'TEXT')
cs = arcpy.da.InsertCursor(all,['SHAPE@','GS','XMLX','XMMC','CS','SJRL','SX','ZBX'])
for m in shpList:
    cs.insertRow(m)