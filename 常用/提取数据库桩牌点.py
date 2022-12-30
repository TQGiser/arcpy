# coding=utf-8
import arcpy
import os
import math
import pandas as pd
import F

path = r'E:\测试文件夹\test'
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True
mdbs = arcpy.ListFiles('*.mdb')
dmaps99 = []
dmaps102 = []
for mdb in mdbs:
    DLG = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG'
    dmap = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'DMAP'
    spatial_ref = arcpy.Describe(DLG).spatialReference
    if '99' in spatial_ref.name:
        with arcpy.da.SearchCursor(dmap, ['SHAPE@', 'NAME', 'ELEV', 'RuleID', 'NUM','COUNTY','TOWN']) as yb:
            for row in yb:
                if row[3] == 2 or row[3] == 3 or row[3] == 4:
                    cn = [row[0], row[1], row[2], row[3], row[4]]
                    print cn
                    dmaps99.append(cn)
    elif '102' in spatial_ref.name:
        with arcpy.da.SearchCursor(dmap, ['SHAPE@', 'NAME', 'ELEV', 'RuleID', 'NUM']) as yb:
            for row in yb:
                if row[3] == 2 or row[3] == 3 or row[3] == 4:
                    cn = [row[0], row[1], row[2], row[3], row[4]]
                    dmaps102.append(cn)
cs99 = arcpy.da.InsertCursor(r'E:\测试文件夹\test\P99.shp', ['SHAPE@', 'NAME', 'ELEV', 'RuleID', 'NUM'])
cs102 = arcpy.da.InsertCursor(r'E:\测试文件夹\test\P102.shp', ['SHAPE@', 'NAME', 'ELEV', 'RuleID', 'NUM'])
for dmap in dmaps99:
    print dmap
    cs99.insertRow(dmap)
for dmap in dmaps102:
    print dmap
    cs102.insertRow(dmap)

# p99 = arcpy.CreateFeatureclass_management(path,'P99.shp','POINT')
# cs99 = arcpy.da.InsertCursor(p99,'SHAPE@')
# for dmap in dmaps99:
#     print dmap
#     with arcpy.da.SearchCursor(dmap,'SHAPE@') as yb:
#         for row in yb:
#             cs99.insertRow(row)
# p102 = arcpy.CreateFeatureclass_management(path,'P102.shp','POINT')
# cs102 = arcpy.da.InsertCursor(p102,'SHAPE@')
# for dmap in dmaps102:
#     with arcpy.da.SearchCursor(dmap,'SHAPE@') as yb:
#         for row in yb:
#             cs102.insertRow(row)
# for mdb in mdbs:
#     DLG = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG'
#     dmap = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'DMAP'
#     spatial_ref = arcpy.Describe(DLG).spatialReference
#     if '99' in spatial_ref.name:
#         dmaps99.append(dmap)
#     elif '102' in spatial_ref.name:
#         dmaps102.append(dmap)
# p99 = arcpy.CreateFeatureclass_management(path,'P99.shp','POINT')
# cs99 = arcpy.da.InsertCursor(p99,'SHAPE@')
# for dmap in dmaps99:
#     print dmap
#     with arcpy.da.SearchCursor(dmap,'SHAPE@') as yb:
#         for row in yb:
#             cs99.insertRow(row)
# p102 = arcpy.CreateFeatureclass_management(path,'P102.shp','POINT')
# cs102 = arcpy.da.InsertCursor(p102,'SHAPE@')
# for dmap in dmaps102:
#     with arcpy.da.SearchCursor(dmap,'SHAPE@') as yb:
#         for row in yb:
#             cs102.insertRow(row)

# for tk in tks:
# if '图名'.decode('utf-8') in [field.name for field in arcpy.ListFields(tk)]:
#     with arcpy.da.SearchCursor(tk,'图名') as yb:
#         for row in yb:
#             tkName = row[0]
# elif 'RefName'.decode('utf-8') in [field.name for field in arcpy.ListFields(tk)]:
#     with arcpy.da.SearchCursor(tk,'Refname') as yb:
#         for row in yb:
#             tkName = row[0]
# elif 'name'.decode('utf-8') in [field.name for field in arcpy.ListFields(tk)]:
#     with arcpy.da.SearchCursor(tk, 'name') as yb:
#         for row in yb:
#             tkName = row[0]
# print tk,tkName.encode('utf-8').split('理塘县')[0]
# sp = arcpy.Describe(tk).spatialReference
# cm2 = (arcpy.Describe(tk).extent.XMax + arcpy.Describe(tk).extent.XMin) / 2
# Shp99 = path + '\\' + '99' + '\\' + '{}.shp'.format(i)
# Shp102 = path + '\\' + '102' + '\\' + '{}.shp'.format(i)
# if sp.name == 'Unknown':
#     if cm2 < 400000.0:
#         arcpy.DefineProjection_management(tk,arcpy.SpatialReference(4543))
#         arcpy.CopyFeatures_management(tk,Shp102)
#     else:
#         arcpy.DefineProjection_management(tk, arcpy.SpatialReference(4542))
#         arcpy.CopyFeatures_management(tk, Shp99)
# elif '2000' in sp.name:
#     if cm2 > 97.5 and cm2 < 100.5:
#         arcpy.Project_management(tk,Shp99,arcpy.SpatialReference(4542))
#     elif cm2 > 100.5 and cm2 < 103.5:
#         arcpy.Project_management(tk, Shp102, arcpy.SpatialReference(4543))
# else:
#     if cm2 < 400000.0:
#         arcpy.CopyFeatures_management(tk, Shp102)
#     else:
#         arcpy.CopyFeatures_management(tk, Shp99)
# i += 1
# print tk,cm2,sp.name
