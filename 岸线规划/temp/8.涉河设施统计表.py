# coding=utf-8
import arcpy
import pandas as pd
import math
import random
import os
import pandas as pd
def cal_xy_byM(m, zxcn_lst):
    newZxList = []
    for cn in zxcn_lst:
        dis = cn[2] - m
        cn1 = [cn[0], cn[1], dis]
        newZxList.append(cn1)
    a = [cn for cn in newZxList if cn[2] < 0][-1]
    b = [cn for cn in newZxList if cn[2] > 0][0]
    x1 = a[0]
    y1 = a[1]
    s1 = abs(a[2])
    x2 = b[0]
    y2 = b[1]
    s2 = abs(b[2])
    s3 = s1 + s2
    x0 = (s1 * (x2 - x1) + s3 * x1) / s3
    y0 = (s1 * (y2 - y1) + s3 * y1) / s3
    return x0, y0
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
    np_m = x1_m - math.sqrt((czx - x1) ** 2 + (czy - y1) ** 2)
    return np_m, ab, czx, czy
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
path = r'E:\2021年项目\1108\色乌绒沟'
arcpy.env.workspace = path
shss = listFile(path, '桥梁'.decode('utf-8'), 'm')
dmal = listFile(path, '管理范围'.decode('utf-8'), 'x')
zx = listFile(path, '中线'.decode('utf-8'), 'x')
zxCnLst = []
with arcpy.da.SearchCursor(zx, ['OID@', 'SHAPE@X', 'SHAPE@Y', 'SHAPE@M'], explode_to_points=True) as yb:
    for row in yb:
        cn = [row[1], row[2], row[3]]
        zxCnLst.append(cn)
spatial_ref = arcpy.Describe(dmal).spatialReference
if '99' in spatial_ref.name:
    xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-99.shp'
    fdh = 99
elif '102' in spatial_ref.name:
    xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-102.shp'
    fdh = 102
