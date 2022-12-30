#coding=utf-8
import arcpy
path = r'E:\测试文件夹\test'
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True
mdbs = arcpy.ListFiles('*.mdb')
cptls = []
for mdb in mdbs:
    cptl =  path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'cptl'
    cptls.append(cptl)
aL = arcpy.CreateFeatureclass_management(path,'temp.shp','POLYLINE')
cs = arcpy.da.InsertCursor(aL,'SHAPE@')
for cptl in cptls:
    print cptl
    with arcpy.da.SearchCursor(cptl,'SHAPE@') as yb2:
        for row2 in yb2:
            cs.insertRow(row2)
Shp = arcpy.Dissolve_management(aL,path + '\\' + 'cptl.shp')
arcpy.Delete_management(aL)
