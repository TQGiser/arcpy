#coding=utf-8
import arcpy
import F
import os

path = r'E:\数据部数据\数据整合\DLG\MDB\河湖划界'
outpath = r'E:\test\all'

mdbPathList = []
for i,v,m in os.walk(path.decode('utf-8')):
    for f in m :
        mdb = os.path.join(i,f)
        mdbPath = '\\'.join(mdb.split('\\',8)[0:8])
        if mdbPath not in mdbPathList:
            mdbPathList.append(mdbPath)
polygonList = []
i=0
for mdbPath in mdbPathList:
    HYDA = mdbPath.encode('utf-8') + '\\' + 'HYDA-84.shp'
    print HYDA
    arcpy.Copy_management(HYDA,outpath + '\\' + '{}.shp'.format(i))
    i+=1
#     print HYDA
#     with arcpy.da.SearchCursor(HYDA,['SHAPE@','XMMC']) as yb:
#         for row in yb:
#             cn = [row[0],row[1]]
#             polygonList.append(cn)
#     del yb
#
# AllPolygon = arcpy.CreateFeatureclass_management(path, 'all.shp', 'POLYGON')
# arcpy.AddField_management(AllPolygon,'NAME','TEXT')
# cs = arcpy.da.InsertCursor(AllPolygon,['SHAPE@','NAME'])
# for polygon in polygonList:
#     print polygon[1]
#     cs.insertRow(polygon)
# del cs