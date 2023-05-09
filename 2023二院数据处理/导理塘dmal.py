#coding=utf-8
import arcpy
import os
import pandas as pd
path = r'E:\2023年项目\0506二院数据\理塘县MDB\MDB'
outpath = r'E:\2023年项目\0506二院数据\理塘县MDB'
arcpy.env.workspace = path
walk = arcpy.da.Walk(path, datatype="FeatureClass", type='Polyline')
dmaplst = []
for i, v, m in walk:
    for s in m:
        if 'DMAL' in s:
            dmal =  os.path.join(i,s)
            print dmal
            dmal_shp = outpath + '\\' + 'dmal' + '\\' + '{}.shp'.format(
                dmal.encode('utf-8').split('.mdb')[0].split('\\')[-1])
            if '#' in dmal_shp:
                dmal_shp = outpath + '\\' + 'dmal' + '\\' + '{}.shp'.format(
                    dmal.encode('utf-8').split('.mdb')[0].split('\\')[-1].replace('#', ''))
            arcpy.CopyFeatures_management(dmal, dmal_shp)
            print dmal_shp