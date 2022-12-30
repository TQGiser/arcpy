
#coding=utf-8
import arcpy
import os
import pandas as pd
import F
arcpy.env.overwriteOutput = True
path = r'E:\测试文件夹\test\河流'
ms = F.listFiles(path,'','m')
mList = []
for m in ms:
    print arcpy.Describe(m).spatialReference.name
    riverName = (arcpy.Describe(m).path).encode('utf-8').split('河流\\')[1].replace('\\数据', '')
    pShp = path + '\\' + 'temp' + '\\' + '{}.shp'.format(riverName)
    if '99' in arcpy.Describe(m).spatialReference.name or '102' in arcpy.Describe(m).spatialReference.name:
        newM = arcpy.Project_management(m,pShp,out_coor_system="GEOGCS['GCS_China_Geodetic_Coordinate_System_2000',DATUM['D_China_2000',"
                                                               "SPHEROID['CGCS2000',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],"
                                                               "UNIT['Degree',0.0174532925199433]]")
        fields = [fiedl.baseName for fiedl in arcpy.ListFields(newM)]
        # riverName2 = arcpy.Describe(newM).name
        if '名称'.decode('utf-8') in fields:
            with arcpy.da.SearchCursor(newM,['SHAPE@','名称'.decode('utf-8')]) as yb:
                for row in yb:
                    cn =[row[0],riverName,row[1]]
                    mList.append(cn)
        else:
            with arcpy.da.SearchCursor(newM,'SHAPE@') as yb:
                for row in yb:
                    cn =[row[0],riverName,'']
                    mList.append(cn)
    fields = [fiedl.baseName for fiedl in arcpy.ListFields(m)]
    if 'GCS_China_Geodetic_Coordinate_System' in arcpy.Describe(m).spatialReference.name:
        if '名称'.decode('utf-8') in fields:
            with arcpy.da.SearchCursor(m, ['SHAPE@', '名称'.decode('utf-8')]) as yb:
                for row in yb:
                    cn = [row[0], riverName, row[1]]
                    mList.append(cn)
        else:
            with arcpy.da.SearchCursor(m, 'SHAPE@') as yb:
                for row in yb:
                    cn = [row[0], riverName, '']
                    mList.append(cn)

all = arcpy.CreateFeatureclass_management(path,'All.shp','POLYGON')
arcpy.AddField_management(all,'河流','TEXT')
arcpy.AddField_management(all,'名称','TEXT')
cs = arcpy.da.InsertCursor(all,['SHAPE@','河流','名称'])
for m in mList:
    cs.insertRow(m)