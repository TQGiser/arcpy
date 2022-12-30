#coding=utf-8
import arcpy
import os
import pandas as pd
import F
arcpy.env.overwriteOutput =True
path = r'E:\2021年项目\1222岸线规划\定曲'
dmal = F.listFile(path,'管理范围线'.decode('utf-8'),'x')
zx = F.listFile(path,'校正后中线'.decode('utf-8'),'x')
i = 0
with arcpy.da.UpdateCursor(dmal,'SHAPE@') as yb:
    for row in yb:
        with arcpy.da.SearchCursor(zx, 'SHAPE@') as yb2:
            for row2 in yb2:
                a = row2[0].measureOnLine(row[0].firstPoint)
                b = row2[0].measureOnLine(row[0].lastPoint)
                print a,b
                if a > b:
                    tempLine = arcpy.CopyFeatures_management(row[0],path + '\\' + 'tempLine{}'.format(i))
                    newtempLine = arcpy.FlipLine_edit(tempLine)
                    yb.deleteRow()
                    i+=1
tls = F.listFiles(path,'tempLine','x')
cs = arcpy.da.InsertCursor(dmal,['SHAPE@'])
polylinelist = []
for tl in tls:
    with arcpy.da.SearchCursor(tl,'SHAPE@') as yb:
        for row in yb:
            polylinelist.append(row[0])
for l in polylinelist:
    cs.insertRow([l])
for l in tls:
    arcpy.Delete_management(l)