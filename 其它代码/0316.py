import arcpy
import os
os.chdir(r'E:\2021年项目\0319\1')
fc = '巴塘38条河.shp'
zdmc1 = 'Name'
zdmc2 = 'GroupName'
cursor = arcpy.UpdateCursor(fc)
arcpy.AddField_management(fc,'TEST','TEXT')
for row in cursor:
    row.setValue(zdmc2,row.getValue(zdmc1))
    cursor.updateRow(row)
