#coding=utf-8
import arcpy
path = r'D:\CesiumData\鲜水河\里程点'
arcpy.env.workspace =path
arcpy.env.overwriteOutput=True
dem = r'E:\数据\甘孜藏族自治州12.5米DEM\甘孜藏族自治州.tif'
p = r'D:\CesiumData\鲜水河\里程点\鲜水河_sc.shp'
spatial_ref = arcpy.Describe(p).spatialReference
cnList =[]
with arcpy.da.SearchCursor(p,['SHAPE@','里程','XZQMC','XJQYMC']) as yb:
    for row in yb:
        cn = [row[0].centroid.X,row[0].centroid.Y,row[1],row[2],row[3]]
        cnList.append(cn)
nPoint = arcpy.CreateFeatureclass_management(path,'np','POINT',spatial_reference=spatial_ref,has_z='ENABLED')
arcpy.AddField_management(nPoint,'里程','TEXT')
arcpy.AddField_management(nPoint,'XZQMC','TEXT')
arcpy.AddField_management(nPoint,'XJQYMC','TEXT')
yb = arcpy.da.InsertCursor(nPoint,['SHAPE@X','SHAPE@Y','里程','XZQMC','XJQYMC'])
for p in cnList:
    yb.insertRow(p)
del yb
np84 = arcpy.Project_management(nPoint,path + '\\' + 'np84.shp','4326')
arcpy.Delete_management(nPoint)
with arcpy.da.UpdateCursor(np84,['SHAPE@X','SHAPE@Y','SHAPE@Z']) as yb:
    for row in yb:
        E = row[0]
        N = row[1]
        row[2] = str(arcpy.GetCellValue_management(in_raster=dem, location_point='{} {}'.format(E, N)))
        print E,N,row[2]
        yb.updateRow(row)