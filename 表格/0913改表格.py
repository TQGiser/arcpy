#coding=utf-8
import arcpy
import pandas as pd
import math
import os
import random
pd.set_option('display.width',500)
path = r'D:\2021年项目\0915江北改表格\xls加告示牌标题'
from openpyxl import load_workbook
from openpyxl.styles import Border,Side,colors,Alignment,Font
wb = load_workbook(r'D:\2021年项目\0915江北改表格\xls加告示牌标题\雅江县白龙柯.xlsx'.decode('utf-8'))
ws = wb.worksheets[0]
for row in ws.rows:
    if row[8].value == '实体桩'.decode('utf-8'):
        Rvx = (random.randint(0, 200)) / 1000.0
        Rvy = (random.randint(0, 200)) / 1000.0
        Rvh = (random.randint(0, 400)) / 1000.0

#coding=utf-8
import arcpy
import pandas as pd
import math
import os
import random
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
def cal_M_AB(x,y,zx):
    px_lst = []
    a = 0
    for a in range(0, len(zx)):
        dis = (math.sqrt((x - zx[a][0]) ** 2 + (y - zx[a][1]) ** 2))
        m = zx[a][2]
        px_p = [dis, m, zx[a][0], zx[a][1]]
        px_lst.append(px_p)
    cn_sort = sorted(px_lst, key=lambda s: s[0])
    x1 = cn_sort[0][2]
    y1 = cn_sort[0][3]
    x2 = cn_sort[1][2]
    y2 = cn_sort[1][3]
    x1_m = cn_sort[0][1]
    x2_m = cn_sort[1][1]
    if x1_m < x2_m:
        d = (y1 - y2) * x + (x2 - x1) * y + x1 * y2 - x2 * y1
    elif x1_m > x2_m:
        d = (y2 - y1) * x + (x1 - x2) * y + x2 * y1 - x1 * y2
    if d < 0:
        ab = '左岸'
    elif d > 0:
        ab = '右岸'
    czx = ((x - x1) * (x1 - x2) + (y - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (x1 - x2) + x1
    czy = ((x - x1) * (x1 - x2) + (y - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (y1 - y2) + y1
    np_m = x1_m - math.sqrt((czx - x1) ** 2 + (czy - y1) ** 2)
    return np_m,ab,czx,czy
def cal_xy_byM(m,zxcn_lst):
    newZxList= []
    for cn in zxcn_lst:
        dis = cn[2] - m
        cn1 = [cn[0],cn[1],dis]
        newZxList.append(cn1)
    a = [cn for cn in newZxList if cn[2] <0][-1]
    b = [cn for cn in newZxList if cn[2] >0][0]
    x1 = a[0]
    y1 = a[1]
    s1 = abs(a[2])
    x2 = b[0]
    y2 = b[1]
    s2 = abs(b[2])
    s3 = s1 + s2
    x0 = (s1*(x2-x1) + s3*x1)/s3
    y0 = (s1*(y2-y1) + s3*y1)/s3
    return x0,y0
def creatPoint(p_cn):
    point = arcpy.Point()
    pointList = []
    for p in p_cn:
        point.X = p[0]
        point.Y = p[1]
        pg = arcpy.PointGeometry(point)
        pointList.append(pg)
        arcpy.CopyFeatures_management(pointList, r'D:\Test\np.shp')
def cal_foot(x0,y0,x1,y1,x2,y2):
    czx = ((x0 - x1) * (x1 - x2) + (y0 - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (x1 - x2) + x1
    czy = ((x0 - x1) * (x1 - x2) + (y0 - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (y1 - y2) + y1
    return czx,czy
pd.set_option('display.width',500)
path = r'D:\2021年项目\0913州河数据库'
df = pd.read_excel(r'D:\2021年项目\0913州河数据库\丁曲表格\改电子桩.xlsx'.decode('utf-8'))
zx = listFile(path,'中线'.decode('utf-8'),'x')
zxcn_lst = []
with arcpy.da.SearchCursor(zx,['OID@','SHAPE@X','SHAPE@Y','SHAPE@M'],explode_to_points = True) as yb:
    for row in yb:
        cn = [row[1],row[2],row[3]]
        zxcn_lst.append(cn)
cnList = []
for name,value in df.iterrows():
    if value['bz'] == '实体桩'.decode('utf-8'):
        x0 = value['x']
        y0 = value['y']
        Rvx = (random.randint(0, 200)) / 1000.0
        Rvy = (random.randint(0, 200)) / 1000.0
        x1 = cal_M_AB(x0, y0, zxcn_lst)[2]
        y1 = cal_M_AB(x0, y0, zxcn_lst)[3]
        if x0 < x1 and y0 < y1:
            x3 = x0 - Rvx
            y3 = y0 - Rvy
        elif x0 < x1 and y0 > y1:
            x3 = x0 - Rvx
            y3 = y0 + Rvy
        elif x0 > x1 and y0 > y1:
            x3 = x0 + Rvx
            y3 = y0 + Rvy
        elif x0 > x1 and y0 < y1:
            x3 = x0 + Rvx
            y3 = y0 - Rvy
        df.loc[name,'x'] = x3
        df.loc[name, 'y'] = y3
df.to_excel(r'D:\2021年项目\0913州河数据库\丁曲表格\改实体桩.xlsx'.decode('utf-8'),index=False)
path = r'D:\2021年项目\0917江北图册'
df = pd.read_excel(path.decode('utf-8') + '\\' + '1111.xlsx'.decode('utf-8'),sheetname='Sheet2')


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
for name,value in df.iterrows():
    x = df.loc[name,'xg']
    y = df.loc[name,'yg']
    e = 'E' + '%0.8f'%round(XY2LatLon(x,y,102)[1],8) + '°'.decode('utf-8')
    n = 'N' + '%0.8f' % round(XY2LatLon(x, y,102)[0], 8) + '°'.decode('utf-8')
    print df.loc[name,'name'],e,n