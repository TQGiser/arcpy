# coding=utf-8
import arcpy
import os
import math
def cal_p_m(p,zx):
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
    j = 0
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
            d = (y2 - y1) * x + (x1 - x2) * y + x2 * y1 - x1 * y2
            d2 = (y1 - y2) * x + (x2 - x1) * y + x1 * y2 - x2 * y1
            czx = ((x - x1) * (x1 - x2) + (y - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (x1 - x2) + x1
            czy = ((x - x1) * (x1 - x2) + (y - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (y1 - y2) + y1
            xm = (x1 + x2)/2
            ym = (y2 + y2)/2
            dis = math.sqrt((x - x1) ** 2 + (y - y1) ** 2)
            dis2 = math.sqrt((x - xm) ** 2 + (y - ym) ** 2)
            mdis = m1 + math.sqrt((x1 - czx) ** 2 + (y1 - czy) ** 2)
            czdis = (y2 - y1) * czx + (x1 - x2) * czy + x2 * y1 - x1 * y2
            if x > min(x1, x2) and x < max(x1, x2) or y > min(y1, y2) and y < max(y1, y2) :
                newp = [x1,y1,dis2,d,mdis,x]
                aList.append(newp)
            i +=1
        aListSort = sorted(aList,key=lambda s:s[2])
        npCnList.append(aListSort[0])
        j+=1
    return npCnList
path = r'D:\T'
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True
zxshp =  r'D:\T\zx.shp'
pshp = r'D:\T\p.shp'
spatial_ref = arcpy.Describe(pshp).spatialReference
if '99' in spatial_ref.name:
    xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-99.shp'
elif '102' in spatial_ref.name:
    xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-102.shp'
arcpy.AddField_management(pshp,'县','TEXT')
arcpy.AddField_management(pshp,'乡镇','TEXT')
with arcpy.da.SearchCursor(xzjx,['SHAPE@','XZQMC_1','XZQMC']) as yb:
    for row in yb:
        with arcpy.da.UpdateCursor(pshp,['SHAPE@','县','乡镇']) as yb2:
            for row2 in yb2:
                if row[0].contains(row2[0]):
                    row2[1] = row[1]
                    row2[2] = row[2]
                    yb2.updateRow(row2)
pMList = cal_p_m(pshp,zxshp)
arcpy.AddField_management(pshp,'M','DOUBLE')
arcpy.AddField_management(pshp,'D','DOUBLE')
with arcpy.da.UpdateCursor(pshp,['SHAPE@X','M','D']) as yb:
    for row in yb:
        for cn in pMList:
            if row[0] == cn[5]:
                row[1] = cn[4]
                row[2] = cn[3]
                yb.updateRow(row)