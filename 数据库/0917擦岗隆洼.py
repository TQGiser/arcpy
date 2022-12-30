#coding=utf-8
import arcpy
import pandas as pd
import math
import os
def listFiles_Mdb(path,type):
    shps = []
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
                shps.append(shp)
            elif a == 'DMAL':
                shp = os.path.join(path, a)
                shps.append(shp)
            elif a == 'DMAA':
                shp = os.path.join(path, a)
                shps.append(shp)
    return shps
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
path = r'D:\2021年项目\0915改擦岗隆洼表格'
shps = listFiles_Mdb(path,'d')
cnList = []
# for shp in shps:
#     with arcpy.da.SearchCursor(shp,['NAME','SHAPE@X','SHAPE@Y','ELEV','NUM','GB','RuleID']) as yb:
#         for row in yb:
#             cn = [row[0].encode('utf-8'), row[1], row[2], row[3], row[4].encode('utf-8'),row[5],row[6]]
#             print str(cn).decode('string_escape')
#             cnList.append(cn)
for shp in shps:
    with arcpy.da.SearchCursor(shp,['NAME',]) as yb:
        for row in yb:
            cn = [row[0].encode('utf-8'), row[1], row[2], row[3], row[4].encode('utf-8'),row[5],row[6]]
            print str(cn).decode('string_escape')
            cnList.append(cn)
# df = pd.read_excel(r'D:\2021年项目\0915改擦岗隆洼表格\数据库坐标.xlsx'.decode('utf-8'),sheetname='ys')
# cnList = []
# for name,value in df.iterrows():
#     x = df.loc[name,'xys']
#     y = df.loc[name,'yys']
#     e = 'E' + '%0.8f'%round(XY2LatLon(x,y,99)[1],8) + '°'.decode('utf-8')
#     n = 'N' + '%0.8f' % round(XY2LatLon(x,y,99)[0], 8) + '°'.decode('utf-8')
#     Name = df.loc[name,'name']
#     print Name,e,n
    # cn = [df.loc[name,'name'],'%0.4f'%round(df.loc[name,'x'],4),'%0.4f'%round(df.loc[name,'y'],4),'%0.2f'%round(df.loc[name,'h'],2),df.loc[name,'lc']]
    # cnList.append(cn)
# dwg2k = r'D:\2021年项目\0915改擦岗隆洼表格\dwg\2K.dwg\Annotation'
# dwg1w = r'D:\2021年项目\0915改擦岗隆洼表格\dwg\1W.dwg\Annotation'
# with arcpy.da.UpdateCursor(dwg2k,'Text') as yb:
#     for row in yb:
#         for cn in cnList:
#             if cn[0] in row[0]:
#                 x = 'X:{}'.format(cn[1])
#                 y = 'Y:{}'.format(cn[2])
#                 h = 'H:{}'.format(cn[3])
#                 lc = '里程:{}'.format(cn[4])
#                 new = row[0].split(' ')[0] + ' ' + x + ' ' + y + ' ' + h + ' ' + lc.decode('utf-8')
#                 row[0] =  new
#                 yb.updateRow(row)