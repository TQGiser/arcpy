#coding=utf-8
import arcpy
import os
import math
import pandas as pd
import F
arcpy.env.overwriteOutput = True
path = r'E:\2021年项目\1213理塘桩牌表'
tks = F.listFiles(path,'','m')
i = 0
for tk in tks:
    if '图名'.decode('utf-8') in [field.name for field in arcpy.ListFields(tk)]:
        with arcpy.da.SearchCursor(tk,'图名') as yb:
            for row in yb:
                tkName = row[0]
    elif 'RefName'.decode('utf-8') in [field.name for field in arcpy.ListFields(tk)]:
        with arcpy.da.SearchCursor(tk,'Refname') as yb:
            for row in yb:
                tkName = row[0]
    elif 'name'.decode('utf-8') in [field.name for field in arcpy.ListFields(tk)]:
        with arcpy.da.SearchCursor(tk, 'name') as yb:
            for row in yb:
                tkName = row[0]
    sp = arcpy.Describe(tk).spatialReference
    cm2 = (arcpy.Describe(tk).extent.XMax + arcpy.Describe(tk).extent.XMin) / 2
    Shp99 = path + '\\' + 'okTk' + '\\' +  '99' + '\\' + '{}.shp'.format(i)
    Shp102 = path + '\\' + 'okTk' + '\\' +  '102' + '\\' + '{}.shp'.format(i)
    if sp.name == 'Unknown':
        if cm2 < 400000.0:
            arcpy.DefineProjection_management(tk,arcpy.SpatialReference(4543))
            arcpy.CopyFeatures_management(tk,Shp102)
        else:
            arcpy.DefineProjection_management(tk, arcpy.SpatialReference(4542))
            arcpy.CopyFeatures_management(tk, Shp99)
    elif 'GCS_China_Geodetic_Coordinate_System_2000' in sp.name:
        if cm2 > 97.5 and cm2 < 100.5:
            arcpy.Project_management(tk,Shp99,arcpy.SpatialReference(4542))
        elif cm2 > 100.5 and cm2 < 103.5:
            arcpy.Project_management(tk, Shp102, arcpy.SpatialReference(4543))
    else:
        if cm2 < 400000.0:
            arcpy.CopyFeatures_management(tk, Shp102)
            print 102
        else:
            print 99
            arcpy.CopyFeatures_management(tk, Shp99)
    i += 1
    print tk,cm2,sp.name
