#coding=utf-8
import arcpy
import os
path = r"D:\2021年项目\TEST\分幅".decode('utf-8')
os.chdir(path)
arcpy.env.workspace = path
out_path = path
rasters = arcpy.Raster('朗村隆巴沟8bit.tif')
arcpy.Delete_management('fw.shp')
arcpy.Delete_management('fwpx.shp')
arcpy.Delete_management('r_d.shp')
ex = rasters.extent
x = ex.XMin
y = ex.YMin
x1 = ex.XMax
y1 = ex.YMax
xlen = ex.XMax-ex.XMin
ylen = ex.YMax-ex.YMin
cod1 = str(x) + ' ' + str(y)
cod2 = str(x) + ' ' + str(y1+10)
cod3 = str(x1) + ' ' + str(y1)
print(cod1,cod2,cod3)
arcpy.CreateFishnet_management('fw.shp',template= rasters,labels= 'NO_LABELS',origin_coord=cod1,y_axis_coord=cod2,corner_coord = cod3,number_columns = '',number_rows = '' ,geometry_type='POLYGON',cell_width=1000,cell_height=1000)
arcpy.Sort_management('fw.shp','fwpx.shp',sort_field="Shape ASCENDING",spatial_sort_method='UL')