#coding=utf-8
import arcpy
path = r'E:\数据存储\DLG\MDB\河湖划界\德曲\1W'
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True
Shp = arcpy.ListFiles('*.shp')[0]
arcpy.AddField_management(Shp,'类型','TEXT')
arcpy.AddField_management(Shp,'格式','TEXT')
arcpy.AddField_management(Shp,'项目类型','TEXT')
arcpy.AddField_management(Shp,'项目名称','TEXT')
arcpy.AddField_management(Shp,'参数','TEXT')
arcpy.AddField_management(Shp,'数据容量','TEXT')
arcpy.AddField_management(Shp,'时相','TEXT')
arcpy.AddField_management(Shp,'坐标系','TEXT')
ds = arcpy.Describe(Shp)
if '\\MDB\\' in ds.path:
    arcpy.CalculateField_management(Shp,'类型',"'DLG'",'PYTHON_9.3')
    arcpy.CalculateField_management(Shp,'格式',"'MDB'",'PYTHON_9.3')
elif '\\DWG\\' in ds.path:
    arcpy.CalculateField_management(Shp, '类型', "'DLG'", 'PYTHON_9.3')
    arcpy.CalculateField_management(Shp, '格式', "'DWG'", 'PYTHON_9.3')

elif '河湖划界' in ds.path.decode('utf-8'):
    arcpy.CalculateField_management(Shp, '项目类型', "'河湖划界'", 'PYTHON_9.3')
# proName = ds.path.encode('utf-8')
# proName1 = proName.split('河湖划界')[1].replace('\\','')
