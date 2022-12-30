# coding=utf-8
import arcpy
import os
import math

path = r'D:\2021年项目\0628理塘断面数据\多曲'.decode('utf-8')
arcpy.env.workspace = path
zx = r'D:\2021年项目\0628理塘断面数据\多曲\shape\中线.shp'.decode('utf-8')

sp = arcpy.Describe(zx).spatialReference.MDomain
lcd = r'D:\2021年项目\0628理塘断面数据\多曲\stuff\lcd.shp'.decode('utf-8')

a = arcpy.Describe(lcd).extent.XMin
expression = '{} = 0'.format(arcpy.AddFieldDelimiters(lcd, 'LC'))
xmax = arcpy.Describe(lcd).extent.XMax
ymax = arcpy.Describe(lcd).extent.YMax
xmin = arcpy.Describe(lcd).extent.XMin
ymin = arcpy.Describe(lcd).extent.YMin

with arcpy.da.SearchCursor(lcd, ['SHAPE@X', 'SHAPE@Y', 'LC'], where_clause=expression) as yb:
    for row in yb:
        x = row[0]
        y = row[1]
        UPPER_LEFT = math.sqrt((x - xmin) ** 2 + (y - ymax) ** 2)
        LOWER_LEFT = math.sqrt((x - xmin) ** 2 + (y - ymin) ** 2)
        UPPER_RIGHT = math.sqrt((x - xmax) ** 2 + (y - ymax) ** 2)
        LOWER_RIGHT = math.sqrt((x - xmax) ** 2 + (y - ymin) ** 2)
data = {'UPPER_LEFT':UPPER_LEFT,'LOWER_LEFT':LOWER_LEFT,'UPPER_RIGHT':UPPER_RIGHT,'LOWER_RIGHT':LOWER_RIGHT}
a = min(data,key=data.get)
print a