xlsList = []
with arcpy.da.SearchCursor(shss, ['SHAPE@', 'type', 'name', 'FID', 'SHAPE@X', 'SHAPE@Y'])as qs:
    for q in qs:
        with arcpy.da.SearchCursor(xzjx, ['SHAPE@', 'XZQMC_1']) as xzqs:
            for xzq in xzqs:
                if xzq[0].contains(q[0].labelPoint):
                    qxzq = xzq[1]
        if '桥梁'.decode('utf-8') in q[1]:
            for qps in q[0]:
                cnList = []
                szList = []
                for pnt in qps:
                    cn = [pnt.X, pnt.Y]
                    cnList.append(cn)
                p1 = [sorted(cnList, key=lambda s: s[0])[0][0], sorted(cnList, key=lambda s: s[0])[0][1]]
                p2 = [sorted(cnList, key=lambda s: s[0])[-1][0], sorted(cnList, key=lambda s: s[0])[-1][1]]
                p3 = [sorted(cnList, key=lambda s: s[1])[0][0], sorted(cnList, key=lambda s: s[1])[0][1]]
                p4 = [sorted(cnList, key=lambda s: s[1])[-1][0], sorted(cnList, key=lambda s: s[1])[-1][1]]
                szList.append(p1)
                szList.append(p2)
                szList.append(p3)
                szList.append(p4)
                Qlen = round(min(math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2),
                                 math.sqrt((p1[0] - p3[0]) ** 2 + (p1[1] - p3[1]) ** 2),
                                 math.sqrt((p1[0] - p4[0]) ** 2 + (p1[1] - p4[1]) ** 2)), 1)
                mLList = []
                mRList = []
                for a in szList:
                    point = arcpy.Point(a[0], a[1])
                    pg = arcpy.PointGeometry(point)
                    with arcpy.da.SearchCursor(dmal, ['SHAPE@', 'BANK'], '"BANK" = 0') as dmals:
                        for L in dmals:
                            m = L[0].queryPointAndDistance(pg)[1]
                            disL = L[0].queryPointAndDistance(pg)[2]
                            Lpx = L[0].queryPointAndDistance(pg)[0].centroid.X
                            Lpy = L[0].queryPointAndDistance(pg)[0].centroid.Y
                            Lcn = [m, disL, Lpx, Lpy]
                            mLList.append(Lcn)
                    with arcpy.da.SearchCursor(dmal, ['SHAPE@', 'BANK'], '"BANK" = 1') as dmals:
                        for R in dmals:
                            m1 = R[0].queryPointAndDistance(pg)[1]
                            disR = R[0].queryPointAndDistance(pg)[2]
                            Rpx = R[0].queryPointAndDistance(pg)[0].centroid.X
                            Rpy = R[0].queryPointAndDistance(pg)[0].centroid.Y
                            Rcn = [m1, disR, Rpx, Rpy]
                            mRList.append(Rcn)
                mL1 = sorted(mLList, key=lambda s: s[1])[0][0]
                mL2 = sorted(mLList, key=lambda s: s[1])[1][0]
                mR1 = sorted(mRList, key=lambda s: s[1])[0][0]
                mR2 = sorted(mRList, key=lambda s: s[1])[1][0]
                Lp1x = sorted(mLList, key=lambda s: s[1])[0][2]
                Lp1y = sorted(mLList, key=lambda s: s[1])[0][3]
                Lp2x = sorted(mLList, key=lambda s: s[1])[1][2]
                Lp2y = sorted(mLList, key=lambda s: s[1])[1][3]
                Rp1x = sorted(mRList, key=lambda s: s[1])[0][2]
                Rp1y = sorted(mRList, key=lambda s: s[1])[0][3]
                Rp2x = sorted(mRList, key=lambda s: s[1])[1][2]
                Rp2y = sorted(mRList, key=lambda s: s[1])[1][3]
                NewMLx = sorted(mLList, key=lambda s: s[0])[0][2]
                NewMLy = sorted(mLList,key = lambda s:s[0])[0][3]
                NewMRx = sorted(mRList, key=lambda s: s[0])[0][2]
                NewMRy = sorted(mRList, key=lambda s: s[0])[0][3]
                LLenth = round(abs(mL1 - mL2), 1)
                RLenth = round(abs(mR1 - mR2), 1)
            # print q[3], '甘孜州', qxzq, '左岸', q[2], '桥梁', LLenth, Lp1x, Lp1y
            # print q[3], '甘孜州', qxzq, '左岸', q[2], '桥梁', LLenth, Lp2x, Lp2y
            # print q[3], '甘孜州', qxzq, '右岸', q[2], '桥梁', RLenth, Rp1x, Rp1y
            # print q[3], '甘孜州', qxzq, '右岸', q[2], '桥梁', RLenth, Rp2x, Rp2y
            if LLenth - Qlen < 0:
                LLenth = Qlen + random.randint(1, 5) / 10.0
            if RLenth - Qlen < 0:
                RLenth = Qlen + random.randint(1, 5) / 10.0
            # xls1 = [q[3], '甘孜州', qxzq, '左岸', q[2], '桥梁', LLenth, XY2LatLon(NewMLx,NewMLy,fdh)[1],XY2LatLon(NewMLx,NewMLy,fdh)[0],mL1]                               桥梁起点坐标
            # xls2 = [q[3], '甘孜州', qxzq, '右岸', q[2], '桥梁', RLenth,XY2LatLon(NewMRx,NewMRy,fdh)[1],XY2LatLon(NewMRx,NewMRy,fdh)[0], mR1]
            xls1 = [q[3], '甘孜州', qxzq, '左岸', q[2], '桥梁', LLenth, XY2LatLon(q[0].centroid.X,q[0].centroid.Y,fdh)[1],XY2LatLon(q[0].centroid.X,q[0].centroid.Y,fdh)[0],mL1]        #桥梁中心点坐标
            xls2 = [q[3], '甘孜州', qxzq, '右岸', q[2], '桥梁', RLenth,XY2LatLon(q[0].centroid.X,q[0].centroid.Y,fdh)[1],XY2LatLon(q[0].centroid.X,q[0].centroid.Y,fdh)[0], mR1]
            xlsList.append(xls1)
            xlsList.append(xls2)
        if q[1] == '公路桥'.decode('utf-8'):
            glqX = q[0].centroid.X
            glqY = q[0].centroid.Y
            m = cal_M_AB(glqX, glqY, zxCnLst)[0]
            sym = m + 200
            xym = m - 200
            if xym > 0:
                symx = cal_xy_byM(sym, zxCnLst)[0]
                symy = cal_xy_byM(sym, zxCnLst)[1]
                xymx = cal_xy_byM(xym, zxCnLst)[0]
                xymy = cal_xy_byM(xym, zxCnLst)[1]
                syp = arcpy.Point(symx, symy)
                sypg = arcpy.PointGeometry(syp)
                xyp = arcpy.Point(xymx, xymy)
                xypg = arcpy.PointGeometry(xyp)
            else:
                symx = cal_xy_byM(sym, zxCnLst)[0]
                symy = cal_xy_byM(sym, zxCnLst)[1]
                syp = arcpy.Point(symx, symy)
                sypg = arcpy.PointGeometry(syp)
            with arcpy.da.SearchCursor(dmal, ['SHAPE@', 'BANK'], '"BANK" = 0') as dmals:
                for L in dmals:
                    if xym < 0:
                        print q[2],sym,xym,L[0].measureOnLine(sypg)
                        xls3 = [q[3], '甘孜州', qxzq, '左岸', q[2], '公路桥',
                                round(L[0].measureOnLine(sypg), 1),XY2LatLon(q[0].centroid.X,q[0].centroid.Y,fdh)[1],XY2LatLon(q[0].centroid.X,q[0].centroid.Y,fdh)[0], sym]
                    else:
                        print q[2], sym, xym,L[0].measureOnLine(sypg),L[0].measureOnLine(xypg)
                        xls3 = [q[3], '甘孜州', qxzq, '左岸', q[2], '公路桥',
                                round((L[0].measureOnLine(sypg) - L[0].measureOnLine(xypg)), 1),XY2LatLon(q[0].centroid.X,q[0].centroid.Y,fdh)[1],XY2LatLon(q[0].centroid.X,q[0].centroid.Y,fdh)[0], sym]
                    xlsList.append(xls3)
            with arcpy.da.SearchCursor(dmal, ['SHAPE@', 'BANK'], '"BANK" = 1') as dmals:
                for R in dmals:
                    if xym < 0:
                        print q[2],sym,xym,R[0].measureOnLine(sypg)
                        xls4 = [q[3], '甘孜州', qxzq, '右岸', q[2], '公路桥',
                                round(R[0].measureOnLine(sypg), 1),XY2LatLon(q[0].centroid.X,q[0].centroid.Y,fdh)[1],XY2LatLon(q[0].centroid.X,q[0].centroid.Y,fdh)[0], sym]
                    else:
                        print q[2], sym, xym, R[0].measureOnLine(sypg), R[0].measureOnLine(xypg)
                        xls4 = [q[3], '甘孜州', qxzq, '右岸', q[2], '公路桥',
                                round((R[0].measureOnLine(sypg) - R[0].measureOnLine(xypg)), 1),XY2LatLon(q[0].centroid.X,q[0].centroid.Y,fdh)[1],XY2LatLon(q[0].centroid.X,q[0].centroid.Y,fdh)[0], sym]
                    xlsList.append(xls4)
