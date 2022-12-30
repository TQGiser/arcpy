#coding=utf-8
import arcpy
path = r'E:\2022年项目\0727理塘断面\mdball'
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True
mdbs = arcpy.ListFiles('*.mdb')
SPList =['DMAP','DMAL','DMAA','HFCL']
for mdb in mdbs:
    print mdb,type(mdb.encode('utf-8'))
    arcpy.CreateFolder_management(path, '{}'.format(mdb.encode('utf-8')).replace('.mdb',''))
    for SP in SPList:
        shp =  path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + SP
        arcpy.FeatureClassToFeatureClass_conversion(shp,path + '\\' + '{}'.format(mdb.encode('utf-8')).replace('.mdb',''),'{}.shp'.format(SP))
