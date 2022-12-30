#coding=utf-8
import arcpy
import os
path = "D:/2021年项目/0317雅江北桩确认".decode('utf-8')
mxdpath = "D:/2021年项目/0317雅江北桩确认/分河图.mxd".decode('utf-8')
os.chdir(path)
arcpy.env.workspace = path
mxd = arcpy.mapping.MapDocument(mxdpath)
shppath = '分河图框.shp'
outpath = './安装位置/'
for pagenum in range(1,mxd.dataDrivenPages.pageCount + 1):
    mxd.dataDrivenPages.currentPageID = pagenum
    cursor = arcpy.UpdateCursor(shppath)
    for i in cursor:
        if i.FID == pagenum-1:
            name = i.NAME2
            name2 = name.encode('utf-8')
    arcpy.mapping.ExportToJPEG(mxd,"D:/2021年项目/0329雅江北图册/安装位置/" + name2 + ".jpg",resolution = 800)