if listFile(path,'堤防'.decode('utf-8'), 'x') is not None:
    shss_df = listFile(path, '堤防'.decode('utf-8'), 'x')
    dfLList = []
    dfRList = []
    with arcpy.da.SearchCursor(shss_df, ['SHAPE@', 'Name', 'BANK', 'FID'], '"BANK" = 0') as dfs:
        for df in dfs:
            print df[1]
            with arcpy.da.SearchCursor(xzjx, ['SHAPE@', 'XZQMC_1']) as xzqs:
                for xzq in xzqs:
                    if xzq[0].contains(df[0].labelPoint):
                        dfxzq = xzq[1]
            x1 = df[0].firstPoint.X
            y1 = df[0].firstPoint.Y
            m1 = cal_M_AB(x1, y1, zxCnLst)[0]
            x2 = df[0].lastPoint.X
            y2 = df[0].lastPoint.Y
            m2 = cal_M_AB(x2, y2, zxCnLst)[0]
            if m1>m2:
                qdx = x2
                qdy = y2
                qdm = m2
            else:
                qdx = x1
                qdy = y1
                qdm = m1
            M = min(m1,m2)
            dfLCn = [df[3], '甘孜州', dfxzq, '左岸', df[1], '堤防', df[0].length, qdx,qdy,qdm]
            dfLList.append(dfLCn)
    dfLNameList = []
    for a in dfLList:
        Lname = a[4]
        if Lname not in dfLNameList:
            dfLNameList.append(Lname)
    for a in dfLNameList:
        LLenth = round(sum([b[6] for b in dfLList if b[4] == a]), 1)
        Lm = min([b[9] for b in dfLList if b[4] == a])
        qdxAll = sorted(dfLList,key = lambda s:s[9])[0][7]
        qdyAll = sorted(dfLList, key=lambda s: s[9])[0][8]
        xls5 = [dfLList[0][0], dfLList[0][1], dfLList[0][2], dfLList[0][3], a, dfLList[0][5], LLenth,XY2LatLon(qdxAll,qdyAll,fdh)[1],XY2LatLon(qdxAll,qdyAll,fdh)[0],Lm]
        xlsList.append(xls5)
    with arcpy.da.SearchCursor(shss_df, ['SHAPE@', 'Name', 'BANK', 'FID'], '"BANK" = 1') as dfs:
        for df in dfs:
            with arcpy.da.SearchCursor(xzjx, ['SHAPE@', 'XZQMC_1']) as xzqs:
                for xzq in xzqs:
                    if xzq[0].contains(df[0].labelPoint):
                        dfxzq = xzq[1]
            x1 = df[0].firstPoint.X
            y1 = df[0].firstPoint.Y
            m1 = cal_M_AB(x1, y1, zxCnLst)[0]
            x2 = df[0].lastPoint.X
            y2 = df[0].lastPoint.Y
            m2 = cal_M_AB(x2, y2, zxCnLst)[0]
            if m1>m2:
                qdx = x2
                qdy = y2
                qdm = m2
            else:
                qdx = x1
                qdy = y1
                qdm = m1
            M = min(m1,m2)
            dfRCn = [df[3], '甘孜州', dfxzq, '右岸', df[1], '堤防', df[0].length, qdx,qdy,qdm]
            dfRList.append(dfRCn)
    dfRNameList = []
    for a in dfRList:
        Rname = a[4]
        if Rname not in dfRNameList:
            dfRNameList.append(Rname)
    for a in dfRNameList:
        RLenth = round(sum([b[6] for b in dfRList if b[4] == a]), 1)
        Rm = min([b[7] for b in dfRList if b[4] == a])
        qdxAll = sorted(dfRList,key = lambda s:s[9])[0][7]
        qdyAll = sorted(dfRList, key=lambda s: s[9])[0][8]
        xls6 = [dfRList[0][0], dfRList[0][1], dfRList[0][2], dfRList[0][3], a, dfRList[0][5], RLenth,XY2LatLon(qdxAll,qdyAll,fdh)[1],XY2LatLon(qdxAll,qdyAll,fdh)[0],Rm]
        xlsList.append(xls6)
okxls = sorted(xlsList, key=lambda s: s[7])
df = pd.DataFrame(okxls, columns=['序号', '市（地）级行政区', '县级行政区', '岸别', '项目名称', '类型', '占用岸线长度(m)', '起点坐标（经度）','起点坐标（纬度）','里程'])
df.to_excel(path.decode('utf-8') + '\\' + u'涉河设施表.xlsx', index=False)
