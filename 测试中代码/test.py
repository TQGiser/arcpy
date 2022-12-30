#coding=utf-8
import arcpy
# path = r'C:\Users\Administrator\Desktop\TEST'.decode('utf-8')
# arcpy.env.workspace = path
# dmd = r'C:\Users\Administrator\Desktop\TEST\断面点.shp'
# dmx = r'C:\Users\Administrator\Desktop\TEST\断面线fg2.shp'
# cdlst = []
# sr = arcpy.Describe(dmd).spatialReference
# with arcpy.da.SearchCursor(dmd,['SHAPE@X','SHAPE@Y','SHAPE@Z']) as yb:
#     for row in yb:
#         cdlst.append([row[0],row[1],row[2]])
# arcpy.CreateFeatureclass_management(path,'createPolyline','POLYLINE',has_m= True,has_z= True,spatial_reference=sr)



# A list of features and coordinate pairs
# feature_info = [[[1, 2,10], [2, 4,20], [3, 7,10]],
#                 [[6, 8,15], [5, 7,13], [7, 2,13], [9, 5,15]]]
#
# # A list that will hold each of the Polyline objects
# features = []
#
# for feature in feature_info:
#     # Create a Polyline object based on the array of points
#     # Append to the list of Polyline objects
#     features.append(arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in feature])))
#     features.append(arcpy.Point)
#
# # Persist a copy of the Polyline objects using CopyFeatures
# arcpy.CopyFeatures_management(features, r"C:\Users\Administrator\Desktop\TEST\polylines.shp")

arcpy.env.workspace = r'C:\Users\Administrator\Desktop\TEST'
pointList = [[1,2,0.2],[3,5,0.11],[7,3,0.12]]
point = arcpy.Point()
pointGeometryList = []
for pt in pointList:
    point.X = pt[0]
    point.Y = pt[1]
    point.Z = pt[2]
    pointGeometry = arcpy.PointGeometry(point,has_z = 'ENABLED')
    pointGeometryList.append(pointGeometry)
arcpy.CopyFeatures_management(pointGeometryList, "C:\Users\Administrator\Desktop\TEST\points.shp")

