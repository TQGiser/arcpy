#coding=utf-8
import arcpy
path = r'E:\2022年项目\0621甘孜断面\白玉\mdb'
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True
mdbs = arcpy.ListFiles('*.mdb')
shps = []
for mdb in mdbs:
    shp =  path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'DMAL'
    shps.append(shp)
aL = arcpy.CreateFeatureclass_management(path,'temp.shp','POLYLINE')
cs = arcpy.da.InsertCursor(aL,'SHAPE@')
for s in shps:
    print s
    with arcpy.da.SearchCursor(s,'SHAPE@',"GB=922214") as yb2:
        for row2 in yb2:
            cs.insertRow(row2)
Shp = arcpy.Dissolve_management(aL,path + '\\' + 'dmal.shp')
arcpy.Delete_management(aL)
