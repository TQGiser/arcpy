#coding=utf-8
import arcpy
path = r'E:\数据存储\DLG\MDB\河湖划界'
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True
mdbs = arcpy.ListFiles('*.mdb')
bouas = []
for mdb in mdbs:
    boua =  path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'DMAA'
    bouas.append(boua)
aL = arcpy.CreateFeatureclass_management(path,'temp.shp','POLYGON')
cs = arcpy.da.InsertCursor(aL,'SHAPE@')
for boua in bouas:
    print boua
    with arcpy.da.SearchCursor(boua,'SHAPE@') as yb2:
        for row2 in yb2:
            cs.insertRow(row2)
Shp = arcpy.Dissolve_management(aL,path + '\\' + 'DMAA.shp')
arcpy.Delete_management(aL)
