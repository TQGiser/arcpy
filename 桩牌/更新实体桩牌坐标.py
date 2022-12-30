# coding=utf-8
import arcpy
import pandas as pd
import math
import os
path = r'D:\Test'
p1 = r'D:\Test\dmap.shp'
dmap = r'D:\Test\丁曲划界成果.mdb\DLG\DMAP'
with arcpy.da.UpdateCursor(dmap,['SHAPE@X','SHAPE@Y','NAME']) as yb:
    for dmap in yb:
        with arcpy.da.SearchCursor(p1,['SHAPE@X','SHAPE@Y','name']) as point:
            for p in point:
                if dmap[2] == p[2]:
                    dmap[0] = p[0]
                    dmap[1] = p[1]
        yb.updateRow(dmap)
