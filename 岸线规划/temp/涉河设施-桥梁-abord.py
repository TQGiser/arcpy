#coding=utf-8
import arcpy
import pandas as pd
import math
import os
arcpy.env.overwriteOutput = True
path = r'D:\Test'
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
shss = listFile(path, '设施'.decode('utf-8'), 'm')
zx = listFile(path,'中线'.decode('utf-8'),'x')
dmal = listFile(path,'DMAL','x')
zxcn_lst = []
with arcpy.da.SearchCursor(zx,['OID@','SHAPE@X','SHAPE@Y','SHAPE@M'],explode_to_points = True) as yb:
    for row in yb:
        cn = [row[1],row[2],row[3]]
        zxcn_lst.append(cn)
cnList = []
with arcpy.da.SearchCursor(shss, ['SHAPE@', 'type', 'name', 'FID','SHAPE@X','SHAPE@Y'])as yb:
    for row in yb:
        if row[1] == '公路桥'.decode('utf-8'):
            for part in row[0]:
                i = 0
                for pnt in part:
                    cn = [pnt.X, pnt.Y,row[2],row[3],i,row[0].centroid.X,row[0].centroid.Y]
                    cnList.append(cn)
                    i +=1
pointListAll = list(set([cn[3] for cn in cnList]))
qCnList = []
for i in pointListAll:
    pAll = []
    cnGroup = [cn for cn in cnList if cn[3] == i]
    p1 = [sorted(cnGroup, key=lambda s: s[0])[-1][0],sorted(cnGroup, key=lambda s: s[0])[-1][1],sorted(cnGroup, key=lambda s: s[0])[-1][4],sorted(cnGroup, key=lambda s: s[0])[-1][3]]
    p2 = [sorted(cnGroup, key=lambda s: s[0])[0][0],sorted(cnGroup, key=lambda s: s[0])[0][1],sorted(cnGroup, key=lambda s: s[0])[0][4],sorted(cnGroup, key=lambda s: s[0])[0][3]]
    p3 = [sorted(cnGroup, key=lambda s: s[1])[-1][0],sorted(cnGroup, key=lambda s: s[1])[-1][1],sorted(cnGroup, key=lambda s: s[1])[-1][4],sorted(cnGroup, key=lambda s: s[1])[-1][3]]
    p4 = [sorted(cnGroup, key=lambda s: s[1])[0][0],sorted(cnGroup, key=lambda s: s[1])[0][1],sorted(cnGroup, key=lambda s: s[1])[0][4],sorted(cnGroup, key=lambda s: s[1])[0][3]]
    pAll.append(p1)
    pAll.append(p2)
    pAll.append(p3)
    pAll.append(p4)
    pAllSorted = sorted(pAll,key=lambda s:s[2])
    x1 = pAllSorted[0][0]
    y1 = pAllSorted[0][1]
    x2 = pAllSorted[1][0]
    y2 = pAllSorted[1][1]
    x3 = pAllSorted[2][0]
    y3 = pAllSorted[2][1]
    dis1 = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    dis2 = math.sqrt((x2-x3)**2 + (y2-y3)**2)
    if dis1>dis2:
        wide = dis2
        length = dis1
    else:
        wide = dis1
        length = dis2
    qCn = [cnGroup[0][2],round(wide,1),round(length,1),cnGroup[0][5],cnGroup[0][6],cnGroup[0][3]]
    qCnList.append(qCn)
sxyCnList = []
for cn in qCnList:
    qM = cal_M_AB(cn[3],cn[4],zx=zxcn_lst)
    xyCnX = cal_xy_byM(qM[0]-200,zxcn_lst)[0]
    xyCnY = cal_xy_byM(qM[0]-200,zxcn_lst)[1]
    syCnX = cal_xy_byM(qM[0] + 200,zxcn_lst)[0]
    syCnY = cal_xy_byM(qM[0] + 200, zxcn_lst)[1]
    sxyCn = [xyCnX,xyCnY,syCnX,syCnY,cn[0],cn[3],cn[4],cn[5]]
    sxyCnList.append(sxyCn)
bankL = []
bankR = []
i = 0
with arcpy.da.SearchCursor(dmal,['OID@','SHAPE@X','SHAPE@Y','bank'],explode_to_points = True) as yb:
    for row in yb:
        if int(row[3]) == 0:
            cnLBank  = [row[1],row[2],i]
            bankL.append(cnLBank)
            i +=1
i = 0
with arcpy.da.SearchCursor(dmal, ['OID@', 'SHAPE@X', 'SHAPE@Y', 'bank'], explode_to_points=True) as yb:
    for row in yb:
        if int(row[3]) == 1:
            cnRBank = [row[1],row[2],i]
            bankR.append(cnRBank)
            i +=1
