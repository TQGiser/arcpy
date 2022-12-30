#coding=utf-8
import arcpy
import os
import pandas as pd
path = r'D:\2021年项目\0712湖泊数据库\0709MDB成果'
outpath = r'D:\2021年项目\0712湖泊数据库'
xlspath = r'D:\2021年项目\0712湖泊数据库\xls'
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