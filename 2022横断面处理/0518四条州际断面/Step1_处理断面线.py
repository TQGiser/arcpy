# coding=utf-8
import arcpy
import os
import math
import pinyin
path = r'E:\2022年项目\0519定曲断面\shp'
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True
name = r'定曲'
walk = arcpy.da.Walk(path, datatype="FeatureClass", type='Polyline')
zxlst = []
dmxlst = []
for i, v, m in walk:
    for s in m:
        if '中线'.decode('utf-8') in s:
            zxlst.append(os.path.join(i, s))
        if '断面线'.decode('utf-8') in s:
            dmxlst.append(os.path.join(i, s))
walk = arcpy.da.Walk(path, datatype="FeatureClass", type='Point')
lcdlst = []
for i, v, m in walk:
    for s in m:
        if '里程'.decode('utf-8') in s:
            lcdlst.append(os.path.join(i, s))
yslcd = lcdlst[0]
yszx = zxlst[0]
ysdmx = dmxlst[0]
arcpy.CreateFolder_management(path, 'stuff')
dmx = path + '\\' + 'stuff' + '\\' + 'dmx.shp'
arcpy.CopyFeatures_management(ysdmx,dmx)
arcpy.AddField_management(dmx,'Lj','LONG')
arcpy.CalculateField_management(dmx,'Lj','!FID!','PYTHON_9.3')
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
with arcpy.da.UpdateCursor(lcd,['里程','LC']) as yb:
    for row in yb:
        if '+' in row[0]:
            row[1] = int(row[0].split('+')[0].replace('K',''))*1000 + int(row[0].split('+')[1])
        else:
            row[1] = float(row[0].replace('K',''))*1000
        yb.updateRow(row)
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
gdbPath = path + '\\' + 'stuff'
gdb = arcpy.CreateFileGDB_management(gdbPath, name)
zxLc = gdbPath + '\\' + '{}.gdb'.format(name) + '\\' + 'zxLc'
arcpy.CreateRoutes_lr(zx, 'NAME', zxLc, coordinate_priority='{}'.format(coordinate_priority))
JzhZx = gdbPath + '\\' + '{}.gdb'.format(name) + '\\' + 'JzhZx'
finalshp = arcpy.CalibrateRoutes_lr(zxLc, 'NAME', lcd, 'NAME', 'LC', JzhZx, search_radius=500)
arcpy.CopyFeatures_management(finalshp,path + '\\' + '{}校正后中线.shp'.format(name))
dmLcd = path + '\\' + 'stuff' + '\\' + 'dmLcd.shp'
dmxJd = arcpy.Intersect_analysis(in_features= '{} #;{} #'.format(dmx,JzhZx),out_feature_class=dmLcd,output_type='POINT')
jdTable = path + '\\' + 'stuff' + '\\' + 'jdTable_test'
arcpy.LocateFeaturesAlongRoutes_lr(in_features=dmxJd,in_routes=JzhZx,
                                   route_id_field="NAME",
                                   radius_or_tolerance="10 Meters",
                                   out_table=jdTable,
                                   out_event_properties="RID POINT MEAS",
                                   route_locations="FIRST",
                                   distance_field="DISTANCE",
                                   zero_length_events="ZERO",
                                   in_fields="NO_FIELDS",
                                   m_direction_offsetting="M_DIRECTON")                          #NO_FIELDS 保证乱码字段不输出
arcpy.JoinField_management(in_data=dmx,in_field="Lj", join_table=jdTable, join_field="INPUTOID", fields="MEAS")
dmx_sorted = path + '\\' + '{}校正后断面线.shp'.format(name)
arcpy.Sort_management(dmx,dmx_sorted,'MEAS DESCENDING')
arcpy.AddField_management(dmx_sorted,'dmh','TEXT')
arcpy.AddField_management(dmx_sorted,'里程','TEXT')
arcpy.AddField_management(dmx_sorted,'间距','TEXT')
with arcpy.da.UpdateCursor(dmx_sorted,['dmh','MEAS','里程','间距']) as yb:
    a = 1
    lcList = [0.0]
    for row in yb:
        row[0] = pinyin.get_initial('{}'.format(name)).replace(' ','').upper() + '-' + '%03d'%a
        row[2] = 'K' + str(int(row[1] / 1000.0)) + '+' + '%03d' % (round(row[1]%1000))
        row[3] = round(abs(row[1] - lcList[-1]))
        if len(lcList) == 1:
            row[3] =0.0
        lcList.append(row[1])
        yb.updateRow(row)
        a +=1