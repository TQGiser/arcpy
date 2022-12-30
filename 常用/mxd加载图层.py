# coding=utf-8
import arcpy
import os
import math
import pandas as pd
path = r'E:\2021年项目\1025康定划界\冷子沟'
arcpy.env.workspace = path
mxd = arcpy.mapping.MapDocument(r'E:\2021年项目\1025康定划界\冷子沟\冷子沟.mxd'.decode('utf-8'))
df = arcpy.mapping.ListDataFrames(mxd)[0]
# walk = arcpy.da.Walk(path, topdown=True, datatype="RasterDataset", type='TIF')
# for path, name, file in walk:
#     for a in file:
#         tif = os.path.join(path, a)
#         print tif
#         ly = arcpy.mapping.Layer(tif)
#         arcpy.mapping.AddLayer(df,ly)
# mxd.save()
walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Polyline')
for path, name, file in walk:
    for a in file:
        shpList = ['HYDA','HYDL','RESA']
        for b in shpList:

            if a == b:
                shp = os.path.join(path, a)
                print shp
                ly = arcpy.mapping.Layer(shp)
                arcpy.mapping.AddLayer(df,ly)
mxd.save()