#coding=utf-8
import arcpy
path = r'E:\2022年项目\1107鲜水河断面\mdb'
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True
mdbs = arcpy.ListFiles('*.mdb')
try:
    arcpy.CreateFolder_management(path,'temp')
    arcpy.CreateFolder_management(path,'temp2')
    arcpy.CreateFolder_management(path,'shp')
except:
    pass
shps = []
def extract_FromMDB(shpname):
    for mdb in mdbs:
        print mdb
        shp =  path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + shpname
        tempshpname = arcpy.Describe(mdb).name.replace('-','').replace('.mdb','') + arcpy.Describe(shp).name + '.shp'
        shp2 = arcpy.FeatureClassToFeatureClass_conversion(shp,path + '\\' + 'temp',tempshpname)
        shp3 = arcpy.Project_management(shp2,path + '\\' + 'temp2' + '\\' + tempshpname.encode('utf-8'),
                                        out_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',"
                                                        "SPHEROID['WGS_1984',6378137.0,298.257223563]]"
                                                        ",PRIMEM['Greenwich',0.0],"
                                                        "UNIT['Degree',0.0174532925199433]]")
        shps.append(shp3)
    arcpy.Merge_management(shps,path + '\\' + 'shp' + '\\' + '{}.shp'.format((shpname)))

extract_FromMDB('HYDA')