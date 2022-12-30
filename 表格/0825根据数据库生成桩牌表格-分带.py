# coding=utf-8
import arcpy
import pandas as pd
import math
import os
path = r'D:\Test'
def listFile_Mdb(path,type):
    if type == 'd':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Point')
    elif type == 'x':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Polyline')
    elif type == 'm':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Polygon')
    for path, name, file in walk:
        for a in file:
            if a == 'DMAP':
                shp = os.path.join(path, a)
            elif a == 'DMAL':
                shp = os.path.join(path, a)
            elif a == 'DMAA':
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
def LatLon2XY(latitude, longitude):
    a = 6378137.0
    e2 = 0.0066943999013
    latitude2Rad = (math.pi / 180.0) * latitude
    beltNo = int((longitude + 1.5) / 3.0) #计算3度带投影度带号
    L = beltNo * 3 #计算中央经线
    l0 = longitude - L #经差
    tsin = math.sin(latitude2Rad)
    tcos = math.cos(latitude2Rad)
    t = math.tan(latitude2Rad)
    m = (math.pi / 180.0) * l0 * tcos
    et2 = e2 * pow(tcos, 2)
    et3 = e2 * pow(tsin, 2)
    X = 111132.9558 * latitude - 16038.6496 * math.sin(2 * latitude2Rad) + 16.8610 * math.sin(
        4 * latitude2Rad) - 0.022333 * math.sin(6 * latitude2Rad)
    N = a / math.sqrt(1 - et3)
    x = X + N * t * (0.5 * pow(m, 2) + (5.0 - pow(t, 2) + 9.0 * et2 + 4 * pow(et2, 2)) * pow(m, 4) / 24.0 + (
    61.0 - 58.0 * pow(t, 2) + pow(t, 4)) * pow(m, 6) / 720.0)
    y = 500000 + N * (m + (1.0 - pow(t, 2) + et2) * pow(m, 3) / 6.0 + (
    5.0 - 18.0 * pow(t, 2) + pow(t, 4) + 14.0 * et2 - 58.0 * et2 * pow(t, 2)) * pow(m, 5) / 120.0)
    return x, y
p = listFile_Mdb(path,'d')
l = listFile_Mdb(path,'x')
cnLst = []
with arcpy.da.SearchCursor(p,['NAME','NUM','COUNTY','TOWN','SHAPE@X','SHAPE@Y','ELEV','RuleID','SHAPE@','BANK']) as yb :
    for row in yb:
        name = row[0]
        lc = row[1]
        xzq = row[2] + row[3]
        e1 = XY2LatLon(row[4], row[5], 99)[1]
        n1 = XY2LatLon(row[4], row[5], 99)[0]
        e = round(XY2LatLon(row[4],row[5],99)[1],8)
        n = round(XY2LatLon(row[4],row[5],99)[0],8)                                                                     #带号选择99或102
        if e > 100.5:
            x = LatLon2XY(n1,e1)[0]
            y = LatLon2XY(n1,e1)[1]
        elif e < 100.5:
            x = round(row[5],4)
            y = round(row[4],4)
        h = round(row[6],2)
        if row[7] == 27:
            bz = '电子桩'
        elif row[7] == 2:
            bz = '实体桩'
        elif row[7] == 3:
            bz = '实体桩(移位桩)'
        elif row[7] == 4:
            bz = '告示牌'
        with arcpy.da.SearchCursor(l, 'SHAPE@') as dmals:
                for line in dmals:
                    if line[0].contains(row[8]):
                        jc = 'Y'
                        break
                    jc = 'N'
        cn = [name,lc,xzq,e,n,x,y,h,bz,jc]
        cnLst.append(cn)
df = pd.DataFrame(cnLst,columns=['桩名（编号）','里程','所在位置（地名）','经度','纬度','X','Y','高程（1985国家高程基准）','备注','检查'])
df.to_excel(r'D:\Test\1.xlsx',index=False)