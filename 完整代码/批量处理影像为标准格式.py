#coding=utf-8
import arcpy
import os
import shutil
import re
path = r'D:\2021年项目\0406江北DLG检查\DOM'.decode('utf-8')
out_path = r'D:\2021年项目\0406江北DLG检查\DOM\OK'.decode('utf-8')
arcpy.env.workspace = path
os.chdir(path)
rasters_ys = []
rasters_8bit = []
clip_all_frame = []
DLMC = '雅江县段'
for i,v,m in os.walk(path):
    for rasname in m:
        if rasname.endswith('.tif'):
            rasters_ys.append(rasname)
for name in rasters_ys:
    print(name)
    fn = name.strip('.tif')
    ras = arcpy.Raster(name)
    tif_transto_8bit = name.strip('.tif') + '16bit_Projected' + '.tif'
    arcpy.env.workspace = out_path
    arcpy.env.compression = 'NONE'
    arcpy.DefineProjection_management(name,coor_system='4543')
