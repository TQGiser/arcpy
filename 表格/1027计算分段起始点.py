# coding=utf-8
import arcpy
import os
import math
import json
import pinyin
path = r'E:\2021年项目\1027分段点程序\bt'
arcpy.env.worksapce = path
arcpy.env.overwriteOutput = True
def listFile(path, keyword, type):
    arcpy.env.workspace = path
    if type == 'd':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Point')
    elif type == 'x':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Polyline')
    elif type == 'm':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Polygon')
    for path, name, file in walk:
        for a in file:
            if keyword in a:
                shp = os.path.join(path, a)
    return shp
def XY2LatLon(X, Y, L0):
    iPI = 0.0174532925199433
    a = 6378137.0
    f= 0.003352810693716
    ProjNo = int(X / 1000000)
    L0 = L0 * iPI
    X0 = ProjNo * 1000000 + 500000
    Y0 = 0
    xval = X - X0
    yval = Y - Y0
    e2 = 2 * f - f * f #第一偏心率平方
    e1 = (1.0 - math.sqrt(1 - e2)) / (1.0 + math.sqrt(1 - e2))
    ee = e2 / (1 - e2) #第二偏心率平方
    M = yval
    u = M / (a * (1 - e2 / 4 - 3 * e2 * e2 / 64 - 5 * e2 * e2 * e2 / 256))
    fai = u \
          + (3 * e1 / 2 - 27 * e1 * e1 * e1 / 32) * math.sin(2 * u) \
          + (21 * e1 * e1 / 16 - 55 * e1 * e1 * e1 * e1 / 32) * math.sin(4 * u) \
          + (151 * e1 * e1 * e1 / 96) * math.sin(6 * u)\
          + (1097 * e1 * e1 * e1 * e1 / 512) * math.sin(8 * u)
    C = ee * math.cos(fai) * math.cos(fai)
    T = math.tan(fai) * math.tan(fai)
    NN = a / math.sqrt(1.0 - e2 * math.sin(fai) * math.sin(fai))
    R = a * (1 - e2) / math.sqrt(
        (1 - e2 * math.sin(fai) * math.sin(fai)) * (1 - e2 * math.sin(fai) * math.sin(fai)) * (1 - e2 * math.sin(fai) * math.sin(fai)))
    D = xval / NN
    longitude1 = L0 + (D - (1 + 2 * T + C) * D * D * D / 6 + (
    5 - 2 * C + 28 * T - 3 * C * C + 8 * ee + 24 * T * T) * D * D * D * D * D / 120) / math.cos(fai)
    latitude1 = fai - (NN * math.tan(fai) / R) * (
    D * D / 2 - (5 + 3 * T + 10 * C - 4 * C * C - 9 * ee) * D * D * D * D / 24 + (
    61 + 90 * T + 298 * C + 45 * T * T - 256 * ee - 3 * C * C) * D * D * D * D * D * D / 720)
    longitude = longitude1 / iPI
    latitude = latitude1 / iPI
    return latitude, longitude
lqd = listFile(path,'2000','x')
ywd = listFile(path,'10000','x')
pList = []
with arcpy.da.SearchCursor(lqd,['SHAPE@','河流']) as yb:
    for row in yb:
        qd= [row[1],'2K起点',row[0].firstPoint.X,row[0].firstPoint.Y,
             'E' + str('%.8f'%round(XY2LatLon(row[0].firstPoint.X,row[0].firstPoint.Y,99)[1],8)) + '°'.decode('utf-8'),
             'N' + str('%.8f'%round(XY2LatLon(row[0].firstPoint.X,row[0].firstPoint.Y,99)[0],8)) + '°'.decode('utf-8'),
             '%0.4f' % round(row[0].firstPoint.Y, 4),
             '%0.4f' % round(row[0].firstPoint.X, 4)]
        zd= [row[1],'2K终点',row[0].lastPoint.X,row[0].lastPoint.Y,
             'E' + str('%.8f'%round(XY2LatLon(row[0].lastPoint.X,row[0].lastPoint.Y,99)[1],8)) + '°'.decode('utf-8'),
             'N' + str('%.8f'%round(XY2LatLon(row[0].lastPoint.X,row[0].lastPoint.Y,99)[0],8)) + '°'.decode('utf-8'),
             '%0.4f' % round(row[0].firstPoint.Y, 4),
             '%0.4f' % round(row[0].firstPoint.X, 4)]
        pList.append(qd)
        pList.append(zd)
with arcpy.da.SearchCursor(ywd,['SHAPE@','河流']) as yb:
    for row in yb:
        qd= [row[1],'1W起点',row[0].firstPoint.X,row[0].firstPoint.Y,
             'E' + str('%.8f'%round(XY2LatLon(row[0].firstPoint.X,row[0].firstPoint.Y,99)[1],8)) + '°'.decode('utf-8'),
             'N' + str('%.8f'%round(XY2LatLon(row[0].firstPoint.X,row[0].firstPoint.Y,99)[0],8)) + '°'.decode('utf-8'),
             '%0.4f'%round(row[0].firstPoint.Y,4),
             '%0.4f' % round(row[0].firstPoint.X, 4)]
        zd= [row[1],'1W终点',row[0].lastPoint.X,row[0].lastPoint.Y,
             'E' + str('%.8f'%round(XY2LatLon(row[0].lastPoint.X,row[0].lastPoint.Y,99)[1],8)) + '°'.decode('utf-8'),
             'N' + str('%.8f'%round(XY2LatLon(row[0].lastPoint.X,row[0].lastPoint.Y,99)[0],8)) + '°'.decode('utf-8'),
             '%0.4f'%round(row[0].lastPoint.Y,4),
             '%0.4f'%round(row[0].lastPoint.X,4)]
        pList.append(qd)
        pList.append(zd)
p = arcpy.CreateFeatureclass_management(path,'a','POINT')
arcpy.AddField_management(p,'NAME','TEXT')
arcpy.AddField_management(p,'QZ','TEXT')
arcpy.AddField_management(p,'Y','TEXT')
arcpy.AddField_management(p,'X','TEXT')
arcpy.AddField_management(p,'E','TEXT')
arcpy.AddField_management(p,'N','TEXT')
yb = arcpy.da.InsertCursor(p,['NAME','QZ','SHAPE@X','SHAPE@Y','E','N','X','Y'])
for cn in pList:
    yb.insertRow(cn)
del yb
