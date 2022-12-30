 #coding=utf-8
import arcpy
import pythonaddins
import math
import pandas as pd
import os
import time
import tkinter as tk1
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
def listFiles(path, keyword, type):
    shps = []
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
                shps.append(shp)
    return shps
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
    df = ''
    ql = ''
    tk = ''
class ButtonClass37(object):
    """Implementation for T2_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        msList = []
        River.glq = pythonaddins.OpenDialog('选择功能区'.decode('utf-8'))
        River.path = arcpy.Describe(River.glq).path
        River.dmal = listFile(River.path, '管理范围线'.decode('utf-8'), 'x')
        River.dmal2 = listFile(River.path, '水位线'.decode('utf-8'), 'x')
        River.zx = listFile(River.path, '校正后中线'.decode('utf-8'), 'x')
        River.df = listFile(River.path, '堤防'.decode('utf-8'), 'x')
        River.ql = listFile(River.path, '桥梁'.decode('utf-8'), 'm')
        River.tk = listFile(River.path, '图框'.decode('utf-8'), 'm')
        River.name = arcpy.Describe(River.glq).baseName.replace('功能区'.decode('utf-8'), '')
        with arcpy.da.UpdateCursor(River.dmal, 'SHAPE@') as yb:
            for row in yb:
                with arcpy.da.SearchCursor(River.zx, 'SHAPE@') as yb2:
                    for row2 in yb2:
                        a = row2[0].measureOnLine(row[0].firstPoint)
                        b = row2[0].measureOnLine(row[0].lastPoint)
                        if a > b:
                            ms = '管理范围线起终点反向'
                            msList.append(ms)
        if River.dmal is None:
            ms = '缺少管理范围线'
            msList.append(ms)
        if 'According'.decode('utf-8') not in [field.name for field in arcpy.ListFields(River.glq)]:
            ms = '功能区缺少According字段'
            msList.append(ms)
        if River.dmal2 is None:
            ms = '缺少2年水位线'
            msList.append(ms)
        if River.zx is None:
            ms = '缺少校正后中线'
            msList.append(ms)
        if River.df is None:
            ms = '缺少堤防'
            msList.append(ms)
        if River.ql is None:
            ms = '缺少桥梁'
            msList.append(ms)
        if River.tk is None:
            ms = '缺少图框'
            msList.append(ms)
        for a in msList:
            pythonaddins.MessageBox(a.decode('utf-8'), '错误！'.decode('utf-8'))
class ButtonClass38(object):
    """Implementation for T2_addin.button_1 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        path = River.path
        dmal = River.dmal
        zx = River.zx
        arcpy.env.workspace = path
        arcpy.env.overwriteOutput = True
        with pythonaddins.ProgressDialog as dialog:
            dialog.title = "处理管理范围线".decode('utf-8')
            dialog.description = "翻转管理范围线".decode('utf-8')
            dialog.animation = "Spiral"
            for i in xrange(10):
                dialog.progress = i
                time.sleep(0.01)
                j = 0
                with arcpy.da.UpdateCursor(dmal, 'SHAPE@') as yb:
                    for row in yb:
                        with arcpy.da.SearchCursor(zx, 'SHAPE@') as yb2:
                            for row2 in yb2:
                                a = row2[0].measureOnLine(row[0].firstPoint)
                                b = row2[0].measureOnLine(row[0].lastPoint)
                                if a > b:
                                    tempLine = arcpy.CopyFeatures_management(row[0],
                                                                             path + '\\' + 'tempLine{}'.format(j))
                                    arcpy.FlipLine_edit(tempLine)
                                    yb.deleteRow()
                                    j += 1
                tls = listFiles(path, 'tempLine', 'x')
                cs = arcpy.da.InsertCursor(dmal, ['SHAPE@'])
                polylinelist = []
                for tl in tls:
                    with arcpy.da.SearchCursor(tl, 'SHAPE@') as yb:
                        for row in yb:
                            polylinelist.append(row[0])
                for l in polylinelist:
                    cs.insertRow([l])
                for l in tls:
                    arcpy.Delete_management(l)
