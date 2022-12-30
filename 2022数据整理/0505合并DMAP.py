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
    shp = mdbPath.encode('utf-8') + '\\' + 'DMAP-84.shp'
    with arcpy.da.SearchCursor(shp,['SHAPE@','XMMC'],explode_to_points=True) as yb:
        for row in yb:
            cn = [row[0],row[1]]
            print row[0],row[1]
            shpList.append(cn)
all = arcpy.CreateFeatureclass_management(path,'DMAP','POINT')
arcpy.AddField_management(all, 'XMMC', 'TEXT')
cs = arcpy.da.InsertCursor(all,['SHAPE@','XMMC'])
for m in shpList:
    print m
    cs.insertRow(m)