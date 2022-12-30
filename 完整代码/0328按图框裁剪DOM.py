import arcpy
import os
import sys
from arcpy.sa import *

os.chdir(r'E:\2021年项目\0205-125个湖泊\0329')
arcpy.env.workspace = r'E:\2021年项目\0205-125个湖泊\0329'
shp = r'E:\2021年项目\0205-125个湖泊\TK.shp'
path = r'E:\2021年项目\0205-125个湖泊\0329'
lack_name = '扎杰龙瓦'
raster = arcpy.Raster(r'E:\2021年项目\0205-125个湖泊\1.tif')
with arcpy.da.SearchCursor(shp,["SHAPE@",'Name']) as yb:
    for row in yb:
        out_name = lack_name + row[1] + '.shp'
        print(row[1])
        arcpy.FeatureClassToFeatureClass_conversion(row[0],path,out_name)
        print(out_name)
filename = []
for i,v,m in os.walk(r'E:\2021年项目\0205-125个湖泊\0329'):
    for a in m:
        if a.endswith('.shp'):
            filename.append(a)
print(filename)
for name in filename:
    print(name)
    buffDis = 10
    mask = arcpy.GraphicBuffer_analysis(name,'{}_buffer_{}.tif'.format((name.strip('.shp')),(buffDis)),buffDis)
    rm =arcpy.sa.ExtractByMask(raster,mask)
    rm.save('{}.tif'.format(name.strip('.shp')))