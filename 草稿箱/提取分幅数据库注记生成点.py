#coding=utf-8
import arcpy
import pythonaddins
import math
import F
path = r'E:\达曲'
arcpy.env.workspace = path
arcpy.env.overwriteOutput= True
mdbs = arcpy.ListFiles('*.mdb')
NpList = []
for mdb in mdbs:
    print mdb
    zj = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'ANNOTATION'
    yb = arcpy.da.SearchCursor(zj,['SHAPE@','TextString'])
    for row in yb:
        cn = [row[0].centroid,row[1]]
        NpList.append(cn)
NP = arcpy.CreateFeatureclass_management(path,'all.shp','POINT')
arcpy.AddField_management(NP,'name','Text')
cs = arcpy.da.InsertCursor(NP,['SHAPE@','name'])
for p in NpList:
    cs.insertRow(p)


