# coding=utf-8
import arcpy
import pandas
import os
path = r'D:\2021年项目\0628提取数据库\102-all'.decode('utf-8')
mdblst = []
for i,v,m in os.walk(path):
    mdblst = m
for mdb in mdblst:
    try:
        arcpy.env.workspace = path.encode('utf-8') + '\\' + mdb.encode('utf-8')
        terlShpName = mdb.encode('utf-8').split('.')[0].replace('-', '')
        if '#' in mdb:
            terlShpName =  mdb.encode('utf-8').split('.')[0].replace('-','').replace('#','')
        arcpy.CopyFeatures_management('BOUA',r'D:\2021年项目\0628提取数据库\BOUA102\{}'.format(terlShpName))
        print '{} is  done'.format(terlShpName)
    except:
        print '{} *******'.format(terlShpName)
