# coding=utf-8
import arcpy
import pandas as pd
arcpy.env.overwriteOutput = True
path = r'E:\2022年项目\0621甘孜断面\白玉\temp'
arcpy.env.workspace = path
def txt_shp():
    xlsx = path + '\\' + 'txt.xlsx'
    df = pd.read_excel(xlsx.decode('utf-8'))
    p_cn = []
    for name,value in df.iterrows():
        cn = [df.loc[name,'x'],df.loc[name,'y'],df.loc[name,'p_name'],df.loc[name,'h']]
        p_cn.append(cn)
    p = arcpy.CreateFeatureclass_management(path,'txt_shp','POINT')
    arcpy.AddField_management(p,'p_name','TEXT')
    arcpy.AddField_management(p,'elev','TEXT')
    yb = arcpy.da.InsertCursor(p,['SHAPE@X','SHAPE@Y','p_name','elev'])
    for cn in p_cn:
        yb.insertRow(cn)
    del yb
def mdb_shp():
    xlsx = path + '\\' + 'mdb.xlsx'
    df = pd.read_excel(xlsx.decode('utf-8'))
    p_cn = []
    for name,value in df.iterrows():
        cn = [df.loc[name,'x'],df.loc[name,'y'],df.loc[name,'p_name'],df.loc[name,'h']]
        p_cn.append(cn)
    p = arcpy.CreateFeatureclass_management(path,'mdb_shp','POINT')
    arcpy.AddField_management(p,'p_name','TEXT')
    arcpy.AddField_management(p,'elev','TEXT')
    yb = arcpy.da.InsertCursor(p,['SHAPE@X','SHAPE@Y','p_name','elev'])
    for cn in p_cn:
        yb.insertRow(cn)
    del yb
txt_shp()
# mdb_shp()