class ButtonClass39(object):
    """Implementation for T2_addin.button_2 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        path = River.path
        riverName = River.name
        arcpy.env.workspace = path
        glq = River.glq
        dmal = River.dmal
        dmal2 = River.dmal2
        zx = River.zx
        spatial_ref = arcpy.Describe(glq).spatialReference
        if '99' in spatial_ref.name:
            xzjx = (path).encode('utf-8') + '\\' + '甘孜乡镇界带县名-99.shp'
            fdh = 99
        elif '102' in spatial_ref.name:
            xzjx = (path).encode('utf-8') + '\\' + '甘孜乡镇界带县名-102.shp'
            fdh = 102
        try:
            arcpy.AddField_management(glq, 'province', 'TEXT')
            arcpy.AddField_management(glq, 'city', 'TEXT')
            arcpy.AddField_management(glq, 'county', 'TEXT')
            arcpy.AddField_management(glq, 'BH', 'TEXT')
            arcpy.AddField_management(glq, 'AB', 'TEXT')
            arcpy.AddField_management(glq, 'LENGTH', 'TEXT')
        except:
            pass
        with arcpy.da.UpdateCursor(glq, ['SHAPE@', 'province', 'city', 'county']) as yb1:
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
        with arcpy.da.SearchCursor(zx, ['OID@', 'SHAPE@X', 'SHAPE@Y', 'SHAPE@M'], explode_to_points=True) as yb:
            for row in yb:
                cn = [row[1], row[2], row[3]]
                zxcn_lst.append(cn)
        groupCn = []
        with arcpy.da.SearchCursor(glq,['SHAPE@', 'Name', 'FID', 'According', 'province', 'city', 'county']) as aeras:
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
                with arcpy.da.SearchCursor(dmal, 'SHAPE@') as dmals:
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
                            QDMAmongDmal = 'K' + str(
                                int(line[0].measureOnLine(qdp) / 1000.0)) + '+' + '%03d' % (
                                                   line[0].measureOnLine(qdp) % 1000)
                            ZDMAmongDmal = 'K' + str(
                                int(line[0].measureOnLine(zdp) / 1000.0)) + '+' + '%03d' % (
                                                   line[0].measureOnLine(zdp) % 1000)
                            lenth = clipLine.length
                            lcm = [clipLine.trueCentroid.X, clipLine.trueCentroid.Y]
                with arcpy.da.SearchCursor(dmal2, 'SHAPE@') as dmals:
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
                cn2 = [0, prov, city, county, 0, ab, glq, round(lenth / 1000.0, 2), qdE, qdN, zdE, zdN, qd2E,
                       qd2N,
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
        df_all.to_csv(csv.decode('utf-8'), encoding='gbk', index=False)
class ButtonClass40(object):
    """Implementation for T2_addin.button_3 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        path = River.path
        riverName = River.name
        arcpy.env.workspace = path
        glq = River.glq
        csv = path.encode('utf-8') + '\\' + '{}总表.csv'.format(riverName.encode('utf-8'))
        p_cn = []
        dfForP = pd.read_csv(csv.decode('utf-8'), encoding='gbk')
        for index, value in dfForP.iterrows():
            cn = [value['面中心X'.decode('utf-8')],
                  value['面中心Y'.decode('utf-8')],
                  value['编号'.decode('utf-8')],
                  value['县级行政区'.decode('utf-8')],
                  value['功能区类型'.decode('utf-8')],
                  value['主要划分依据'.decode('utf-8')],
                  value['岸别'.decode('utf-8')],
                  value['FID'],
                  value['岸线长度(km)'.decode('utf-8')],
                  ]
            p_cn.append(cn)
        point = arcpy.Point()
        pointList = []
        for p in p_cn:
            point.X = p[0]
            point.Y = p[1]
            pg = arcpy.PointGeometry(point)
            pointList.append(pg)
        p = arcpy.CopyFeatures_management(pointList, path + '\\' + 'glqPoint.shp')
        centerMeridian = float(dfForP['起点坐标(经度）'.decode('utf-8')].mean())
        if centerMeridian < 100.5:
            arcpy.DefineProjection_management(p, coor_system='4542')
        elif centerMeridian > 100.5 and centerMeridian < 103.5:
            arcpy.DefineProjection_management(p, coor_system='4543')
        elif centerMeridian > 103.5:
            arcpy.DefineProjection_management(p, coor_system='4544')
        try:
            arcpy.AddField_management(p, 'Name', 'TEXT')
            arcpy.AddField_management(p, 'County', 'TEXT')
            arcpy.AddField_management(p, 'Type', 'TEXT')
            arcpy.AddField_management(p, 'According', 'TEXT')
            arcpy.AddField_management(p, 'Bank', 'TEXT')
            arcpy.AddField_management(p, 'Num', 'TEXT')
            arcpy.AddField_management(p, 'Lenth', 'TEXT')
        except:
            pass
        with arcpy.da.UpdateCursor(p, ['SHAPE@X', 'Name', 'County', 'Type', 'According', 'Bank', 'Num', 'Lenth']) as yb:
            for row in yb:
                for cn in p_cn:
                    if round(row[0], 1) == round(cn[0], 1):
                        row[1] = cn[2]
                        row[2] = cn[3]
                        row[3] = cn[4]
                        row[4] = cn[5]
                        row[5] = cn[6]
                        row[6] = cn[7]
                        row[7] = '%0.2f' % round(cn[8], 2)
                yb.updateRow(row)
        with arcpy.da.UpdateCursor(glq, ['SHAPE@', 'BH', 'AB', 'LENGTH']) as yb1:
            for row1 in yb1:
                with arcpy.da.SearchCursor(p, ['SHAPE@', 'Name', 'Bank', 'Lenth']) as yb2:
                    for row2 in yb2:
                        if row1[0].contains(row2[0]):
                            row1[1] = row2[1]
                            row1[2] = row2[2]
                            row1[3] = row2[3]
                            yb1.updateRow(row1)
        arcpy.Delete_management(p)
