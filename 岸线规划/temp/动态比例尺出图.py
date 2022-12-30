#coding=utf-8
import arcpy
import pandas as pd
import math
path = r'E:\2021年项目\1020岸线图册\湖泊'
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True
mxd = arcpy.mapping.MapDocument(r'E:\2021年项目\1020岸线图册\湖泊\湖泊.mxd'.decode('utf-8'))
tk = path + '\\' + '湖泊图框.shp'
zbz = arcpy.mapping.ListLayoutElements(mxd,'Mapsurround_Element','')[0]
blc = arcpy.mapping.ListLayoutElements(mxd,'Text_Element','比例尺')[0]
TopRightX =  27.8336
TopRightY =  24.683
TopLeftX = 0.8613
TopLeftY = 24.683
for pagenum in range(1,mxd.dataDrivenPages.pageCount + 1):
    mxd.dataDrivenPages.currentPageID = pagenum              #驱动页面从1开始
    cursor = arcpy.SearchCursor(tk)
    for i in cursor:
        if i.FID == pagenum - 1:
            print i.FID
            blcNum = str(i.Blc)
            riverName = i.Name.split('0')[0]
            fileName = riverName + '%03d'%pagenum
            if i.Zbz == 0:
                x = TopLeftX
                y = TopLeftY
            else:
                x = TopRightX
                y = TopRightY
            print fileName,i.Zbz
            zbz.elementPositionX = x
            zbz.elementPositionY = y
            blc.text = '比例尺1：{}'.format(blcNum)
            mxd.save
            arcpy.mapping.ExportToJPEG(mxd,path.decode('utf-8') + '\\' + 'pdf' + '\\' + fileName +  ".jpg",resolution = 400)





