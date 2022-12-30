# coding=utf-8
import os
import arcpy
path = r'D:\2021年项目\0601湖泊划界\方哥\理塘县\达弄错'.decode('utf-8')
arcpy.env.workspace = path
shp = r'D:\2021年项目\0601湖泊划界\方哥\理塘县\达弄错\达弄错电子桩.shp'
fields = arcpy.ListFields(shp)
for field in fields:
    a = field.name.encode('utf-8')
    if a != '里程' and a != 'FID'.decode('utf-8') and a!= 'Shape'.decode('utf-8') and a != 'NAME'.decode('utf-8'):
        arcpy.DeleteField_management(shp,'{}'.format(a))
    else:
        pass
