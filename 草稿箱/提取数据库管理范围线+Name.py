#coding=utf-8
import arcpy
import os
import pandas as pd
arcpy.env.overwriteOutput = True
path = r'E:\2022年项目\0119交煤田\MDBS\125Lake'
arcpy.env.workspace = path
mdbs = arcpy.ListFiles('*.mdb')
dmaa99List = []
dmaa102List = []
for mdb in mdbs:
    print mdb
    riverName = arcpy.Describe(mdb).name.replace('.mdb', '')
    DLG = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG'
    spatial_ref = arcpy.Describe(DLG).spatialReference
    if '99' in spatial_ref.name:
        xzjx = r'D:\资料\甘孜乡镇\甘孜县界-99.shp'
        dmaa = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'DMAA'
        with arcpy.da.SearchCursor(dmaa, 'SHAPE@', "ruleid = 3") as yb:
            for row in yb:
                cn = [row[0], riverName]
                dmaa99List.append(cn)
    elif '102' in spatial_ref.name:
        xzjx = r'D:\资料\甘孜乡镇\甘孜县界-102.shp'
        dmaa = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'DMAA'
        with arcpy.da.SearchCursor(dmaa, 'SHAPE@', "ruleid = 3") as yb:
            for row in yb:
                cn = [row[0], riverName]
                dmaa102List.append(cn)


dmaa99All = arcpy.CreateFeatureclass_management(path,'All99.shp','POLYGON')
dmaa102All = arcpy.CreateFeatureclass_management(path,'All102.shp','POLYGON')
arcpy.AddField_management(dmaa99All,'NAME','TEXT')
cs = arcpy.da.InsertCursor(dmaa99All,['SHAPE@','NAME'])
for l in dmaa99List:
    print l[1]
    cs.insertRow(l)
arcpy.AddField_management(dmaa102All,'NAME','TEXT')
cs = arcpy.da.InsertCursor(dmaa102All,['SHAPE@','NAME'])
for l in dmaa102List:
    print l[1]
    cs.insertRow(l)


