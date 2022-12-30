# coding=utf-8
import os
import pandas as pd
import arcpy
import F
import math
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
path = r'E:\2022年项目\1107鲜水河断面\test'
outpath = r'E:\2022年项目\1107鲜水河断面\test\pdf'.decode('utf-8')
arcpy.env.workspace = path
dmx1 = F.listFile(path, '99', 'x')
dmx2 = F.listFile(path, '102', 'x')
dmd = F.listFile(path, 'dmd', 'd')
fidList = []
cnList = []
dmxShapeLength = 0
with arcpy.da.SearchCursor(dmx1, ['SHAPE@', '断面名称', 'FID'], explode_to_points=True) as yb:
    for row in yb:
        x = row[0].centroid.X
        y = row[0].centroid.Y
        z = round(row[0].centroid.Z, 2)
        fid = row[1]
        if fid not in fidList:
            x0 = x
            y0 = y
            fidList.append(fid)
            i = 1
            dmxShapeLength += 1
        dis = round(math.sqrt((x - x0) ** 2 + (y - y0) ** 2), 0)
        dmh = row[1]
        a = int(dmh.replace('鲜水河'.decode('utf-8'), ''))
        cn = [dmh, a, i, dis, z, x0, y0]
        cnList.append(cn)
        i += 1
#
# for cn in cnList:
#     print cn[0], cn[1], cn[2], cn[3], cn[4], cn[5], cn[6]

for j in range(1, dmxShapeLength + 1):
    figure = plt.gcf()
    figure.set_facecolor('white')
    xlst = []
    ylst = []
    dmxList = [a for a in cnList if a[1] == j]
    expression = '"aa" = {}'.format(j)
    elevList = []
    disList =[]
    with arcpy.da.SearchCursor(dmd, ['SHAPE@', 'aa', 'RASTERVALU'], where_clause=expression) as yb:
        for row in yb:
            e = row[0].centroid.X
            n = row[0].centroid.Y
            num = row[1]
            elev = row[2]
            elevList.append(elev)
            x, y = F.LatLon2XY(n,e)
            dis = math.sqrt((x - dmxList[0][6]) ** 2 + (y - dmxList[0][5]) ** 2)
            disList.append(dis)
    elev_sm = (elevList[0] + elevList[1])/2
    # print j,disList[1],disList[0],elev_sm
    fileName = dmxList[0][0]
    for cn in dmxList:
        xlst.append(cn[3])
        ylst.append(cn[4])
        plt.xlabel('点距'.decode('utf-8'))
        plt.ylabel('高程'.decode('utf-8'))
    xmax = max(xlst[2:])
    xmin = min(xlst[2:])
    ymax = max(ylst[2:])
    ymin = min(ylst[2:])
    if ymax - ymin < 10:
        plt.xlim((xmin, xmax))
        plt.ylim((ymin, ymax))
        plt.axis([xmin, xmax, ymin, ymax + 10])
    else:
        plt.xlim((xmin, xmax))
        plt.ylim((ymin, ymax))
        plt.axis([xmin, xmax, ymin, ymax])
    pic = outpath + '\\' + fileName + '.pdf'
    plt.title('%s' % fileName)
    plt.plot(xlst[1:], ylst[1:], color='red', label='地面线'.decode('utf-8'))
    plt.plot([disList[1],disList[0]], [elev_sm,elev_sm], color='blue', label='现实水位线'.decode('utf-8'))
    plt.legend(loc='best', fontsize='medium')
    plt.grid(linestyle=':', color='b')
    plt.show()
    figure.savefig(pic, dpi=800)
    j+=1
