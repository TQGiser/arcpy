#coding=utf-8
import arcpy
import os
import pandas as pd
arcpy.env.overwriteOutput=True
path = r'E:\2022年项目\0621甘孜断面\道孚\mdb'
outpath = r'E:\2022年项目\0621甘孜断面\道孚\csv'
mdbPathList = []
cnList = []
for i,v,m in os.walk(path.decode('utf-8')):
    for f in m :
        if '.mdb' in f and 'DOM' not in f and 'DEM' not in f and 'DLG' not in f:
            mdb = os.path.join(i,f)
            print mdb
            DLG = mdb + '\\' + 'DLG'
            DMAL = DLG + '\\' + 'DMAL'
            sf = arcpy.Describe(DLG).spatialReference
            ZBX = sf.PCSCode
            with arcpy.da.SearchCursor(DMAL,['SHAPE@','GB','NAME','CODE'],"GB=922214",explode_to_points=True) as yb:
                for row in yb:
                    cn = [f,ZBX,row[2],row[3],row[0].centroid.X,row[0].centroid.Y,row[0].centroid.Z]
                    cnList.append(cn)
df = pd.DataFrame(cnList, columns=['Name', 'zbx','dmh','dmh2', 'x', 'y', 'h'])
csv = outpath + '\\' + 'All_FromMDB.csv'
df.to_csv(csv.decode('utf-8'), encoding='gbk', index=False)
