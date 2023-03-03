#coding=utf-8
import arcpy
import os
from os.path import join,getsize
import pandas as pd

df = pd.read_excel(r'E:\数据部数据\数据整合\成果目录-3D产品.xlsx'.decode('utf-8'))
arcpy.env.overwriteOutput=True
path = r'E:\数据部数据\数据整合\DLG\MDB\河湖划界'.decode('utf-8')
mdbPathList = []
for i,v,m in os.walk(path):
    for f in m :
        mdb = os.path.join(i,f)
        mdbPath = '\\'.join(mdb.split('\\',8)[0:8])
        if mdbPath not in mdbPathList:
            mdbPathList.append(mdbPath)
for mdbPath in mdbPathList:
    print mdbPath
    P,P0,P1,P2,GS,XMLX,XMMC,CS = mdbPath.split('\\',8)
    V = 0
    for i, v, m in os.walk(mdbPath, topdown=True):
        V += sum([getsize(join(i, name)) for name in m])
    if V >0 and V<1024: 
        SJRL = '0.1KB'
    elif V>1024 and V<1048576:
        SJRL = str(round(V/1024.0,2)) + 'KB'
    elif V >1048576 and V<1073741824:
        SJRL= str(round(V/1024.0/1024.0,2)) + 'MB'
    elif V >1073741824 :
        SJRL= str(round(V/1024.0/1024.0/1024.0,2)) + 'GB'
    print SJRL
    for name, value in df.iterrows():
        if XMMC in df.loc[name,'项目名称'.decode('utf-8')]:
            SX = (df.loc[name,'时相'.decode('utf-8')])
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
        boua = mdbPath + '\\' + mdb + '\\' + 'DLG' + '\\' + 'HYDA'
        bouas.append(boua)
    sf = arcpy.Describe(DLG).spatialReference
    ZBX = sf.PCSCode
    aL = arcpy.CreateFeatureclass_management(mdbPath, 'temp.shp', 'POLYGON')
    cs = arcpy.da.InsertCursor(aL, 'SHAPE@')
    for boua in bouas:
        with arcpy.da.SearchCursor(boua, 'SHAPE@') as yb2:
            for row2 in yb2:
                cs.insertRow(row2)
    Shp = arcpy.Dissolve_management(aL, mdbPath + '\\' + 'HYDA.shp')
    arcpy.Delete_management(aL)
    arcpy.DefineProjection_management(Shp,coor_system=sf)
    Shp84 = arcpy.Project_management(Shp,mdbPath + '\\' + 'HYDA-84.shp',out_coor_system="GEOGCS['GCS_China_Geodetic_Coordinate_System_2000',DATUM['D_China_2000',"
                                                               "SPHEROID['CGCS2000',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],"
                                                               "UNIT['Degree',0.0174532925199433]]")
    arcpy.Delete_management(Shp)
    print GS,XMLX,XMMC,CS,SJRL,SX,ZBX
    arcpy.AddField_management(Shp84,'GS','TEXT')
    arcpy.AddField_management(Shp84, 'XMLX', 'TEXT')
    arcpy.AddField_management(Shp84, 'XMMC', 'TEXT')
    arcpy.AddField_management(Shp84, 'CS', 'TEXT')
    arcpy.AddField_management(Shp84, 'SJRL', 'TEXT')
    arcpy.AddField_management(Shp84, 'SX', 'TEXT')
    arcpy.AddField_management(Shp84, 'ZBX', 'TEXT')
    with arcpy.da.UpdateCursor(Shp84,['GS','XMLX','XMMC','CS','SJRL','SX','ZBX']) as yb:
        for row in yb:
            row[0] = GS
            row[1] = XMLX
            row[2]= XMMC
            row[3] = CS
            row[4] = SJRL
            row[5] = SX
            row[6] = ZBX
            yb.updateRow(row)
    print '%s is done'%mdbPath