#coding=utf-8
import arcpy
import os
import F

path = r'E:\数据整合\DOM\TIF\河湖划界\措普上湖'
arcpy.env.workspace = path
arcpy.env.overwriteOutput=True
outPath = r'E:\测试文件夹\test'
tifs = F.listTifs(path)
for tif in tifs:
    tifName = arcpy.Describe(tif).name
    arcpy.CopyRaster_management(tif,outPath + '\\' + tifName.encode('utf-8'),nodata_value="0")
    print tifName

# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "闷措湖巴塘县段-001.tif"

# tifs = F.listFiles(path,)