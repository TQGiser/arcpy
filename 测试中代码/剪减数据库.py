#coding=utf-8
import arcpy
import os
mdbpath = r'D:\2021年项目\0416MDB裁剪\热曲1W - 3.mdb'.decode('utf-8')
arcpy.env.workspace = mdbpath
mdb = arcpy.ListDatasets()[0]
file = arcpy.ListFeatureClasses(feature_dataset=mdb)
shppath = r'D:\2021年项目\0416MDB裁剪'.decode('utf-8')
arcpy.env.workspace = shppath
tk = arcpy.ListFeatureClasses()[0]
with arcpy.da.SearchCursor(tk, 'name') as yb:
    for row in yb:
        arcpy.CreatePersonalGDB_management(shppath, row[0])
for ys in file:
    allFeature = mdbpath + '\\' + ys
    print(allFeature)
    with arcpy.da.SearchCursor(tk, ['name','SHAPE@']) as yb:
        for row in yb:
            clipShp = shppath + '\\' + row[0] + '.mdb' + '\\' + ys
            print(clipShp)
            arcpy.Clip_analysis(allFeature,row[1], clipShp)
            # arcpy.FeatureClassToFeatureClass_conversion(allFeature, ffMdb, ys)


#         arcpy.Clip_analysis()
#         arcpy.FeatureClassToFeatureClass_conversion()
# for name in file:
#     print(file)