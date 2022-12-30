#coding=utf-8
import arcpy
path = r'C:\Users\Administrator\Desktop\0615检查\曲登沟\mdb'
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True
mdbs = arcpy.ListFiles('*.mdb')
arcpy.CreateFolder_management(path,'temp')
arcpy.CreateFolder_management(path,'shp')
shpList =['dmap','cptl','hydl','dmal','hfcl','hyda','dmaa','boua']

def extract_from_mdb_shp(shpName):
    shps = []
    for mdb in mdbs:
        shp = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + shpName
        shp2 = arcpy.FeatureClassToFeatureClass_conversion(shp, path + '\\' + 'temp',
                                                           arcpy.Describe(mdb).name.replace('-', '').replace('.mdb',
                                                                                                             '') + arcpy.Describe(
                                                               shp).name + '.shp')
        shps.append(shp2)
    arcpy.Merge_management(shps, path + '\\' + 'shp' + '\\' + '{}.shp'.format(shpName))
for v in shpList:
    extract_from_mdb_shp(v)
