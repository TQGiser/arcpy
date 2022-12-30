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
    np_m = x1_m + math.sqrt((czx - x1) ** 2 + (czy - y2) ** 2)
    return np_m,ab
def cal_p_m(zx,p):
    pCnList = []
    xCnList = []
    npCnList = []
    with arcpy.da.SearchCursor(zx, ['OID@', 'SHAPE@X', 'SHAPE@Y', 'SHAPE@M'], explode_to_points=True) as yb:
        i = 0
        for row in yb:
            cn = [row[1], row[2], row[3], i]
            xCnList.append(cn)
            i += 1
    with arcpy.da.SearchCursor(p, ['SHAPE@X', 'SHAPE@Y']) as yb:
        i = 0
        for row in yb:
            cn = [row[0], row[1], i]
            pCnList.append(cn)
            i += 1
    for cn in pCnList:
        i = 0
        x = cn[0]
        y = cn[1]
        num = cn[2]
        aList = []
        for i in range(0, len(xCnList) - 1):
            x1 = xCnList[i][0]
            y1 = xCnList[i][1]
            m1 = xCnList[i][2]
            x2 = xCnList[i + 1][0]
            y2 = xCnList[i + 1][1]
            if x > min(x1, x2) and x < max(x1, x2) or y > min(y1, y2) and y < max(y1, y2):
                d = (y2 - y1) * x + (x1 - x2) * y + x2 * y1 - x1 * y2
                czx = ((x - x1) * (x1 - x2) + (y - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (x1 - x2) + x1
                czy = ((x - x1) * (x1 - x2) + (y - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (y1 - y2) + y1
                dis = math.sqrt((x - x1) ** 2 + (y - y1) ** 2)
                mdis = m1 + math.sqrt((x1 - czx) ** 2 + (y1 - czy) ** 2)
                a = [x, y, dis, mdis, d]
                aList.append(a)
        i += 1
        aSort = sorted(aList, key=lambda s: s[2])
        npCnList.append(aSort[0])
    return npCnList
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
# coding=utf-8
import arcpy
import os
import math
import pandas as pd
arcpy.env.workspace = r'D:\T'
zx = r'D:\T\zx.shp'
p = r'D:\T\p.shp'
pCnList = []
xCnList = []
arcpy.AddField_management(p,'BANK','TEXT')
arcpy.AddField_management(p,'Lc','LONG')
with arcpy.da.SearchCursor(zx, ['OID@', 'SHAPE@X', 'SHAPE@Y', 'SHAPE@M'], explode_to_points=True) as yb:
    i = 0
    for row in yb:
        cn = [row[1], row[2], row[3], i]
        xCnList.append(cn)
        i += 1
with arcpy.da.UpdateCursor(p,['SHAPE@X','SHAPE@Y','FID','BANK','LC']) as yb :
    for row in yb:
        x = row[0]
        y = row[1]
        num = row[2]
        cnList = []
        i = 0
        for i in range(0, len(xCnList) - 1):
            x1 = xCnList[i][0]
            y1 = xCnList[i][1]
            m1 = xCnList[i][2]
            x2 = xCnList[i + 1][0]
            y2 = xCnList[i + 1][1]
            czx = ((x - x1) * (x1 - x2) + (y - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (x1 - x2) + x1
            czy = ((x - x1) * (x1 - x2) + (y - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (y1 - y2) + y1
            czm = m1 + math.sqrt((czx - x1) ** 2 + (czy - y1) ** 2)
            czdis = (y2 - y1) * czx + (x1 - x2) * czy + x2 * y1 - x1 * y2
            d = (y2 - y1) * x + (x1 - x2) * y + x2 * y1 - x1 * y2
            if czx > min(x1, x2) and czx < max(x1, x2) and czy > min(y1, y2) and czy < max(y1, y2):
                dis = math.sqrt((x - czx) ** 2 + (y - czy) ** 2)
                cn = [num, x1, x2, dis, d, czm]
                cnList.append(cn)
            else:
                dis = math.sqrt((x - x1) ** 2 + (y - y1) ** 2)
                cn = [num, x1, x2, dis, d, czm]
                cnList.append(cn)
            cnSort = sorted(cnList, key=lambda s: s[3])
            i += 1
        if cnSort[0][4] > 0:
            row[3] = 1
        elif cnSort[0][4] < 0:
            row[3] = 0
        row[4] = int(cnSort[0][5])
        yb.updateRow(row)

