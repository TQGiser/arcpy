#coding=utf-8
import arcpy
import pythonaddins
import math
import pandas as pd
import os
import time
def listFile(path, keyword, type):
    arcpy.env.workspace = path
    if type == 'd':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Point')
    elif type == 'x':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Polyline')
    elif type == 'm':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Polygon')
    shps = []
    for path, name, file in walk:
        for a in file:
            if keyword in a:
                shp = os.path.join(path, a)
                shps.append(shp)
    if len(shps) == 0:
        return None
    else:
        return shps[0]
def XY2LatLon(X, Y, L0):
    iPI = 0.0174532925199433
    a = 6378137.0
    f = 0.003352810693716
    ProjNo = int(X / 1000000)
    L0 = L0 * iPI
    X0 = ProjNo * 1000000 + 500000
    Y0 = 0
    xval = X - X0
    yval = Y - Y0
    e2 = 2 * f - f * f  # 第一偏心率平方
    e1 = (1.0 - math.sqrt(1 - e2)) / (1.0 + math.sqrt(1 - e2))
    ee = e2 / (1 - e2)  # 第二偏心率平方
    M = yval
    u = M / (a * (1 - e2 / 4 - 3 * e2 * e2 / 64 - 5 * e2 * e2 * e2 / 256))
    fai = u \
          + (3 * e1 / 2 - 27 * e1 * e1 * e1 / 32) * math.sin(2 * u) \
          + (21 * e1 * e1 / 16 - 55 * e1 * e1 * e1 * e1 / 32) * math.sin(4 * u) \
          + (151 * e1 * e1 * e1 / 96) * math.sin(6 * u) \
          + (1097 * e1 * e1 * e1 * e1 / 512) * math.sin(8 * u)
    C = ee * math.cos(fai) * math.cos(fai)
    T = math.tan(fai) * math.tan(fai)
    NN = a / math.sqrt(1.0 - e2 * math.sin(fai) * math.sin(fai))
    R = a * (1 - e2) / math.sqrt(
        (1 - e2 * math.sin(fai) * math.sin(fai)) * (1 - e2 * math.sin(fai) * math.sin(fai)) * (
                1 - e2 * math.sin(fai) * math.sin(fai)))
    D = xval / NN
    longitude1 = L0 + (D - (1 + 2 * T + C) * D * D * D / 6 + (
            5 - 2 * C + 28 * T - 3 * C * C + 8 * ee + 24 * T * T) * D * D * D * D * D / 120) / math.cos(fai)
    latitude1 = fai - (NN * math.tan(fai) / R) * (
            D * D / 2 - (5 + 3 * T + 10 * C - 4 * C * C - 9 * ee) * D * D * D * D / 24 + (
            61 + 90 * T + 298 * C + 45 * T * T - 256 * ee - 3 * C * C) * D * D * D * D * D * D / 720)
    longitude = longitude1 / iPI
    latitude = latitude1 / iPI
    return latitude, longitude
def cal_M_AB(x, y, zx):
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
    np_m = x1_m + math.sqrt((czx - x1) ** 2 + (czy - y2) ** 2)
    return np_m, ab
class River:
    path = ''
    zx = ''
    name = ''
    glq = ''
    dmal = ''
    dmal2 = ''