class ButtonClass41(object):
    """Implementation for T2_addin.button_4 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        path = River.path
        riverName = River.name
        arcpy.env.workspace = path
        arcpy.env.overwriteOutput=True
        dmal = River.dmal
        zx = River.zx
        spatial_ref = arcpy.Describe(dmal).spatialReference
        KpList = []
        with arcpy.da.SearchCursor(dmal, 'SHAPE@') as yb:
            for row in yb:
                with arcpy.da.SearchCursor(zx, 'SHAPE@') as yb2:
                    for row2 in yb2:
                        ab = row2[0].queryPointAndDistance(row[0].firstPoint)
                        if ab[3] is True:
                            lenth = row[0].length
                            i = 0
                            while i < lenth:
                                name = 'K' + str(i / 1000)
                                Kp = row[0].positionAlongLine(i)
                                cn = [name, Kp]
                                KpList.append(cn)
                                print 'K' + str(i / 1000), row[0].positionAlongLine(i).centroid.X, row[
                                    0].positionAlongLine(
                                    i).centroid.Y
                                i += 1000
                        else:
                            lenth = row[0].length
                            i = 0
                            while i < lenth:
                                name = 'K' + str(i / 1000)
                                Kp = row[0].positionAlongLine(i)
                                cn = [name, Kp]
                                KpList.append(cn)
                                print 'K' + str(i / 1000), row[0].positionAlongLine(i).centroid.X, row[
                                    0].positionAlongLine(
                                    i).centroid.Y
                                i += 1000
        p = arcpy.CreateFeatureclass_management(path, '{}公里桩'.format(riverName.encode('utf-8')), 'POINT',
                                                spatial_reference=spatial_ref)
        arcpy.AddField_management(p, 'name', 'TEXT')
        yb = arcpy.da.InsertCursor(p, ['name', 'SHAPE@'])
        for cn in KpList:
            yb.insertRow(cn)
        del yb
class ButtonClass42(object):
    """Implementation for T2_addin.button_5 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        path = River.path
        riverName = River.name
        arcpy.env.workspace = path
        glq = River.glq
        dmal = River.dmal
        spatial_ref = arcpy.Describe(glq).spatialReference
        if '99' in spatial_ref.name:
            xzjx = (path).encode('utf-8') + '\\' + '甘孜乡镇界带县名-99.shp'
        elif '102' in spatial_ref.name:
            xzjx = (path).encode('utf-8') + '\\' + '甘孜乡镇界带县名-102.shp'
        groupCn = []
        with arcpy.da.SearchCursor(glq, ['SHAPE@', 'BH', 'AB', 'Name', 'According']) as yb:
            for row in yb:
                print row[1]
                with arcpy.da.SearchCursor(dmal, 'SHAPE@') as dmals:
                    for line in dmals:
                        if not line[0].disjoint(row[0]):
                            clipLine = row[0].intersect(line[0], 2)
                            with arcpy.da.SearchCursor(xzjx, ['SHAPE@', 'XZQMC_1', 'XZQMC']) as yb2:
                                for row2 in yb2:
                                    if row2[0].crosses(clipLine):
                                        clipLine2 = row2[0].intersect(clipLine, 2)
                                        lenth = clipLine2.length
                                        xq2 = row2[1] + row2[2]
                                        cn = [row[1], row2[1], row[3], row2[2], lenth, xq2]
                                        groupCn.append(cn)
                                    elif row2[0].contains(clipLine):
                                        lenth = clipLine.length
                                        xq2 = row2[1] + row2[2]
                                        cn = [row[1], row2[1], row[3], row2[2], lenth, xq2]
                                        groupCn.append(cn)
        df = pd.DataFrame(groupCn, columns=['a', 'b', 'c', 'd', 'e', 'f'])
        groupCn2 = []
        title1 = ['按区县分', '', '', '', '', '']
        groupCn2.append(title1)
        for name, group in df.groupby('b'):
            xz = name
            allcount = group['a'].count()
            allLength = round((group['e'].sum()) / 1000.0, 2)
            bhqcount = group[group['c'] == u'岸线保护区']['a'].count()
            bhqLength = round((group[group['c'] == u'岸线保护区']['e'].sum()) / 1000.0, 2)
            bhqPercent = '{:.2f}%'.format(((group[group['c'] == u'岸线保护区']['e'].sum()) / (group['e'].sum()) * 100))
            blqcount = group[group['c'] == u'岸线保留区']['a'].count()
            blqLength = round((group[group['c'] == u'岸线保留区']['e'].sum()) / 1000.0, 2)
            blqPercent = '{:.2f}%'.format(((group[group['c'] == u'岸线保留区']['e'].sum()) / (group['e'].sum()) * 100))
            kzlyqcount = group[group['c'] == u'岸线控制利用区']['a'].count()
            kzlyqLength = round((group[group['c'] == u'岸线控制利用区']['e'].sum()) / 1000.0, 2)
            kzlyqPercent = '{:.2f}%'.format(((group[group['c'] == u'岸线控制利用区']['e'].sum()) / (group['e'].sum()) * 100))
            kflyqcount = group[group['c'] == u'岸线开发利用区']['a'].count()
            kflyqLength = round((group[group['c'] == u'岸线开发利用区']['e'].sum()) / 1000.0, 2)
            kflyqPercent = '{:.2f}%'.format(((group[group['c'] == u'岸线开发利用区']['e'].sum()) / (group['e'].sum()) * 100))
            cn = [xz, allcount, allLength, bhqcount, bhqLength, bhqPercent, blqcount, blqLength, blqPercent, kzlyqcount,
                  kzlyqLength, kzlyqPercent, kflyqcount, kflyqLength, kflyqPercent]
            groupCn2.append(cn)
        title2 = ['按乡镇统计']
        space = ['']
        groupCn2.append(space)
        groupCn2.append(title2)
        for name, group in df.groupby('f'):
            xz = name
            allcount = group['a'].count()
            allLength = round((group['e'].sum()) / 1000.0, 2)
            bhqcount = group[group['c'] == u'岸线保护区']['a'].count()
            bhqLength = round((group[group['c'] == u'岸线保护区']['e'].sum()) / 1000.0, 2)
            bhqPercent = '{:.2f}%'.format(((group[group['c'] == u'岸线保护区']['e'].sum()) / (group['e'].sum()) * 100))
            blqcount = group[group['c'] == u'岸线保留区']['a'].count()
            blqLength = round((group[group['c'] == u'岸线保留区']['e'].sum()) / 1000.0, 2)
            blqPercent = '{:.2f}%'.format(((group[group['c'] == u'岸线保留区']['e'].sum()) / (group['e'].sum()) * 100))
            kzlyqcount = group[group['c'] == u'岸线控制利用区']['a'].count()
            kzlyqLength = round((group[group['c'] == u'岸线控制利用区']['e'].sum()) / 1000.0, 2)
            kzlyqPercent = '{:.2f}%'.format(((group[group['c'] == u'岸线控制利用区']['e'].sum()) / (group['e'].sum()) * 100))
            kflyqcount = group[group['c'] == u'岸线开发利用区']['a'].count()
            kflyqLength = round((group[group['c'] == u'岸线开发利用区']['e'].sum()) / 1000.0, 2)
            kflyqPercent = '{:.2f}%'.format(((group[group['c'] == u'岸线开发利用区']['e'].sum()) / (group['e'].sum()) * 100))
            cn = [xz, allcount, allLength, bhqcount, bhqLength, bhqPercent, blqcount, blqLength, blqPercent, kzlyqcount,
                  kzlyqLength, kzlyqPercent, kflyqcount, kflyqLength, kflyqPercent]
            groupCn2.append(cn)
        df2 = pd.DataFrame(groupCn2, columns=['县（区）', '功能区个数', '长度',
                                              '保护区个数', '长度', '占比',
                                              '保留区个数', '长度', '占比',
                                              '控制利用区个数', '长度', '占比',
                                              '开发利用区个数', '长度', '占比'])
        csv = path.encode('utf-8') + '\\' + '{}县区占比表.csv'.format(riverName.encode('utf-8'))
        df2.to_csv(csv.decode('utf-8'), encoding='gbk', index=False)
