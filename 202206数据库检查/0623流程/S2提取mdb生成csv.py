#coding=utf-8
import arcpy
import os
import pandas as pd
arcpy.env.overwriteOutput=True
# xqlist = ['稻城','得荣' ,'德格','甘孜','九龙','炉霍','泸定','色达','石渠', '乡城','新龙']
xqlist = ['炉霍']
for xq in xqlist:
    path =  r'E:\2022年项目\0621甘孜断面' + '\\' + xq
    mdbsPath = path + '\\' + 'mdb'
    arcpy.env.workspace = mdbsPath
    outpath = path + '\\' + 'csv'
    mdbs = arcpy.ListFiles('*.mdb')
    print xq,len(mdbs)
    cnList = []
    try:
        i=1
        for mdb in mdbs:
            Len = len(mdbs)
            print str(i) + '/' + str(Len) + mdb
            DLG = mdbsPath + '\\' + mdb.encode('utf-8') + '\\' + 'DLG'
            dmal = DLG + '\\' + 'DMAL'
            ZBX = arcpy.Describe(DLG).spatialReference.name
            with arcpy.da.SearchCursor(dmal,['SHAPE@','GB','NAME','CODE'],"GB=922214",explode_to_points=True) as yb:
                for row in yb:
                    cn = [mdb,ZBX,row[2],row[3],row[0].centroid.X,row[0].centroid.Y,row[0].centroid.Z]
                    cnList.append(cn)
            i+=1
        df = pd.DataFrame(cnList, columns=['Name', 'zbx','dmh','dmh2', 'x', 'y', 'h'])
        csv = outpath + '\\' + 'All_FromMDB.csv'
        df.to_csv(csv.decode('utf-8'), encoding='gbk', index=False)
    except:
        print xq,'problem'
