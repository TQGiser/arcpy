#coding=utf-8
import arcpy
import pandas as pd
import math
import F
path = r'E:\2021年项目\1222岸线规划\赤土河'
try:
    arcpy.CreateFolder_management(path,'pdf')
except:
    pass
dmal = F.listFile(path,'管理范围线'.decode('utf-8'),'x')
riverName = (arcpy.Describe(dmal).baseName).encode('utf-8').replace('管理范围线','')
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True
mxdpath = path + '\\' + '{}.mxd'.format(riverName)
print mxdpath
# mxd = arcpy.mapping.MapDocument(r'E:\2021年项目\1222岸线规划\金汤河\{}.mxd'.format(riverName,riverName).decode('utf-8'))
mxd = arcpy.mapping.MapDocument(mxdpath.decode('utf-8'))
tk = path + '\\' + '{}图框.shp'.format(riverName)
zbz = arcpy.mapping.ListLayoutElements(mxd,'Mapsurround_Element','')[0]
TopRightX =  27.8336
TopRightY =  24.683
TopLeftX = 0.8613
TopLeftY = 24.683
for pagenum in range(1,mxd.dataDrivenPages.pageCount + 1):
    mxd.dataDrivenPages.currentPageID = pagenum              #驱动页面从1开始
    cursor = arcpy.SearchCursor(tk)
    for i in cursor:
        if i.FID == pagenum - 1:
            riverName = i.Name.split('0')[0]
            fileName = riverName + '%03d'%pagenum
            if i.Zbz == 0:
                x = TopLeftX
                y = TopLeftY
            else:
                x = TopRightX
                y = TopRightY
            print i.Name,i.Zbz
            zbz.elementPositionX = x
            zbz.elementPositionY = y
            mxd.save
            arcpy.mapping.ExportToJPEG(mxd,path.decode('utf-8') + '\\' + 'pdf' + '\\' + i.Name +  ".jpg",resolution = 100)
