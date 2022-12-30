# coding=utf-8
import arcpy
import os
import math
import pandas as pd
import F
df = pd.read_excel(r'E:\2021年项目\1221理塘断面线入库\理塘县73条县级河流长度统计表.xlsx'.decode('utf-8'))
path = r'E:\2021年项目\1221理塘断面线入库\全部三维断面线'
dmals = F.listFiles(path,'','x')
riverNameList = []
for dmal in dmals:
    riverName = arcpy.Describe(dmal).basename.encode('utf-8')
    riverNameList.append(riverName)
    for name,value in df.iterrows():
        if riverName in (df.loc[name,'河流'.decode('utf-8')]).encode('utf-8'):
            sx = (df.loc[name,'水系'.decode('utf-8')]).encode('utf-8')
    arcpy.AddField_management(dmal,'GB','LONG')
    arcpy.CalculateField_management(dmal, 'GB', '922214', 'PYTHON_9.3')
    arcpy.AddField_management(dmal,'RuleID','LONG')
    arcpy.CalculateField_management(dmal, 'RuleID', '8', 'PYTHON_9.3')
    arcpy.AddField_management(dmal,'RIVER','TEXT')
    arcpy.AddField_management(dmal,'HNNM','TEXT')
    with arcpy.da.UpdateCursor(dmal,['RIVER','HNNM'])as yb:
        for row in yb:
            row[0] = riverName
            row[1] = sx
            yb.updateRow(row)
path2 = r'E:\2021年项目\1221理塘断面线入库\全部数据库'
arcpy.env.workspace= path2
mdbs = arcpy.ListFiles('*.mdb')
for mdb in mdbs:
    riverName = arcpy.Describe(mdb).name.replace('.mdb', '').encode('utf-8')
    if riverName in riverNameList:
        print mdb
        mdb = r'E:\2021年项目\1221理塘断面线入库\全部数据库\{}'.format(mdb.encode('utf-8'))
        dmal = r'E:\2021年项目\1221理塘断面线入库\全部三维断面线\{}.shp'.format(riverName)
        dmalInMdb = mdb + '\\' + 'DLG' + '\\' + 'DMAL'
        arcpy.Append_management(dmal,dmalInMdb,schema_type='NO_TEST')