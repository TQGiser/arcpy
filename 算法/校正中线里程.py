# coding=utf-8
import arcpy
import os
import math
import pinyin
path = r'E:\2021年项目\1013岸线规划\那曲\ZX-NQ'.decode('utf-8')
arcpy.env.workspace = path
name = raw_input('河流名称:')
walk = arcpy.da.Walk(path, datatype="FeatureClass", type='Polyline')
zxlst = []
for i, v, m in walk:
    for s in m:
        if '中线'.decode('utf-8') in s:
            zxlst.append(os.path.join(i, s))
walk = arcpy.da.Walk(path, datatype="FeatureClass", type='Point')
lcdlst = []
for i, v, m in walk:
    for s in m:
        if '里程'.decode('utf-8') in s:
            lcdlst.append(os.path.join(i, s))
yslcd = lcdlst[0]
yszx = zxlst[0]
arcpy.CreateFolder_management(path, 'stuff')
sr = arcpy.Describe(yszx).spatialReference.factoryCode
sr_p_99 = arcpy.SpatialReference(4542)
sr_p_102 = arcpy.SpatialReference(4543)
lcd = path + '\\' + 'stuff' + '\\' + 'lcd.shp'
cm2 = (arcpy.Describe(yslcd).extent.XMax + arcpy.Describe(yszx).extent.XMin) / 2
if cm2 > 97.5 and cm2 < 100.5:
    arcpy.Project_management(yslcd, lcd, out_coor_system=sr_p_99)
elif cm2 > 100.5 and cm2 < 103.5:
    arcpy.Project_management(yslcd, lcd, out_coor_system=sr_p_102)
else:
    arcpy.CopyFeatures_management(yslcd,lcd)
arcpy.AddField_management(lcd, 'NAME', 'TEXT')
arcpy.CalculateField_management(lcd, 'NAME', '"{}"'.format(name))
arcpy.AddField_management(lcd, 'LC', 'DOUBLE')
arcpy.CalculateField_management(lcd, 'LC', "float(!里程!.replace('+','.').replace('K',''))*1000", 'PYTHON_9.3')
xmax = arcpy.Describe(lcd).extent.XMax
ymax = arcpy.Describe(lcd).extent.YMax
xmin = arcpy.Describe(lcd).extent.XMin
ymin = arcpy.Describe(lcd).extent.YMin
expression = '{} = 0'.format(arcpy.AddFieldDelimiters(lcd, 'LC'))
with arcpy.da.SearchCursor(lcd, ['SHAPE@X', 'SHAPE@Y', 'LC'], where_clause=expression) as yb:
    for row in yb:
        x = row[0]
        y = row[1]
        UPPER_LEFT = math.sqrt((x - xmin) ** 2 + (y - ymax) ** 2)
        LOWER_LEFT = math.sqrt((x - xmin) ** 2 + (y - ymin) ** 2)
        UPPER_RIGHT = math.sqrt((x - xmax) ** 2 + (y - ymax) ** 2)
        LOWER_RIGHT = math.sqrt((x - xmax) ** 2 + (y - ymin) ** 2)
data = {'UPPER_LEFT': UPPER_LEFT, 'LOWER_LEFT': LOWER_LEFT, 'UPPER_RIGHT': UPPER_RIGHT, 'LOWER_RIGHT': LOWER_RIGHT}
coordinate_priority = min(data, key=data.get)
zx = path + '\\' + 'stuff' + '\\' + 'zx.shp'
cm = (arcpy.Describe(yszx).extent.XMax + arcpy.Describe(yszx).extent.XMin) / 2
if cm > 97.5 and cm < 100.5:
    arcpy.Project_management(yszx, zx, out_coor_system=sr_p_99)
elif cm > 100.5 and cm < 103.5:
    arcpy.Project_management(yszx, zx, out_coor_system=sr_p_102)
else:
    arcpy.CopyFeatures_management(yszx,zx)
arcpy.AddField_management(zx, 'NAME', 'TEXT')
arcpy.CalculateField_management(zx, 'NAME', '"{}"'.format(name))
gdbPath = path.encode('utf-8') + '\\' + 'stuff'
gdb = arcpy.CreateFileGDB_management(gdbPath, name)
zxLc = gdbPath + '\\' + '{}.gdb'.format(name) + '\\' + 'zxLc'
arcpy.CreateRoutes_lr(zx, 'NAME', zxLc, coordinate_priority='{}'.format(coordinate_priority))
JzhZx = gdbPath + '\\' + '{}.gdb'.format(name) + '\\' + 'JzhZx'
arcpy.CalibrateRoutes_lr(zxLc, 'NAME', lcd, 'NAME', 'LC', JzhZx, search_radius=500)