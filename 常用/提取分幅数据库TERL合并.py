#coding=utf-8
import arcpy
path = r'E:\数据整合\DLG\MDB\河湖划界\达曲\1W'
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True
mdbs = arcpy.ListFiles('*.mdb')
bouas = []
for mdb in mdbs:
    boua =  path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'BOUA'
    bouas.append(boua)
aL = arcpy.CreateFeatureclass_management(path,'temp.shp','POLYGON')
cs = arcpy.da.InsertCursor(aL,'SHAPE@')
for boua in bouas:
    print boua
    with arcpy.da.SearchCursor(boua,'SHAPE@') as yb2:
        for row2 in yb2:
            cs.insertRow(row2)
Shp = arcpy.Dissolve_management(aL,path + '\\' + 'BOUA.shp')
# arcpy.Delete_management(aL)
# arcpy.AddField_management(Shp,'类型','TEXT')
# arcpy.AddField_management(Shp,'格式','TEXT')
# arcpy.AddField_management(Shp,'项目类型','TEXT')
# arcpy.AddField_management(Shp,'项目名称','TEXT')
# arcpy.AddField_management(Shp,'参数','TEXT')
# arcpy.AddField_management(Shp,'数据容量','TEXT')
# arcpy.AddField_management(Shp,'时相','TEXT')
# arcpy.AddField_management(Shp,'坐标系','TEXT')
# ds = arcpy.Describe(Shp)
# if '\\MDB\\' in ds.path:
#     arcpy.CalculateField_management(Shp,'类型',"'DLG'",'PYTHON_9.3')
#     arcpy.CalculateField_management(Shp,'格式',"'MDB'",'PYTHON_9.3')