#coding=utf-8
import arcpy
path = r'E:\数据部数据\数据整合\DLG\MDB\河湖划界\木弄\2K'
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True
mdbs = arcpy.ListFiles('*.mdb')
bouas = []
for mdb in mdbs:
    boua =  path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'HYDA'
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
