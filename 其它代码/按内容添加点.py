import arcpy
import os
os.chdir(r'E:\arcpy\data\0322.gdb')
arcpy.env.workspace = (r'E:\arcpy\data\0322.gdb')
#arcpy.AddField_management('t4','NAME','TEXT')
#arcpy.AddField_management('t4','COORDI','DOUBLE')
cs = arcpy.da.InsertCursor('t4',('NAME','COORDI'))
row_value = ('ADFS',335522)
for row in row_value:
    cs.insertRow(row)
del row