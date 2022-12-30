import arcpy
from osgeo import ogr
fc = (r'E:\arcpy\data\0322.gdb\asdf')
arcpy.Delete_management(r'E:\arcpy\data\0322.gdb\asdf')
arcpy.CreateFeatureclass_management(r'E:\arcpy\data\0322.gdb','asdf','POLYLINE')
fc = (r'E:\arcpy\data\0322.gdb\asdf')
cursor = arcpy.da.InsertCursor(fc, ["SHAPE@"])
array = arcpy.Array([arcpy.Point(-77.4349451, 37.5408265),
                     arcpy.Point(-78.6384349, 35.7780943)])
spatial_reference = arcpy.SpatialReference(4326)
polyline = arcpy.Polyline(array, spatial_reference)
cursor.insertRow([polyline])



# Delete cursor and row objects
del cursor