QList = []
for cn in sxyCnList:
    Qname = cn[4]
    Qx = cn[5]
    Qy = cn[6]
    QFid = cn[7]
    xyx = cn[0]
    xyy = cn[1]
    syx = cn[2]
    syy = cn[3]
    calMXyList = []
    calMSyList = []
    for cn1 in bankL:
        dis1 = math.sqrt((xyx-cn1[0])**2 + (xyy-cn1[1])**2)
        dis2 = math.sqrt((syx-cn1[0])**2 + (syy-cn1[1])**2)
        calMXy = [cn1[0],cn1[1],cn1[2],dis1]
        calMXyList.append(calMXy)
        calMSy = [cn1[0],cn1[1],cn1[2],dis2]
        calMSyList.append(calMSy)
    calMXyListSorted = sorted(calMXyList,key=lambda s:s[3])
    calMSyListSorted = sorted(calMSyList, key=lambda s: s[3])
    x1 = calMSyListSorted[0][0]
    y1 = calMSyListSorted[0][1]
    m1 = calMSyListSorted[0][2]
    x2 = calMSyListSorted[1][0]
    y2 = calMSyListSorted[1][1]
    m2 = calMSyListSorted[1][2]
    x3 = calMXyListSorted[0][0]
    y3 = calMXyListSorted[0][1]
    m3 = calMXyListSorted[0][2]
    x4 = calMXyListSorted[1][0]
    y4 = calMXyListSorted[1][1]
    m4 = calMXyListSorted[1][2]
    bankLQd = cal_foot(syx,syy,x1,y1,x2,y2)
    bankLZd = cal_foot(xyx,xyy,x3,y3,x4,y4)
    disCnListL = [cn for cn in bankL if cn[2] >= m4 and cn[2] <m2]
    i = 0
    bankLCnList = []
    for i in range(0,len(disCnListL)-1):
        x1 = disCnListL[i][0]
        y1 = disCnListL[i][1]
        m1 = disCnListL[i][2]
        x2 = disCnListL[i+1][0]
        y2 = disCnListL[i+1][1]
        dis = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        bankLCn = [x1,y1,m1,dis]
        bankLCnList.append(bankLCn)
        i +=1
    blL = sum([a[3] for a in bankLCnList]) + math.sqrt((bankLZd[0] - bankLCnList[0][0])**2 + (bankLZd[1] - bankLCnList[0][1])**2) +\
          math.sqrt((bankLQd[0] - bankLCnList[-1][0])**2 + (bankLQd[1] - bankLCnList[-1][1])**2)
    calMXyList = []
    calMSyList = []
    for cn1 in bankR:
        dis1 = math.sqrt((xyx-cn1[0])**2 + (xyy-cn1[1])**2)
        dis2 = math.sqrt((syx-cn1[0])**2 + (syy-cn1[1])**2)
        calMXy = [cn1[0],cn1[1],cn1[2],dis1]
        calMXyList.append(calMXy)
        calMSy = [cn1[0],cn1[1],cn1[2],dis2]
        calMSyList.append(calMSy)
    calMXyListSorted = sorted(calMXyList,key=lambda s:s[3])
    calMSyListSorted = sorted(calMSyList, key=lambda s: s[3])
    x1 = calMSyListSorted[0][0]
    y1 = calMSyListSorted[0][1]
    m1 = calMSyListSorted[0][2]
    x2 = calMSyListSorted[1][0]
    y2 = calMSyListSorted[1][1]
    m2 = calMSyListSorted[1][2]
    x3 = calMXyListSorted[0][0]
    y3 = calMXyListSorted[0][1]
    m3 = calMXyListSorted[0][2]
    x4 = calMXyListSorted[1][0]
    y4 = calMXyListSorted[1][1]
    m4 = calMXyListSorted[1][2]
    bankRQd = cal_foot(syx,syy,x1,y1,x2,y2)
    bankRZd = cal_foot(xyx,xyy,x3,y3,x4,y4)
    disCnListR = [cn for cn in bankR if cn[2] >= m4 and cn[2] <m2]
    i = 0
    bankRCnList = []
    for i in range(0,len(disCnListR)-1):
        x1 = disCnListR[i][0]
        y1 = disCnListR[i][1]
        m1 = disCnListR[i][2]
        x2 = disCnListR[i+1][0]
        y2 = disCnListR[i+1][1]
        dis = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        bankRCn = [x1,y1,m1,dis]
        bankRCnList.append(bankRCn)
        i +=1
    blR = sum([a[3] for a in bankRCnList]) + math.sqrt((bankRZd[0] - bankRCnList[0][0])**2 + (bankRZd[1] - bankRCnList[0][1])**2) +\
          math.sqrt((bankRQd[0] - bankRCnList[-1][0])**2 + (bankRQd[1] - bankRCnList[-1][1])**2)
    Qcn = [QFid,Qname,Qx,Qy,blL,blR]
    QList.append(Qcn)
df = pd.DataFrame(QList,columns=['FID','Name','X','Y','BankL','BankR'])
df.to_excel(path + '\\' + '桥梁.xlsx'.decode('utf-8'),index=False)