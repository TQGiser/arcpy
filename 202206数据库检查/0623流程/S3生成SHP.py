# coding=utf-8
import arcpy
import pandas as pd
import math
arcpy.env.overwriteOutput = True
path = r'E:\2022年项目\0621甘孜断面\洲际\赠曲'
outpath = path + '\\' + 'shp'
arcpy.env.workspace = path
def txt_shp():
    csv = path + '\\' + 'csv' + '\\' + 'All_FromTXT.csv'
    df = pd.read_csv(csv.decode('utf-8'),encoding='gbk')
    p_cn = []
    for name,value in df.iterrows():
        print 'processing txtshp',name
        cn = [df.loc[name,'x'],df.loc[name,'y'],df.loc[name,'h'],df.loc[name,'河流'.decode('utf-8')]]
        p_cn.append(cn)
    p = arcpy.CreateFeatureclass_management(outpath,'txt_shp','POINT')
    arcpy.AddField_management(p,'elev','TEXT')
    arcpy.AddField_management(p, 'rvname', 'TEXT')
    yb = arcpy.da.InsertCursor(p,['SHAPE@X','SHAPE@Y','elev','rvname'])
    for cn in p_cn:
        yb.insertRow(cn)
    del yb
def mdb_shp():
    csv = path + '\\' + 'csv' + '\\' + 'All_FromMDB.csv'
    df = pd.read_csv(csv.decode('utf-8'),encoding='gbk')
    p_cn = []
    for name,value in df.iterrows():
        print 'processing mdbshp', name
        cn = [df.loc[name,'x'],df.loc[name,'y'],df.loc[name,'h'],df.loc[name,'dmh'],df.loc[name,'dmh2'],df.loc[name,'Name']]
        p_cn.append(cn)
    p = arcpy.CreateFeatureclass_management(outpath,'mdb_shp','POINT')
    arcpy.AddField_management(p,'elev','TEXT')
    arcpy.AddField_management(p, 'dmh', 'TEXT')
    arcpy.AddField_management(p, 'dmh2', 'TEXT')
    arcpy.AddField_management(p, 'MDBName', 'TEXT')
    yb = arcpy.da.InsertCursor(p,['SHAPE@X','SHAPE@Y','elev','dmh','dmh2','MDBName'])
    for cn in p_cn:
        yb.insertRow(cn)
    del yb
txt_shp()
# mdb_shp()