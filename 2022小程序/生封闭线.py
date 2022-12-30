#coding=utf-8
import arcpy
import F

# dmal = r'E:\测试文件夹\柯拉柯雅江县段.shp'
# tLine = r'E:\测试文件夹\insertLineTest.shp'
# scCs= arcpy.da.SearchCursor(dmal,'SHAPE@')
# l1 = scCs.next()[0]
# l2 = scCs.next()[0]
# sp1 = l1.firstPoint
# ep1 = l1.lastPoint
# sp2 = l2.firstPoint
# ep2 = l2.lastPoint
# array = arcpy.Array([sp1,sp2])
# sl = arcpy.Polyline(array)
# array = arcpy.Array([ep1,ep2])
# el = arcpy.Polyline(array)
# isCs = arcpy.da.InsertCursor(tLine,'SHAPE@')
# isCs.insertRow([sl])
# isCs.insertRow([el])

arcpy.env.overwriteOutput = True
path = r'E:\测试文件夹\102'
dmals = F.listFiles(path,'','x')
sp = arcpy.SpatialReference(4543)
tLine = arcpy.CreateFeatureclass_management(r'E:\测试文件夹','asLine.shp','POLYLINE',spatial_reference=sp)

for dmal in dmals:
    print dmal
    scCs = arcpy.da.SearchCursor(dmal, 'SHAPE@')
    lines = [row[0] for row in scCs]
    sps = [line.firstPoint for line in lines]
    eps = [line.lastPoint for line in lines]
    array = arcpy.Array([point for point in sps])
    sl = arcpy.Polyline(array)
    array = arcpy.Array([point for point in eps])
    el = arcpy.Polyline(array)
    isCs = arcpy.da.InsertCursor(tLine, 'SHAPE@')
    isCs.insertRow([sl])
    isCs.insertRow([el])