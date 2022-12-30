#coding=utf-8
import arcpy
import os
path = r'E:\GeoServerData\DOM\99CG'
arcpy.env.workspace = path
rasList= []
for i,v,m in os.walk(path.decode('utf-8')):
    for ras in m:
        if '.tif' in ras:
            rasList.append(os.path.join(i,ras))
for ras in rasList:
    print ras
    arcpy.DefineProjection_management(ras,coor_system='4542')


   # arcpy.ProjectRaster_management(ras[0] +'\\' + ras[1],ras[0]+ '\\' + ras[1].replace('.tif') + '_wgs84.tif')
