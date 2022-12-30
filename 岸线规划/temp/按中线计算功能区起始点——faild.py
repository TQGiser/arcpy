# coding=utf-8
import arcpy
import pandas as pd
import math
pd.set_option('display.width',100)
path = r'E:\Test'
arcpy.env.workspace = path
def LatLon2XY(latitude, longitude):
    a = 6378137.0
    e2 = 0.0066943799013
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
        4 * latitude2Rad) - 0.022373 * math.sin(6 * latitude2Rad)
    N = a / math.sqrt(1 - et3)
    x = X + N * t * (0.5 * pow(m, 2) + (5.0 - pow(t, 2) + 9.0 * et2 + 4 * pow(et2, 2)) * pow(m, 4) / 24.0 + (
    61.0 - 58.0 * pow(t, 2) + pow(t, 4)) * pow(m, 6) / 720.0)
    y = 500000 + N * (m + (1.0 - pow(t, 2) + et2) * pow(m, 3) / 6.0 + (
    5.0 - 18.0 * pow(t, 2) + pow(t, 4) + 14.0 * et2 - 58.0 * et2 * pow(t, 2)) * pow(m, 5) / 120.0)
    return x, y
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
aera_walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass",type='Polygon')
dmal_zx_walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass",type='Polyline')
for path,name,file in aera_walk:
    glqAera= file[0]
for path,name,file in dmal_zx_walk:
    for shp in file:
        if 'DMAL' in shp:
            dmal = shp
        elif '中线'.decode('utf-8') in shp:
            zx = shp
spatial_ref = arcpy.Describe(dmal).spatialReference
if '99' in spatial_ref.name:
    xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-99.shp'
    fdh = 99
elif '102' in spatial_ref:
    xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-102.shp'
    fdh = 102
cn_lst = []
with arcpy.da.SearchCursor(dmal,['SHAPE@','RIVER']) as dmals:
    for line in dmals:
        with arcpy.da.SearchCursor(glqAera, ['SHAPE@', 'Name','FID']) as aeras:
            for aera in aeras:
                for part in aera[0]:
                    for pnt in part:
                        if line[0]. contains(pnt):
                            # print type(aera[1].encode('utf-8'))
                            # print aera[1].encode('utf-8')
                            # break
                            cn = [pnt.X,pnt.Y,aera[1].encode('utf-8'),aera[2]]
                            if cn not in cn_lst:
                                cn_lst.append(cn)
zxcn_lst = []
with arcpy.da.SearchCursor(zx,['OID@','SHAPE@X','SHAPE@Y','SHAPE@M'],explode_to_points = True) as yb:
    i = 0
    for row in yb:
        cn = [row[1],row[2],row[3]]
        zxcn_lst.append(cn)
groups = max([cn[3] for cn in cn_lst])
pnt_df = []
i = 0
for i in range(0,groups + 1):
    for cn in cn_lst:
        if cn[3] == i:
            x3 = cn[0]
            y3 = cn[1]
            name = cn[2]
            id = cn[3]
            px_lst = []
            a = 0
            for a in range(0,len(zxcn_lst)):
                dis = (math.sqrt((x3-zxcn_lst[a][0])**2 + (y3 - zxcn_lst[a][1])**2))
                m = zxcn_lst[a][2]
                px_p = [dis, m, zxcn_lst[a][0], zxcn_lst[a][1]]
                px_lst.append(px_p)
            cn_sort = sorted(px_lst, key=lambda s: s[0])
            x1 = cn_sort[0][2]
            y1 = cn_sort[0][3]
            x2 = cn_sort[1][2]
            y2 = cn_sort[1][3]
            x1_m = cn_sort[0][1]
            x2_m = cn_sort[1][1]
            if x1_m < x2_m:
                d = (y1 - y2) * x3 + (x2 - x1) * y3 + x1 * y2 - x2 * y1
            elif x1_m > x2_m:
                d = (y2 - y1) * x3 + (x1 - x2) * y3 + x2 * y1 - x1 * y2
            if d < 0:
                ab = 0
            elif d > 0:
                ab = 1
            czx = ((x3 - x1) * (x1 - x2) + (y3 - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (x1 - x2) + x1
            czy = ((x3 - x1) * (x1 - x2) + (y3 - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (y1 - y2) + y1
            np_m = x1_m + math.sqrt((czx - x1) ** 2 + (czy - y2) ** 2)
            # print np_m,i,name,id,round(x3,4),round(y3),round(XY2LatLon(x3,y3,99)[1],8),round(XY2LatLon(x3,y3,99)[1],8)
            np = [name,id,np_m,ab,round(y3,4),round(x3,4),round(XY2LatLon(x3,y3,fdh)[1],8),round(XY2LatLon(x3,y3,fdh)[1],8),czx,czy,x1_m]
            pnt_df.append(np)
    i +=1
# df = pd.DataFrame(columns=['序号','市(地)级行政区','县级行政区','编号','岸别','功能区类型',
#                            '长度(km)','起点坐标(经度)','起点坐标(纬度)','终点坐标(经度)',
#                            '终点坐标(纬度)','主要划分依据','备注'])
df = pd.DataFrame(pnt_df,columns=['功能区类型','编号','长度(km)','岸别','Y','X','E','N','czx','czy','x1_m'])
df.to_excel(r'C:\Users\Administrator\Desktop\1.xlsx',index = False)




