# coding=utf-8
import arcpy
import os
import pandas as pd

arcpy.env.overwriteOutput = True
# riverList = ['阿洛沟', '绰斯甲河', '定曲', '东谷河',
#              '俄热河', '革什扎河', '霍曲', '理塘河',
#              '立曲', '玛曲','莫曲','那曲', '庆达沟',
#              '热衣曲','色曲','水洛河','松林河','田湾河',
#              '鲜水河','小金川','赠曲']
riverList = ['革什扎河']
for river in riverList:
    path = r'E:\2022年项目\0621甘孜断面\洲际' + '\\' + river
    try:
        arcpy.CreateFolder_management(path, 'csv')
        arcpy.CreateFolder_management(path, 'shp')
    except:
        pass
    mdbsPath = path + '\\' + 'mdb'
    arcpy.env.workspace = mdbsPath
    outpath = path + '\\' + 'csv'
    mdbs = arcpy.ListFiles('*.mdb')
    cnList = []
    try:
        i = 1
        for mdb in mdbs:
            Len = len(mdbs)
            print str(i) + '/' + str(Len) + mdb
            DLG = mdbsPath + '\\' + mdb.encode('utf-8') + '\\' + 'DLG'
            dmal = DLG + '\\' + 'DMAL'
            ZBX = arcpy.Describe(DLG).spatialReference.name
            with arcpy.da.SearchCursor(dmal, ['SHAPE@', 'GB', 'NAME', 'CODE'], "GB=922214", explode_to_points=True) as yb:
                for row in yb:
                    cn = [mdb, ZBX, row[2], row[3], row[0].centroid.X, row[0].centroid.Y, row[0].centroid.Z]
                    cnList.append(cn)
            i += 1
        df = pd.DataFrame(cnList, columns=['Name', 'zbx', 'dmh', 'dmh2', 'x', 'y', 'h'])
        csv = outpath + '\\' + 'All_FromMDB.csv'
        df.to_csv(csv.decode('utf-8'), encoding='gbk', index=False)
    except:
        print river, 'problem'
