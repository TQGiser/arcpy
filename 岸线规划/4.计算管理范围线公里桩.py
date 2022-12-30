#coding=utf-8
import arcpy
import os
import pandas as pd
import F
arcpy.env.overwriteOutput = True
path = r'E:\2021年项目\1222岸线规划\定曲'
dmal = F.listFile(path,'管理范围线'.decode('utf-8'),'x')
riverName = arcpy.Describe(dmal).baseName.replace('管理范围线'.decode('utf-8'),'')
zx = F.listFile(path,'校正后中线'.decode('utf-8'),'x')
spatial_ref = arcpy.Describe(dmal).spatialReference
KpList = []
arcpy.env.overwriteOutput=True
FidList = []
with arcpy.da.SearchCursor(dmal,'SHAPE@') as yb:
    for row in yb:
        with arcpy.da.SearchCursor(zx, 'SHAPE@') as yb2:
            for row2 in yb2:
                a = row2[0].measureOnLine(row[0].firstPoint)
                b = row2[0].measureOnLine(row[0].lastPoint)
                ab = row2[0].queryPointAndDistance(row[0].firstPoint)
                if ab[3] is True:
                    lenth = row[0].length
                    i = 0
                    while i < lenth:
                        name = 'K' + str(i / 1000)
                        Kp = row[0].positionAlongLine(i)
                        cn = [name, Kp]
                        KpList.append(cn)
                        print 'K' + str(i / 1000), row[0].positionAlongLine(i).centroid.X, row[0].positionAlongLine(
                            i).centroid.Y
                        i += 1000
                else:
                    lenth = row[0].length
                    i = 0
                    while i < lenth:
                        name = 'K' + str(i / 1000)
                        Kp = row[0].positionAlongLine(i)
                        cn = [name, Kp]
                        KpList.append(cn)
                        print 'K' + str(i / 1000), row[0].positionAlongLine(i).centroid.X, row[0].positionAlongLine(
                            i).centroid.Y
                        i += 1000
p = arcpy.CreateFeatureclass_management(path,'{}公里桩'.format(riverName.encode('utf-8')),'POINT',spatial_reference= spatial_ref)
arcpy.AddField_management(p,'name','TEXT')
yb = arcpy.da.InsertCursor(p,['name','SHAPE@'])
for cn in KpList:
    yb.insertRow(cn)
del yb