class ButtonClass44(object):
    """Implementation for T2_addin.button_7 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        path = River.path
        tk = River.tk
        glq = River.glq
        riverName = River.name
        cnList = []
        with arcpy.da.SearchCursor(tk, ['SHAPE@', 'name']) as yb:
            for row in yb:
                with arcpy.da.SearchCursor(glq, ['SHAPE@', 'county']) as yb2:
                    for row2 in yb2:
                        if row[0].overlaps(row2[0]):
                            cn = [row[1], row2[1]]
                        elif row[0].contains(row2[0]):
                            cn = [row[1], row2[1]]
                cnList.append(cn)
        cnListSort = sorted(cnList, key=lambda s: s[0])
        cn2List = []
        i = 1
        for cn in cnListSort:
            cn2 = ['规划示意图（{}/{}）'.format(i + 3, len(cnListSort) + 3), cn[0], cn[1]]
            cn2List.append(cn2)
            i += 1
        df = pd.DataFrame(cn2List, columns=['图名', '页码', '行政区'])
        csv = path.encode('utf-8') + '\\' + '{}页码统计表.csv'.format(riverName.encode('utf-8'))
        df.to_csv(csv.decode('utf-8'), encoding='gbk', index=False)
class ButtonClass45(object):
    """Implementation for T2_addin.button_8 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        arcpy.env.overwriteOutput=True
        path = River.path
        arcpy.env.workspace = path
        dmal = River.dmal
        riverName = River.name
        glq = River.glq
        qs = River.ql
        df = River.df
        zx = River.zx
        sp = arcpy.Describe(glq).spatialReference
        if '99' in sp.name:
            xzjx = (path).encode('utf-8') + '\\' + '甘孜乡镇界带县名-99.shp'
            fdh = 99
        elif '102' in sp.name:
            xzjx = (path).encode('utf-8') + '\\' + '甘孜乡镇界带县名-102.shp'
            fdh = 102
        tempLines = []
        cnList = []
        with arcpy.da.SearchCursor(dmal, 'SHAPE@') as yb:
            for row in yb:
                with arcpy.da.SearchCursor(qs, ['SHAPE@', 'Name']) as yb2:
                    for row2 in yb2:
                        QName = row2[1]
                        for part in row2[0]:
                            MList = []
                            for pnt in part:
                                MList.append(row[0].measureOnLine(pnt))
                            cn = [row[0].segmentAlongLine(min(MList), max(MList)), QName]
                            tempLines.append(cn)
        QToL = arcpy.CreateFeatureclass_management(path, 'QToL.shp', 'POLYLINE', template=qs, spatial_reference=sp)
        cs = arcpy.da.InsertCursor(QToL,['SHAPE@','Name'])
        for shp in tempLines:
            cs.insertRow([shp[0],shp[1]])
        with arcpy.da.SearchCursor(QToL, ['SHAPE@', 'Name']) as yb:
            for row in yb:
                lx = '桥梁'
                print row[1]
                if row[0] is not None:
                    with arcpy.da.SearchCursor(xzjx, ['SHAPE@', 'XZQMC', 'XZQMC_1']) as yb2:
                        for row2 in yb2:
                            if row2[0].contains(row[0]):
                                qxmc = row2[2] + row2[1]
                    with arcpy.da.SearchCursor(zx, 'SHAPE@') as yb3:
                        for row3 in yb3:
                            if row3[0].queryPointAndDistance(row[0].firstPoint)[3] is True:
                                ab = '右岸'
                            else:
                                ab = '左岸'
                    with arcpy.da.SearchCursor(dmal, 'SHAPE@') as yb4:
                        for row4 in yb4:
                            m1 = row4[0].measureOnLine(row[0].firstPoint)
                            m2 = row4[0].measureOnLine(row[0].lastPoint)
                            p1x = 'E' + '%0.8f' % round(XY2LatLon(row[0].firstPoint.X, row[0].firstPoint.Y, fdh)[1],
                                                        8) + '°'
                            p1y = 'N' + '%0.8f' % round(XY2LatLon(row[0].firstPoint.X, row[0].firstPoint.Y, fdh)[0],
                                                        8) + '°'
                            p2x = 'E' + '%0.8f' % round(XY2LatLon(row[0].lastPoint.X, row[0].lastPoint.Y, fdh)[1],
                                                        8) + '°'
                            p2y = 'N' + '%0.8f' % round(XY2LatLon(row[0].lastPoint.X, row[0].lastPoint.Y, fdh)[0],
                                                        8) + '°'
                            if m1 < m2:
                                qdm = m1
                                zdm = m2
                                qdx = p1x
                                qdy = p1y
                                zdx = p2x
                                zdy = p2y
                            else:
                                qdm = m2
                                zdm = m1
                                qdx = p2x
                                qdy = p2y
                                zdx = p1x
                                zdy = p1y
                            qdm2 = 'K' + str(int(qdm / 1000.0)) + '+' + '%03d' % (qdm % 1000)
                            zdm2 = 'K' + str(int(zdm / 1000.0)) + '+' + '%03d' % (zdm % 1000)
                    cn = [row[1], lx, ab, qxmc, '%0.2f' % round(row[0].length, 2), qdx, qdy, zdx, zdy, qdm2, zdm2, qdm]
                    cnList.append(cn)
        arcpy.Delete_management(QToL)
        if len(df) > 0:
            with arcpy.da.SearchCursor(df, ['SHAPE@', 'Name']) as yb:
                for row in yb:
                    lx = '堤防'
                    print row[1]
                    with arcpy.da.SearchCursor(xzjx, ['SHAPE@', 'XZQMC', 'XZQMC_1']) as yb2:
                        for row2 in yb2:
                            if row2[0].contains(row[0]):
                                qxmc = row2[2] + row2[1]
                    with arcpy.da.SearchCursor(dmal, 'SHAPE@') as yb4:
                        for row4 in yb4:
                            m1 = row4[0].measureOnLine(row[0].firstPoint)
                            m2 = row4[0].measureOnLine(row[0].lastPoint)
                            tempLine = row4[0].segmentAlongLine(m1, m2)
                            p1x = 'E' + '%0.8f' % round(
                                XY2LatLon(tempLine.firstPoint.X, tempLine.firstPoint.Y, fdh)[1], 8) + '°'
                            p1y = 'N' + '%0.8f' % round(
                                XY2LatLon(tempLine.firstPoint.X, tempLine.firstPoint.Y, fdh)[0], 8) + '°'
                            p2x = 'E' + '%0.8f' % round(XY2LatLon(tempLine.lastPoint.X, tempLine.lastPoint.Y, fdh)[1],
                                                        8) + '°'
                            p2y = 'N' + '%0.8f' % round(XY2LatLon(tempLine.lastPoint.X, tempLine.lastPoint.Y, fdh)[0],
                                                        8) + '°'
                            if m1 < m2:
                                qdm = m1
                                zdm = m2
                                qdx = p1x
                                qdy = p1y
                                zdx = p2x
                                zdy = p2y
                            else:
                                qdm = m2
                                zdm = m1
                                qdx = p2x
                                qdy = p2y
                                zdx = p1x
                                zdy = p1y
                            qdm2 = 'K' + str(int(qdm / 1000.0)) + '+' + '%03d' % (qdm % 1000)
                            zdm2 = 'K' + str(int(zdm / 1000.0)) + '+' + '%03d' % (zdm % 1000)
                    with arcpy.da.SearchCursor(zx, 'SHAPE@') as yb3:
                        for row3 in yb3:
                            if row3[0].queryPointAndDistance(row[0].firstPoint)[3] is True:
                                ab = '右岸'
                            else:
                                ab = '左岸'
                    cn = [row[1], lx, ab, qxmc, '%0.2f' % round(tempLine.length, 2), qdx, qdy, zdx, zdy, qdm2, zdm2,
                          qdm]
                    cnList.append(cn)
        cnList2 = sorted(cnList, key=lambda s: s[11])
        df = pd.DataFrame(cnList2, columns=['名称', '涉河设施类别', '岸别', '县（区）', '占用岸线长度（m)', '起点经度', '起点纬度', '终点经度', '终点纬度',
                                            '起点里程', '终点里程', 'Num'])
        csv = path.encode('utf-8') + '\\' + '{}涉河设施表.csv'.format(riverName.encode('utf-8'))
        df.to_csv(csv.decode('utf-8'), encoding='gbk', index=False)
