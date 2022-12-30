#coding=utf-8
import arcpy
import os
import pandas as pd
path = r'D:\2021年项目\0712湖泊数据库\0709MDB成果'
xlspath = r'D:\2021年项目\0712湖泊数据库\xls'
arcpy.env.workspace = path
walk = arcpy.da.Walk(path, datatype="FeatureClass", type='Point')
dmaplst = []
for i, v, m in walk:
    for s in m:
        if 'DMAP' in s:
            dmap =  os.path.join(i,s)
            with arcpy.da.UpdateCursor(dmap,['NAME','NUM']) as yb:
                for row in yb:
                    if row[1] == '':
                        xls = xlspath + '\\' + '{}.xlsx'.format(dmap.encode('utf-8').split('.mdb')[0].split('\\')[-1])
                        df = pd.read_excel(xls.decode('utf-8'),header=1)
                        lc = df[df['桩名（编号）'.decode('utf-8')] == '{}'.format(row[0].encode('utf-8')).decode('utf-8')][
                            '里程'.decode('utf-8')].values[0]
                        row[1] = lc
                        yb.updateRow(row)
                        print row[0],lc
