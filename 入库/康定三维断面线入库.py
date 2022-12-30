# coding=utf-8
import arcpy
import os
import math
import pandas as pd
import F
df = pd.read_excel(r'E:\2021年项目\1122康定1W段入库\康定市62条河流水系表.xlsx'.decode('utf-8'))
path = r'E:\2021年项目\1130断面线入库\康定全部断面线'
dmals = F.listFiles(path,'','x')
for dmal in dmals:
    riverName = arcpy.Describe(dmal).basename.encode('utf-8')
    print riverName
    for name, value in df.iterrows():
        if riverName in (df.loc[name,'河流名称'.decode('utf-8')]).encode('utf-8'):
            sx = (df.loc[name,'水系'.decode('utf-8')]).encode('utf-8')
    arcpy.AddField_management(dmal,'GB','LONG')
    arcpy.CalculateField_management(dmal, 'GB', '922214', 'PYTHON_9.3')
    arcpy.AddField_management(dmal,'RIVER','TEXT')
    arcpy.AddField_management(dmal,'HNNM','TEXT')
    with arcpy.da.UpdateCursor(dmal,['RIVER','HNNM'])as yb:
        for row in yb:
            row[0] = riverName
            row[1] = sx
            yb.updateRow(row)
path2 = r'E:\2021年项目\1130断面线入库\康定2KMDB'
arcpy.env.workspace= path2
mdbs = arcpy.ListFiles('*.mdb')
for mdb in mdbs:
    print mdb
    riverName = arcpy.Describe(mdb).name.replace('.mdb', '')
    mdb = r'E:\2021年项目\1130断面线入库\康定2KMDB\{}'.format(mdb.encode('utf-8'))
    dmal = r'E:\2021年项目\1130断面线入库\康定全部断面线\{}.shp'.format(riverName.encode('utf-8'))
    dmalInMdb = mdb + '\\' + 'DLG' + '\\' + 'DMAL'
    arcpy.Append_management(dmal,dmalInMdb,schema_type='NO_TEST')


