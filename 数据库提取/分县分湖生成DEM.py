# coding=utf-8
import arcpy
import pandas
import os
import pinyin
path = r'D:\2021年项目\0607湖泊DEM\湖泊MDB\102'.decode('utf-8')
outpath = r'D:\2021年项目\0607湖泊DEM\a'.decode('utf-8')
mdblst = []
for i,v,m in os.walk(path):
    mdblst = m
for mdb in mdblst:
    arcpy.env.workspace = path
    terlShpName = mdb.encode('utf-8').split('.')[0].replace('-', '')
    b = str(terlShpName).split('段')[0]
    xName = b.decode('utf-8')[-3:].encode('utf-8')
    lakeName = b.decode('utf-8')[0:-3].encode('utf-8')
    arcpy.CreateFolder_management(outpath,xName)
    x_folder = outpath.encode('utf-8') + '\\' + xName
    arcpy.CreateFolder_management(x_folder,lakeName)
    demFolder = x_folder + '\\' + lakeName
    arcpy.CreateFolder_management(demFolder,'DEM')
for mdb in mdblst:
    arcpy.env.workspace = path
    terlShpName = mdb.encode('utf-8').split('.')[0].replace('-', '')
    b = str(terlShpName).split('段')[0]
    xName = b.decode('utf-8')[-3:].encode('utf-8')
    lakeName = b.decode('utf-8')[0:-3].encode('utf-8')
    x_folder = outpath.encode('utf-8') + '\\' + xName
    demFolder = x_folder + '\\' + lakeName
    try:
        b = pinyin.get_initial('{}'.format(terlShpName)).replace(' ','').capitalize()
        arcpy.env.workspace = path.encode('utf-8') + '\\' + mdb.encode('utf-8')
        terlShpName = mdb.encode('utf-8').split('.')[0].replace('-', '')
        # tin = arcpy.CreateTin_3d(in_features='TERL',out_tin=r'D:\2021年项目\0604谢轩德\tin\{}'.format(b),spatial_reference="PROJCS['CGCS2000_3_Degree_GK_CM_99E',GEOGCS['GCS_China_Geodetic_Coordinate_System_2000',"
        #                                      "DATUM['D_China_2000',SPHEROID['CGCS2000',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],"
        #                                      "PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',99.0],"
        #                                      "PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]")        ###99
        tin = arcpy.CreateTin_3d(out_tin=r'D:\2021年项目\0607湖泊DEM\tin\{}'.format(b),
                           spatial_reference="PROJCS['CGCS2000_3_Degree_GK_CM_102E',GEOGCS['GCS_China_Geodetic_Coordinate_System_2000',DATUM['D_China_2000',"
                                             "SPHEROID['CGCS2000',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],"
                                             "PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],"
                                             "PARAMETER['Central_Meridian',102.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]",
                           in_features="TERL ELEV Hard_Line <None>", constrained_delaunay="DELAUNAY")                  #####102
        creatDemFolder = demFolder + '\\' +'DEM\\{}'.format(b)
        arcpy.TinRaster_3d(tin,out_raster= creatDemFolder,sample_distance="CELLSIZE 2", z_factor="1")
        print '{} is done'.format(terlShpName)
    except:
        print '{} is wrong'.format(terlShpName)
###########################################################
# coding=utf-8
import arcpy
import pinyin
arcpy.env.workspace = r'D:\2021年项目\0615DEM'.decode('utf-8')
outpath = r'D:\2021年项目\0615DEM\OK'.decode('utf-8')
tk = 'TKZS-99.shp'
spatial_ref = arcpy.Describe(tk).spatialReference
with arcpy.da.SearchCursor('TKZS-99.shp',['SHAPE@','图名'.decode('utf=8'),'图号'.decode('utf-8')]) as yb:
    for row in yb:
        try:
            lakeName = row[1].encode('utf-8')
            tk = row[2].encode('utf-8')
            demName = pinyin.get_initial('{}'.format(lakeName)).replace(' ', '').capitalize()
            b = str(lakeName).split('段')[0]
            xName = b.decode('utf-8')[-3:].encode('utf-8')
            x_folder = outpath.encode('utf-8') + '\\' + xName
            arcpy.CreateFolder_management(outpath, xName)
            arcpy.CreateFolder_management(x_folder, lakeName)
            demFolder = x_folder + '\\' + lakeName
            arcpy.CreateFolder_management(demFolder, 'DEM')
            dem2Folder = demFolder + '\\' + 'DEM'.encode('utf-8')
            tkFolder = str(lakeName) + str(tk)
            arcpy.CreateFolder_management(dem2Folder, tkFolder)
            dem = r'D:\2021年项目\0615DEM\dem\{}'.format(demName)
            demByTk_dir = dem2Folder + '\\' +tkFolder + '\\' + demName + str(tk)
            arcpy.gp.ExtractByMask_sa(dem,row[0],demByTk_dir)
        except Exception as e:
            print '{} {}'.format(demName,e)