class ButtonClass1(object):
    """Implementation for Addin1229_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        River.glq  = pythonaddins.OpenDialog('选择功能区'.decode('utf-8'))
        River.path = arcpy.Describe(River.glq).path
        River.dmal = listFile(River.path,'管理范围线'.decode('utf-8'),'x')
        River.dmal2 = listFile(River.path,'水位线'.decode('utf-8'),'x')
        River.zx = listFile(River.path,'校正后中线'.decode('utf-8'),'x')
        River.name = arcpy.Describe(River.glq).baseName.replace('功能区'.decode('utf-8'),'')
class ButtonClass2(object):
    """Implementation for Addin1229_addin.button_1 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        path = River.path
        riverName = River.name
        arcpy.env.workspace = River.path
        spatial_ref = arcpy.Describe(River.glq).spatialReference
        if '99' in spatial_ref.name:
            xzjx = (River.path).encode('utf-8') + '\\' + '甘孜乡镇界带县名-99.shp'
            fdh = 99
        elif '102' in spatial_ref.name:
            xzjx = (River.path).encode('utf-8') + '\\' + '甘孜乡镇界带县名-102.shp'
            fdh = 102
        try:
            arcpy.AddField_management(River.glq, 'province', 'TEXT')
            arcpy.AddField_management(River.glq, 'city', 'TEXT')
            arcpy.AddField_management(River.glq, 'county', 'TEXT')
        except:
            pass
        with arcpy.da.UpdateCursor(River.glq, ['SHAPE@', 'province', 'city', 'county']) as yb1:
            with pythonaddins.ProgressDialog as dialog:
                dialog.title = "处理功能区".decode('utf-8')
                dialog.description = "功能区区域判别".decode('utf-8')
                dialog.animation = "Spiral"
                for i in xrange(100):
                    dialog.progress = i
                    time.sleep(0.125)
                    for row1 in yb1:
                        with arcpy.da.SearchCursor(xzjx, ['SHAPE@', 'XZQMC_1', 'XZQMC']) as yb2:
                            qxList = []
                            for row2 in yb2:
                                if row2[0].overlaps(row1[0]):
                                    qx = row2[1] + row2[2]
                                    qxList.append(qx)
                                elif row2[0].contains(row1[0]):
                                    qx = row2[1] + row2[2]
                                    qxList.append(qx)
                        row1[1] = '四川省'
                        row1[2] = '甘孜藏族自治州'
                        row1[3] = "、".decode('utf-8').join(qxList)
                        yb1.updateRow(row1)
        zxcn_lst = []
        with arcpy.da.SearchCursor(River.zx, ['OID@', 'SHAPE@X', 'SHAPE@Y', 'SHAPE@M'], explode_to_points=True) as yb:
            for row in yb:
                cn = [row[1], row[2], row[3]]
                zxcn_lst.append(cn)
        groupCn = []
        with arcpy.da.SearchCursor(River.glq,['SHAPE@', 'Name', 'FID', 'According', 'province', 'city', 'county']) as aeras:
            with pythonaddins.ProgressDialog as dialog:
                dialog.title = "处理功能区".decode('utf-8')
                dialog.description = "计算功能区".decode('utf-8')
                dialog.animation = "Spiral"
                for i in xrange(100):
                    dialog.progress = i
                    time.sleep(0.125)
                    for aera in aeras:
                        id = aera[2]
                        print id
                        glq = aera[1]
                        zxX = aera[0].labelPoint.X
                        zxY = aera[0].labelPoint.Y
                        acording = aera[3]
                        prov = aera[4]
                        city = aera[5]
                        county = aera[6]
                        with arcpy.da.SearchCursor(River.dmal, 'SHAPE@') as dmals:
                            for line in dmals:
                                if not line[0].disjoint(aera[0]):
                                    clipLine = aera[0].intersect(line[0], 2)
                                    p1 = [clipLine.firstPoint.X, clipLine.firstPoint.Y]
                                    p2 = [clipLine.lastPoint.X, clipLine.lastPoint.Y]
                                    m1 = cal_M_AB(p1[0], p1[1], zxcn_lst)[0]
                                    m2 = cal_M_AB(p2[0], p2[1], zxcn_lst)[0]
                                    ab = cal_M_AB(p1[0], p1[1], zxcn_lst)[1]
                                    if m1 < m2:
                                        qd = p1
                                        zd = p2
                                        qdp = clipLine.firstPoint
                                        zdp = clipLine.lastPoint
                                    elif m1 > m2:
                                        qd = p2
                                        zd = p1
                                        qdp = clipLine.lastPoint
                                        zdp = clipLine.firstPoint
                                    qdE = XY2LatLon(qd[0], qd[1], fdh)[1]
                                    qdN = XY2LatLon(qd[0], qd[1], fdh)[0]
                                    zdE = XY2LatLon(zd[0], zd[1], fdh)[1]
                                    zdN = XY2LatLon(zd[0], zd[1], fdh)[0]
                                    QDMAmongDmal = 'K' + str(int(line[0].measureOnLine(qdp) / 1000.0)) + '+' + '%03d' % (
                                            line[0].measureOnLine(qdp) % 1000)
                                    ZDMAmongDmal = 'K' + str(int(line[0].measureOnLine(zdp) / 1000.0)) + '+' + '%03d' % (
                                            line[0].measureOnLine(zdp) % 1000)
                                    lenth = clipLine.length
                                    lcm = [clipLine.trueCentroid.X, clipLine.trueCentroid.Y]
                        with arcpy.da.SearchCursor(River.dmal2, 'SHAPE@') as dmals:
                            for line in dmals:
                                if not line[0].disjoint(aera[0]):
                                    clipLine = aera[0].intersect(line[0], 2)
                                    p1 = [clipLine.firstPoint.X, clipLine.firstPoint.Y]
                                    p2 = [clipLine.lastPoint.X, clipLine.lastPoint.Y]
                                    m1 = cal_M_AB(p1[0], p1[1], zxcn_lst)[0]
                                    m2 = cal_M_AB(p2[0], p2[1], zxcn_lst)[0]
                                    ab = cal_M_AB(p1[0], p1[1], zxcn_lst)[1]
                                    if m1 < m2:
                                        qd = p1
                                        zd = p2
                                    elif m1 > m2:
                                        qd = p2
                                        zd = p1
                                    qd2E = XY2LatLon(qd[0], qd[1], fdh)[1]
                                    qd2N = XY2LatLon(qd[0], qd[1], fdh)[0]
                                    zd2E = XY2LatLon(zd[0], zd[1], fdh)[1]
                                    zd2N = XY2LatLon(zd[0], zd[1], fdh)[0]
                        cn2 = [0, prov, city, county, 0, ab, glq, round(lenth / 1000.0, 2), qdE, qdN, zdE, zdN, qd2E, qd2N,
                               zd2E, zd2N,
                               qd[1], qd[0], zd[1],
                               zd[0], acording, id, m1, zxX, zxY, QDMAmongDmal, ZDMAmongDmal]
                        groupCn.append(cn2)
        df = pd.DataFrame(groupCn,
                          columns=['num', 'pro', 'city', 'county', 'bh', 'ab', 'glq', 'lenth', 'ste', 'stn', 'ene',
                                   'enn',
                                   'ste2', 'stn2', 'ene2', 'enn2',
                                   'stx', 'sty', 'endx', 'endy', 'according', 'fid', 'lc', 'zxX', 'zxY', 'qdM',
                                   'zdM'])
        df2 = df.groupby('ab')
        df_all = pd.DataFrame(
            columns=['num', 'pro', 'city', 'county', 'bh', 'ab', 'glq', 'lenth', 'ste', 'stn', 'ene', 'enn', 'ste2',
                     'stn2',
                     'ene2', 'enn2', 'stx', 'sty',
                     'endx', 'endy', 'according', 'fid', 'lc', 'zxX', 'zxY', 'qdM', 'zdM'])
        for name, group in df2:
            df6 = group
            df6.sort_values(by='lc', ascending=False, inplace=True)
            i = 0
            for i in range(0, len(df6)):
                df6.iloc[i, 4] = df6.iloc[i, 5] + str(i + 1)
                i += 1
            df_all = df_all.append(df6)
        i = 0
        for index, value in df_all.iterrows():
            df_all.loc[index, 'num'] = str(i)
            i += 1
        for index, value in df_all.iterrows():
            if '左' in df_all.loc[index, 'bh']:
                df_all.loc[index, 'bh'] = df_all.loc[index, 'bh'].replace('左岸', 'L')
            elif '右' in df_all.loc[index, 'bh']:
                df_all.loc[index, 'bh'] = df_all.loc[index, 'bh'].replace('右岸', 'R')
        df_all.columns = ['序号', '省', '市（地）级行政区', '县级行政区', '编号', '岸别', '功能区类型', '岸线长度(km)',
                          '起点坐标(经度）', '起点坐标(纬度）', '终点坐标(经度）', '终点坐标(纬度）',
                          '临水线起点坐标(经度）', '临水线起点坐标(纬度）', '临水线终点坐标(经度）', '临水线终点坐标(纬度）',
                          'stP_X', 'stP_Y', 'enP_X', 'enP_Y', '主要划分依据', 'FID', 'LC', '面中心X', '面中心Y', '起点桩号', '终点桩号']
        csv = path.encode('utf-8') + '\\' + '{}总表.csv'.format(riverName.encode('utf-8'))
        df_all.to_csv(csv.decode('utf-8'),encoding= 'gbk', index=False)