class ButtonClass46(object):
    """Implementation for T2_addin.button_9 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        path = River.path
        try:
            arcpy.CreateFolder_management(path, 'pdf')
        except:
            pass
        riverName = River.name
        arcpy.env.workspace = path
        arcpy.env.workspace = path
        arcpy.env.overwriteOutput = True
        mxd = arcpy.mapping.MapDocument('current')
        tk = path.encode('utf-8') + '\\' + '{}图框.shp'.format(riverName.encode('utf-8'))
        zbz = arcpy.mapping.ListLayoutElements(mxd, 'Mapsurround_Element', '')[0]
        TopRightX = 27.8336
        TopRightY = 24.683
        TopLeftX = 0.8613
        TopLeftY = 24.683
        with pythonaddins.ProgressDialog as dialog:
            dialog.title = "草图出图".decode('utf-8')
            dialog.description = "正在出图".decode('utf-8')
            dialog.animation = "Spiral"
            dialog.canCancel = True
            for pagenum in range(1, mxd.dataDrivenPages.pageCount + 1):
                dialog.progress = pagenum
                time.sleep(0.1)
                mxd.dataDrivenPages.currentPageID = pagenum  # 驱动页面从1开始
                cursor = arcpy.SearchCursor(tk)
                for i in cursor:
                    if i.FID == pagenum - 1:
                        if i.Zbz == 0:
                            x = TopLeftX
                            y = TopLeftY
                        else:
                            x = TopRightX
                            y = TopRightY
                        print i.Name, i.Zbz
                        zbz.elementPositionX = x
                        zbz.elementPositionY = y
                        mxd.save
                        jpgPath = path.encode('utf-8') + '\\' + 'pdf' + '\\' + (i.Name).encode('utf-8') + ".jpg"
                        arcpy.mapping.ExportToJPEG(mxd, jpgPath.decode('utf-8'),resolution=40)
class ButtonClass51(object):
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        path = River.path
        try:
            arcpy.CreateFolder_management(path, 'pdf')
        except:
            pass
        riverName = River.name
        arcpy.env.workspace = path
        arcpy.env.workspace = path
        arcpy.env.overwriteOutput = True
        mxd = arcpy.mapping.MapDocument('current')
        tk = path.encode('utf-8') + '\\' + '{}图框.shp'.format(riverName.encode('utf-8'))
        zbz = arcpy.mapping.ListLayoutElements(mxd, 'Mapsurround_Element', '')[0]
        TopRightX = 27.8336
        TopRightY = 24.683
        TopLeftX = 0.8613
        TopLeftY = 24.683
        with pythonaddins.ProgressDialog as dialog:
            dialog.title = "正式图出图".decode('utf-8')
            dialog.description = "正在出图".decode('utf-8')
            dialog.animation = "Spiral"
            dialog.canCancel = True
            for pagenum in range(1, mxd.dataDrivenPages.pageCount + 1):
                dialog.progress = pagenum
                time.sleep(2)
                mxd.dataDrivenPages.currentPageID = pagenum  # 驱动页面从1开始
                cursor = arcpy.SearchCursor(tk)
                for i in cursor:
                    if i.FID == pagenum - 1:
                        if i.Zbz == 0:
                            x = TopLeftX
                            y = TopLeftY
                        else:
                            x = TopRightX
                            y = TopRightY
                        print i.Name, i.Zbz
                        zbz.elementPositionX = x
                        zbz.elementPositionY = y
                        mxd.save
                        jpgPath = path.encode('utf-8') + '\\' + 'pdf' + '\\' + (i.Name).encode('utf-8') + ".jpg"
                        arcpy.mapping.ExportToJPEG(mxd, jpgPath.decode('utf-8'), resolution=400)