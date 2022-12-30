#coding=utf-8
import arcpy
import pandas as pd
import math
import os
arcpy.env.overwriteOutput = True
path = r'D:\Test'
def cal_length(xlist):
    i = 0
    dis = 0
    for i in range(0,len(xlist)-1):
        x1 = xlist[i][0]
        y1 = xlist[i][1]
        x2 = xlist[i+1][0]
        y2 = xlist[i+1][1]
        a = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        dis +=a
    return dis
def cal_CZ(xlist,x,y):
    cnList = []
    i = 0
    for i in range(0,len(xlist)-1):
        x1 = xlist[i][0]
        y1 = xlist[i][1]
        num = xlist[i][2]
        x2 = xlist[i + 1][0]
        y2 = xlist[i + 1][1]
        czx = ((x - x1) * (x1 - x2) + (y - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (x1 - x2) + x1
        czy = ((x - x1) * (x1 - x2) + (y - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (y1 - y2) + y1
        if czx > min(x1, x2) and czx < max(x1, x2) and czy > min(y1, y2) and czy < max(y1, y2):
            dis = math.sqrt((x - czx) ** 2 + (y - czy) ** 2)
            cn = [x1, y1, dis,czx, czy,num]
            cnList.append(cn)
        else:
            dis = math.sqrt((x - x1) ** 2 + (y - y1) ** 2)
            cn = [x1, y1, dis,czx, czy,num]
            cnList.append(cn)
        cnSort = sorted(cnList, key=lambda s: s[2])
        i +=1
        Czx = cnSort[0][3]
        Czy = cnSort[0][4]
        pNum = cnSort[0][5]
        sPx = cnSort[0][0]
        sPy = cnSort[0][1]
    return Czx,Czy,pNum,sPx,sPy
def cal_Point_M(zxCnList,x,y,num):
    cnList = []
    i = 0
    for i in range(0,len(zxCnList) - 1):
        x1 = zxCnList[i][0]
        y1 = zxCnList[i][1]
        m1 = zxCnList[i][2]
        x2 = zxCnList[i + 1][0]
        y2 = zxCnList[i + 1][1]
        czx = ((x - x1) * (x1 - x2) + (y - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (x1 - x2) + x1
        czy = ((x - x1) * (x1 - x2) + (y - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (y1 - y2) + y1
        czm = m1 + math.sqrt((czx - x1) ** 2 + (czy - y1) ** 2)
        czdis = (y2 - y1) * czx + (x1 - x2) * czy + x2 * y1 - x1 * y2
        d = (y2 - y1) * x + (x1 - x2) * y + x2 * y1 - x1 * y2
        if czx > min(x1, x2) and czx < max(x1, x2) and czy > min(y1, y2) and czy < max(y1, y2):
            dis = math.sqrt((x - czx) ** 2 + (y - czy) ** 2)
            cn = [num, x1, x2, dis, d, czm,czx,czy]
            cnList.append(cn)
        else:
            dis = math.sqrt((x - x1) ** 2 + (y - y1) ** 2)
            cn = [num, x1, x2, dis, d, czm,czx,czy]
            cnList.append(cn)
        cnSort = sorted(cnList, key=lambda s: s[3])
        i += 1
        Czm = cnSort[0][5]
        Czx = cnSort[0][6]
        Czy = cnSort[0][7]
        D = cnSort[0][4]
    return Czm,Czx,Czy,D
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
shss = listFile(path, '设施'.decode('utf-8'), 'm')
zx = listFile(path,'中线'.decode('utf-8'),'x')
zxCnList = []
with arcpy.da.SearchCursor(zx,['OID@','SHAPE@X','SHAPE@Y','SHAPE@M'],explode_to_points = True) as yb:
    for row in yb:
        cn = [row[1],row[2],row[3]]
        zxCnList.append(cn)
dmal = listFile(path,'DMAL','x')
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
cnList = []
with arcpy.da.SearchCursor(shss, ['SHAPE@', 'type', 'name', 'FID','SHAPE@X','SHAPE@Y'])as yb:
    for row in yb:
        if row[1] == '桥梁'.decode('utf-8'):
            for part in row[0]:
                i = 0
                for pnt in part:
                    cn = [pnt.X, pnt.Y,row[2],row[3],i,row[0].centroid.X,row[0].centroid.Y]
                    cnList.append(cn)
                    i +=1
numList = []
for cn in cnList:
    num = cn[3]
    if num not in numList:
        numList.append(num)

for num in numList:
    Q4PList = []
    pAll = []
    cnGroup = [cn for cn in cnList if cn[3] == num]
    p1 = [sorted(cnGroup, key=lambda s: s[0])[-1][0],sorted(cnGroup, key=lambda s: s[0])[-1][1],sorted(cnGroup, key=lambda s: s[0])[-1][4],sorted(cnGroup, key=lambda s: s[0])[-1][3]]
    p2 = [sorted(cnGroup, key=lambda s: s[0])[0][0],sorted(cnGroup, key=lambda s: s[0])[0][1],sorted(cnGroup, key=lambda s: s[0])[0][4],sorted(cnGroup, key=lambda s: s[0])[0][3]]
    p3 = [sorted(cnGroup, key=lambda s: s[1])[-1][0],sorted(cnGroup, key=lambda s: s[1])[-1][1],sorted(cnGroup, key=lambda s: s[1])[-1][4],sorted(cnGroup, key=lambda s: s[1])[-1][3]]
    p4 = [sorted(cnGroup, key=lambda s: s[1])[0][0],sorted(cnGroup, key=lambda s: s[1])[0][1],sorted(cnGroup, key=lambda s: s[1])[0][4],sorted(cnGroup, key=lambda s: s[1])[0][3]]
    p1x = p1[0]
    p1y = p1[1]
    p1num = p1[2]
    p1d = cal_Point_M(zxCnList,p1x,p1y,p1num)[3]
    p2x = p2[0]
    p2y = p2[1]
    p2num = p2[2]
    p2d = cal_Point_M(zxCnList,p2x,p2y,p2num)[3]
    p3x = p3[0]
    p3y = p3[1]
    p3num = p3[2]
    p3d = cal_Point_M(zxCnList,p3x,p3y,p3num)[3]
    p4x = p4[0]
    p4y = p4[1]
    p4num = p4[2]
    p4d = cal_Point_M(zxCnList,p4x,p4y,p4num)[3]
    cn1 = [p1x,p1y,p1d]
    cn2 = [p2x,p2y,p2d]
    cn3 = [p3x,p3y,p3d]
    cn4 = [p4x,p4y,p4d]
    Q4PList.append(cn1)
    Q4PList.append(cn2)
    Q4PList.append(cn3)
    Q4PList.append(cn4)
    L2Ps = [Qcn for Qcn in Q4PList if Qcn[2] > 0]
    R2Ps = [Qcn for Qcn in Q4PList if Qcn[2] < 0]
    Cz1x = cal_CZ(bankL,L2Ps[0][0],L2Ps[0][1])[0]
    Cz1y = cal_CZ(bankL, L2Ps[0][0], L2Ps[0][1])[1]
    Cz1Num = cal_CZ(bankL, L2Ps[0][0], L2Ps[0][1])[2]
    sx = cal_CZ(bankL, L2Ps[0][0], L2Ps[0][1])[3]
    sy = cal_CZ(bankL, L2Ps[0][0], L2Ps[0][1])[4]
    Cz2x = cal_CZ(bankL, L2Ps[1][0], L2Ps[1][1])[0]
    Cz2y = cal_CZ(bankL, L2Ps[1][0], L2Ps[1][1])[1]
    ex = cal_CZ(bankL, L2Ps[1][0], L2Ps[1][1])[3]
    ey = cal_CZ(bankL, L2Ps[1][0], L2Ps[1][1])[4]
    Cz2Num = cal_CZ(bankL, L2Ps[1][0], L2Ps[1][1])[2]
    #disPs = sorted([lp for lp in bankL if lp[2]>= min(Cz1Num,Cz2Num)  and lp[2]<= max(Cz1Num,Cz2Num)],key=lambda s:s[2])
    dis1 = math.sqrt((Cz1x - sx)**2 + (Cz1y - sy)**2)
    dis2 = math.sqrt((Cz2x - sx)**2 + (Cz2y - sy)**2)
    dis5 = dis1 + dis2
    Cz3x = cal_CZ(bankR, R2Ps[0][0], R2Ps[0][1])[0]
    Cz3y = cal_CZ(bankR, R2Ps[0][0], R2Ps[0][1])[1]
    Cz3Num = cal_CZ(bankR, R2Ps[0][0], L2Ps[0][1])[2]
    sx2 = cal_CZ(bankR, R2Ps[0][0], R2Ps[0][1])[3]
    sy2 = cal_CZ(bankR, R2Ps[0][0], R2Ps[0][1])[4]
    Cz4x = cal_CZ(bankR, R2Ps[1][0], R2Ps[1][1])[0]
    Cz4y = cal_CZ(bankR, R2Ps[1][0], R2Ps[1][1])[1]
    ex2 = cal_CZ(bankR, R2Ps[1][0], R2Ps[1][1])[3]
    ey2 = cal_CZ(bankR, R2Ps[1][0], R2Ps[1][1])[4]
    Cz2Num = cal_CZ(bankL, L2Ps[1][0], L2Ps[1][1])[2]
    dis3 = math.sqrt((Cz3x - sx2) ** 2 + (Cz3y - sy2) ** 2)
    dis4 = math.sqrt((Cz4x - sx2) ** 2 + (Cz4y - sy2) ** 2)
    dis6 = dis3 + dis4
    print num,dis5,Cz1x,Cz1y,Cz2x,Cz2y

    print num,dis6,Cz3x,Cz3y,Cz4x,Cz4y



