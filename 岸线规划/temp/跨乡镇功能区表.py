# coding=utf-8
import arcpy
import os
import math
import pandas as pd
import F
path = r'E:\2021年项目\1215许曲岸线规划'
arcpy.env.workspace = path
glq = F.listFile(path,'功能区'.decode('utf-8'),'m')
dmal = F.listFile(path,'管理范围线'.decode('utf-8'),'x')
dmal2 = F.listFile(path,'两年一遇'.decode('utf-8'),'x')
zx = F.listFile(path,'校正后中线'.decode('utf-8'),'x')
spatial_ref = arcpy.Describe(glq).spatialReference
if '99' in spatial_ref.name:
    xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-99.shp'
    fdh = 99
elif '102' in spatial_ref.name:
    xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-102.shp'
    fdh = 102
zxcn_lst = []
with arcpy.da.SearchCursor(zx, ['OID@', 'SHAPE@X', 'SHAPE@Y', 'SHAPE@M'], explode_to_points=True) as yb:
    i = 0
    for row in yb:
        cn = [row[1], row[2], row[3]]
        zxcn_lst.append(cn)
groupCn = []
i = 0
with arcpy.da.SearchCursor(glq,['SHAPE@','BH','AB','Name','According']) as yb:
    for row in yb:
        dmalList = []
        with arcpy.da.SearchCursor(dmal,'SHAPE@') as dmals:
            for line in dmals:
                if not line[0].disjoint(row[0]):
                    clipLine = row[0].intersect(line[0],2)
                    with arcpy.da.SearchCursor(xzjx,['SHAPE@','XZQMC_1','XZQMC']) as yb2:
                        for row2 in yb2:
                            if row2[0].crosses(clipLine):
                                clipLine2 = row2[0].intersect(clipLine,2)
                                p1 = [clipLine2.firstPoint.X, clipLine2.firstPoint.Y]
                                p2 = [clipLine2.lastPoint.X, clipLine2.lastPoint.Y]
                                m1 = F.cal_M_AB(p1[0], p1[1], zxcn_lst)[0]
                                m2 = F.cal_M_AB(p2[0], p2[1], zxcn_lst)[0]
                                county = row2[1] + row2[2]
                                bh = row[1]
                                ab = row[2]
                                name = row[3]
                                according = row[4]
                                if m1 < m2:
                                    qd = p1
                                    zd = p2
                                elif m1 > m2:
                                    qd = p2
                                    zd = p1
                                qdE = F.XY2LatLon(qd[0], qd[1], fdh)[1]
                                qdN = F.XY2LatLon(qd[0], qd[1], fdh)[0]
                                zdE = F.XY2LatLon(zd[0], zd[1], fdh)[1]
                                zdN = F.XY2LatLon(zd[0], zd[1], fdh)[0]
                                qdM = 'K' + str(int(F.cal_M_AB(qd[0], qd[1], zxcn_lst)[0] / 1000.0)) + '+' + '%03d' % (
                                        F.cal_M_AB(qd[0], qd[1], zxcn_lst)[0] % 1000)
                                zdM = 'K' + str(int(F.cal_M_AB(zd[0], zd[1], zxcn_lst)[0] / 1000.0)) + '+' + '%03d' % (
                                        F.cal_M_AB(zd[0], zd[1], zxcn_lst)[0] % 1000)
                                lenth = clipLine2.length
                                cn = [county, bh, ab, name, according, lenth, qdE, qdN, zdE, zdN, qdM, zdM]
                                # print county, bh, ab, name, according, lenth, qdE, qdN, zdE, zdN, qdM, zdM
                                dmalList.append(cn)
        dmal2List = []
        with arcpy.da.SearchCursor(dmal2,'SHAPE@') as dmals:
            for line in dmals:
                if not line[0].disjoint(row[0]):
                    clipLine = row[0].intersect(line[0],2)
                    with arcpy.da.SearchCursor(xzjx,['SHAPE@','XZQMC_1','XZQMC']) as yb2:
                        for row2 in yb2:
                            if row2[0].crosses(clipLine):
                                clipLine2 = row2[0].intersect(clipLine,2)
                                p1 = [clipLine2.firstPoint.X, clipLine2.firstPoint.Y]
                                p2 = [clipLine2.lastPoint.X, clipLine2.lastPoint.Y]
                                m1 = F.cal_M_AB(p1[0], p1[1], zxcn_lst)[0]
                                m2 = F.cal_M_AB(p2[0], p2[1], zxcn_lst)[0]
                                if m1 < m2:
                                    qd = p1
                                    zd = p2
                                elif m1 > m2:
                                    qd = p2
                                    zd = p1
                                qd2E = F.XY2LatLon(qd[0], qd[1], fdh)[1]
                                qd2N = F.XY2LatLon(qd[0], qd[1], fdh)[0]
                                zd2E = F.XY2LatLon(zd[0], zd[1], fdh)[1]
                                zd2N = F.XY2LatLon(zd[0], zd[1], fdh)[0]
                                cn2 = [qd2E,qd2N,zd2E,zd2N]
                                dmal2List.append(cn2)
        if not len(dmalList) == 0:
            j = 0
            for j in range(len(dmalList)):
                county = dmalList[j][0]
                bh = dmalList[j][1]
                ab = dmalList[j][2]
                name = dmalList[j][3]
                according = dmalList[j][4]
                lenth = dmalList[j][5]
                qdE = dmalList[j][6]
                qdN = dmalList[j][7]
                zdE = dmalList[j][8]
                zdN = dmalList[j][9]
                qdM = dmalList[j][10]
                zdM = dmalList[j][11]
                qd2E = dmal2List[j][0]
                qd2N = dmal2List[j][1]
                zd2E = dmal2List[j][2]
                zd2N = dmal2List[j][3]
                cn3 = [i,'四川省','甘孜藏族自治州',county,bh,ab,name,round(lenth/1000,2),qdE,qdN,zdE,zdN,qd2E,qd2N,zd2E,zd2N,according,qdM,zdM]
                print i,'四川省','甘孜藏族自治州',county,bh,ab,name,round(lenth/1000,2),qdE,qdN,zdE,zdN,qd2E,qd2N,zd2E,zd2N,according,qdM,zdM
                groupCn.append(cn3)
                j += 1
                i+=1

groupCn2 = sorted(groupCn,key=lambda s:s[4])
df = pd.DataFrame(groupCn2,columns=['num', 'pro', 'city', 'county', 'bh', 'ab', 'glq', 'lenth', 'ste', 'stn', 'ene', 'enn','ste2', 'stn2', 'ene2', 'enn2',
                            'according', 'qdM','zdM'])

df.columns = ['序号', '省', '市（地）级行政区', '县级行政区', '编号', '岸别', '功能区类型', '岸线长度(km)',
                  '起点坐标(经度）', '起点坐标(纬度）', '终点坐标(经度）','终点坐标(纬度）',
                  '临水线起点坐标(经度）', '临水线起点坐标(纬度）', '临水线终点坐标(经度）','临水线终点坐标(纬度）',
                   '主要划分依据', '起点桩号','终点桩号']
xlsx = path + '\\' + '跨乡镇功能区表.xlsx'
df.to_excel(xlsx.decode('utf-8'), index=False)