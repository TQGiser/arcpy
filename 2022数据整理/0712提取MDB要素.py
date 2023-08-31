#coding=utf-8
import arcpy
path = r'C:\Users\Administrator\Desktop\新建文件夹'
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True
mdbs = arcpy.ListFiles('*.mdb')
arcpy.CreateFolder_management(path,'temp')
arcpy.CreateFolder_management(path,'shp')
shps = []
def extract_FromMDB(shpname):
    for mdb in mdbs:
        print mdb
        shp =  path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + shpname
        tempshpname = arcpy.Describe(mdb).name.replace('-','').replace('.mdb','') + arcpy.Describe(shp).name + '.shp'
        shp2 = arcpy.FeatureClassToFeatureClass_conversion(shp,path + '\\' + 'temp',tempshpname)
        shps.append(shp2)
    arcpy.Merge_management(shps,path + '\\' + 'shp' + '\\' + '{}.shp'.format((shpname)))

extract_FromMDB('DMAL')