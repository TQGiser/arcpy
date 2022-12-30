#coding=utf-8
import arcpy
import os
from os.path import join,getsize
import pandas as pd

df = pd.read_excel(r'E:\数据整合\成果目录-3D产品.xlsx'.decode('utf-8'))
arcpy.env.overwriteOutput=True
path = r'E:\数据整合\DLG\MDB\河湖划界'.decode('utf-8')
mdbPathList = []
for i,v,m in os.walk(path):
    for f in m :
        mdb = os.path.join(i,f)
        mdbPath = '\\'.join(mdb.split('\\',7)[0:7])
        if mdbPath not in mdbPathList:
            mdbPathList.append(mdbPath)
for mdbPath in mdbPathList:
    print mdbPath
    XMMC= mdbPath.split('\\',7)[5]
    print XMMC
    arcpy.env.workspace = mdbPath
    mdbs = arcpy.ListFiles('*.mdb')
    for mdb in mdbs:
        DLG = mdbPath + '\\' + mdb + '\\' + 'DLG'
    sf = arcpy.Describe(DLG).spatialReference
    arcpy.env.workspace = mdbPath
    mdbs = arcpy.ListFiles('*.mdb')
    bouas = []
    for mdb in mdbs:
        DLG = mdbPath + '\\' + mdb + '\\' + 'DLG'
        boua = mdbPath + '\\' + mdb + '\\' + 'DLG' + '\\' + 'DMAP'
        bouas.append(boua)
    sf = arcpy.Describe(DLG).spatialReference
    ZBX = sf.PCSCode
    aL = arcpy.CreateFeatureclass_management(mdbPath, 'temp.shp', 'POINT')
    cs = arcpy.da.InsertCursor(aL, 'SHAPE@')
    for boua in bouas:
        with arcpy.da.SearchCursor(boua, 'SHAPE@') as yb2:
            for row2 in yb2:
                cs.insertRow(row2)
    Shp = arcpy.Dissolve_management(aL, mdbPath + '\\' + 'DMAP.shp')
    arcpy.Delete_management(aL)
    arcpy.DefineProjection_management(Shp,coor_system=sf)
    Shp84 = arcpy.Project_management(Shp,mdbPath + '\\' + 'DMAP-84.shp',out_coor_system="GEOGCS['GCS_China_Geodetic_Coordinate_System_2000',DATUM['D_China_2000',"
                                                               "SPHEROID['CGCS2000',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],"
                                                               "UNIT['Degree',0.0174532925199433]]")
    arcpy.Delete_management(Shp)
    arcpy.AddField_management(Shp84, 'XMMC', 'TEXT')
    with arcpy.da.UpdateCursor(Shp84,'XMMC') as yb:
        for row in yb:
            row[0]= XMMC
            yb.updateRow(row)
    print '%s is done'%mdbPath