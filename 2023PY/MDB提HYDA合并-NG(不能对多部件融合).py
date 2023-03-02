#coding=utf-8
import arcpy
import os
arcpy.env.overwriteOutput = True
zbx = arcpy.SpatialReference(4326)
# path = r'E:\数据部数据\数据整合\DLG\MDB\河湖划界'
path = r'E:\test\数据整合\DLG\MDB\河湖划界'
arcpy.env.workspace = path
mdbPathList = []
allPolygonList = []
for i,v,m in os.walk(path.decode('utf-8')):
    for f in m :
        mdb = os.path.join(i,f)
        mdbPath = '\\'.join(mdb.split('\\',8)[0:8])
        if mdbPath not in mdbPathList:
            mdbPathList.append(mdbPath)
for mdbPath in mdbPathList:
    print mdbPath
    riverName = mdbPath.split('\\')[6].encode('utf-8')
    arcpy.env.workspace = mdbPath
    arcpy.env.overwriteOutput = True
    mdbs = arcpy.ListFiles('*.mdb')
    polygons = []

    for mdb in mdbs:
        polygon = mdbPath + '\\' + mdb + '\\' + 'DLG' + '\\' + 'HYDA'
        fileName = mdb.encode('utf-8').replace('.mdb','').replace('-','') + '.shp'
        projectFileName = 'pro' + fileName
        testCs = arcpy.da.SearchCursor(polygon,'SHAPE@')
        arcpy.FeatureClassToFeatureClass_conversion(polygon, mdbPath, fileName)
        arcpy.Project_management(mdbPath.encode('utf-8') + '\\' + fileName,mdbPath.encode('utf-8') + '\\' + projectFileName,zbx)
        tempPolygon = mdbPath.encode('utf-8') + '\\' + projectFileName
        polygons.append(tempPolygon)

    riverPolygon = arcpy.CreateFeatureclass_management(mdbPath, '{}.shp'.format(riverName), 'POLYGON')
    arcpy.AddField_management(riverPolygon, 'NAME', 'TEXT')
    cs = arcpy.da.InsertCursor(riverPolygon, 'SHAPE@')
    for polygon84 in polygons:
        with arcpy.da.SearchCursor(polygon84, 'SHAPE@') as yb2:
            for row2 in yb2:
                cs.insertRow(row2)
    Disshp = arcpy.Dissolve_management(riverPolygon,
                              multi_part="MULTI_PART",
                             )
    arcpy.Copy_management(Disshp,mdbPath.encode('utf-8') + '\\' + '{}_HB.shp'.format(riverName))
#     for polygon84 in polygons:
#         arcpy.Delete_management(polygon84)
#     # arcpy.Delete_management(mdbPath.encode('utf-8') + '\\' + 'a.shp')
#     # arcpy.Delete_management(riverPolygon)
#     okPolygon = mdbPath.encode('utf-8') + '\\' + '{}_HB.shp'.format(riverName)
#     arcpy.AddField_management(okPolygon,'NAME','TEXT')
#     with arcpy.da.UpdateCursor(okPolygon,'NAME') as yb:
#         for row in yb:
#             row[0] = riverName
#             yb.updateRow(row)
#
#     allPolygonList.append(okPolygon)
# finalShp = arcpy.CreateFeatureclass_management(path, 'all.shp', 'POLYGON')
# arcpy.AddField_management(finalShp,'NAME','TEXT')
# cs = arcpy.da.InsertCursor(finalShp, ['SHAPE@','NAME'])
# for polygon in allPolygonList:
#     print polygon
#     with arcpy.da.SearchCursor(polygon, ['SHAPE@', 'NAME']) as yb:
#         for row in yb:
#             cs.insertRow(row)



# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "查铺"
# arcpy.Dissolve_management(in_features="查铺", out_feature_class="E:/test/a.shp", dissolve_field="", statistics_fields="", multi_part="SINGLE_PART", unsplit_lines="DISSOLVE_LINES")