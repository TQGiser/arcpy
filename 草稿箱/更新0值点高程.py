# coding=utf-8
import arcpy
import os
import math
import pandas as pd
import F
import arcpy
path = 'E:\测试文件夹\Temp2'
arcpy.env.workspace =path
dmxs = F.listFiles(path,'','x')
allPoint = F.listFile(path,'全部'.decode('utf-8'),'d')
for dmx in dmxs:
    with arcpy.da.UpdateCursor(dmx,['SHAPE@X','SHAPE@Z','NAME'],explode_to_points=True) as yb:
        for row in yb:
            if row[1] == 0:
                a = row[2]
                expression = "dmh = '{}'".format(a)
                with arcpy.da.SearchCursor(allPoint,['SHAPE@X','elev','dmh'],where_clause=expression) as yb2:
                    for row2 in yb2:
                        if abs(row2[0] -row[0]) < 0.1:
                            row[1] = float(row2[1])
                            yb.updateRow(row)
                            print dmx,row[2],row[0]




