#coding=utf-8
import arcpy
import F
path = r'D:\CesiumData\cp\zx'
tif = r'E:\数据\甘孜藏族自治州12.5米DEM\甘孜藏族自治州.tif'
arcpy.env.workspace = path
arcpy.env.overwriteOutput=True
zx = F.listFile(path,'中线'.decode('utf-8'),'x')
spatial_ref = arcpy.Describe(zx).spatialReference
cnList =[]
with arcpy.da.SearchCursor(zx,'SHAPE@') as yb:
    for row in yb:
        riverLength = row[0].length
        i = 0.0
        while i <riverLength:
            E = row[0].positionAlongLine(i).centroid.X
            N = row[0].positionAlongLine(i).centroid.Y
            cn = [E,N]
            cnList.append(cn)
            i+=0.0008983152841195214           #度单位的100米
nPoint = arcpy.CreateFeatureclass_management(path,'np','POINT',spatial_reference=spatial_ref,has_z='ENABLED')
yb = arcpy.da.InsertCursor(nPoint,['SHAPE@X','SHAPE@Y'])
for p in cnList:
    yb.insertRow(p)
del yb
np84 = arcpy.Project_management(nPoint,path + '\\' + 'np84.shp','4326')
arcpy.Delete_management(nPoint)
with arcpy.da.UpdateCursor(np84,['SHAPE@X','SHAPE@Y','SHAPE@Z']) as yb:
    for row in yb:
        E = row[0]
        N = row[1]
        row[2] = str(arcpy.GetCellValue_management(in_raster=tif, location_point='{} {}'.format(E, N)))
        print E,N,row[2]
        yb.updateRow(row)
