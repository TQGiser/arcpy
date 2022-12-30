# coding=utf-8
import arcpy
arcpy.env.overwriteOutput=True
path = r'E:\2022年项目\0802理塘入库'
arcpy.env.workspace = path
dmx = r'E:\2022年项目\0802理塘入库\理塘断面线改8.9\dmx102.shp'
sf = arcpy.Describe(dmx).spatialReference
riverList = []
with arcpy.da.SearchCursor(dmx, 'river') as yb:
    for row in yb:
        if row[0] not in riverList:
            riverList.append(row[0])

for river in riverList:
    print river
    shpList = []
    # expression = u"RIVER = '{}'".format(river)
    expression = "RIVER = '{}'".format(river.encode('utf-8'))
    with arcpy.da.SearchCursor(dmx, ['SHAPE@', 'GB', 'HNNM', 'RIVER', 'dmh'],
                               where_clause= expression) as yb:
        for row in yb:
            shp = [row[0], row[1], row[2], row[3], row[4]]
            print row[3], row[4]
            shpList.append(shp)
    shp = arcpy.CreateFeatureclass_management(path + '\\'+'shps', '{}.shp'.format(river.encode('utf-8')), 'POLYLINE',has_z='ENABLED')
    arcpy.DefineProjection_management(shp, coor_system=sf)
    arcpy.AddField_management(shp, 'GB', 'LONG')
    arcpy.AddField_management(shp, 'HNNM', 'TEXT')
    arcpy.AddField_management(shp, 'RIVER', 'TEXT')
    arcpy.AddField_management(shp, 'DMH', 'TEXT')
    yb = arcpy.da.InsertCursor(shp, ['SHAPE@','GB', 'HNNM', 'RIVER', 'dmh'])
    for shp in shpList:
        yb.insertRow(shp)
    del yb
