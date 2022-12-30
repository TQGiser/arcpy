# coding=utf-8
import arcpy
import pandas as pd
import math
import F
pd.set_option('display.width', 500)
path = r'E:\2021年项目\1213拉曲岸线规划'
arcpy.env.workspace = path
dmal = F.listFile(path,'管理范围线'.decode('utf-8'),'x')
zx = F.listFile(path,'校正后中线'.decode('utf-8'),'x')
glqAera = F.listFile(path,'功能区'.decode('utf-8'),'m')
spatial_ref = arcpy.Describe(dmal).spatialReference
if '99' in spatial_ref.name:
    xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-99.shp'
    fdh = 99
elif '102' in spatial_ref.name:
    xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-102.shp'
    fdh = 102
try:
    arcpy.AddField_management(glqAera, 'province', 'TEXT')
    arcpy.AddField_management(glqAera, 'city', 'TEXT')
    arcpy.AddField_management(glqAera, 'county', 'TEXT')
except:
    pass
with arcpy.da.UpdateCursor(glqAera,['SHAPE@','province', 'city', 'county']) as yb1:
    for row1 in yb1:
        with arcpy.da.SearchCursor(xzjx,['SHAPE@','XZQMC_1','XZQMC']) as yb2:
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
    i = 0
    for row in yb:
        cn = [row[1], row[2], row[3]]
        zxcn_lst.append(cn)
cnLst = []
groupCn = []
with arcpy.da.SearchCursor(glqAera, ['SHAPE@', 'Name', 'FID', 'According', 'province', 'city', 'county']) as aeras:
    for aera in aeras:
        id = aera[2]
        glq = aera[1]
        zxX = aera[0].labelPoint.X
        zxY = aera[0].labelPoint.Y
        acording = aera[3]
        prov = aera[4]
        city = aera[5]
        county = aera[6]
        print aera[2]
        for part in aera[0]:
            cnLst = []
            poion_count = 0
            for pnt in part:
                x = pnt.X
                y = pnt.Y
                with arcpy.da.SearchCursor(dmal, 'SHAPE@') as dmals:
                    for line in dmals:
                        if not line[0].disjoint(pnt):
                            cn = [pnt.X, pnt.Y, aera[1], aera[2], poion_count, aera[0].pointCount]
                            if cn not in cnLst:
                                cnLst.append(cn)
                poion_count += 1
            i = 0
            aLst = []
            for cn in cnLst:
                if cn[4] != i:
                    a = i
                    aLst.append(a)
                i += 1
            for cn in cnLst:
                if cn[4] < min(aLst):
                    cn[4] = min(aLst) - cn[4]
                elif cn[4] > min(aLst):
                    cn[4] = aera[0].pointCount - cn[4] + min(aLst)
            cnLst.sort(key=lambda s: s[4])
            a = 0
            lenth = 0
            for a in range(0, len(cnLst) - 1):
                disPart = math.sqrt((cnLst[a][0] - cnLst[a + 1][0]) ** 2 + (cnLst[a][1] - cnLst[a + 1][1]) ** 2)
                lenth += disPart
                a += 1
            p1 = cnLst[0]
            p2 = cnLst[-1]
            m1 = F.cal_M_AB(p1[0], p1[1], zxcn_lst)[0]
            m2 = F.cal_M_AB(p2[0], p2[1], zxcn_lst)[0]
            ab = F.cal_M_AB(p1[0], p1[1], zxcn_lst)[1]
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
            qdM = F.cal_M_AB(qd[0],qd[1],zxcn_lst)[0]
            zdM = F.cal_M_AB(zd[0],zd[1],zxcn_lst)[0]
            cn2 = [0, prov, city, county, 0, ab, glq, round(lenth / 1000.0, 2), qdE, qdN, zdE, zdN, qd[1], qd[0], zd[1],
                   zd[0], acording, id, m1, zxX, zxY,qdM,zdM]
            groupCn.append(cn2)
df = pd.DataFrame(groupCn,
                  columns=['num', 'pro', 'city', 'county', 'bh', 'ab', 'glq', 'lenth', 'ste', 'stn', 'ene', 'enn',
                           'stx', 'sty', 'endx', 'endy', 'according', 'fid', 'lc', 'zxX', 'zxY','qdM','zdM'])
df2 = df.groupby('ab')
df_all = pd.DataFrame(
    columns=['num', 'pro', 'city', 'county', 'bh', 'ab', 'glq', 'lenth', 'ste', 'stn', 'ene', 'enn', 'stx', 'sty',
             'endx', 'endy', 'according', 'fid', 'lc', 'zxX', 'zxY','qdM','zdM'])
for name, group in df2:
    df6 = group
    df6.sort_values(by='lc', ascending=False, inplace=True)
    i = 0
    for i in range(0, len(df6)):
        df6.iloc[i, 4] = df6.iloc[i, 5] + str(i + 1)
        i += 1
    df_all = df_all.append(df6)
df_all.sort_values(by='lc', ascending=False, inplace=True)
i = 0
for index, value in df_all.iterrows():
    df_all.loc[index, 'num'] = str(i)
    i += 1
for index, value in df_all.iterrows():
    if '左' in df_all.loc[index, 'bh']:
        df_all.loc[index, 'bh'] = df_all.loc[index, 'bh'].replace('左岸', 'L')
    elif '右' in df_all.loc[index, 'bh']:
        df_all.loc[index, 'bh'] = df_all.loc[index, 'bh'].replace('右岸', 'R')
df_all.columns = ['序号', '省', '市（地）级行政区', '县级行政区', '编号', '岸别', '功能区类型', '岸线长度(km)', '起点坐标(经度）', '起点坐标(纬度）', '终点坐标(经度）',
                  '终点坐标(纬度）', 'stP_X', 'stP_Y', 'enP_X', 'enP_Y', '主要划分依据', 'FID', 'LC', '面中心X', '面中心Y','起点桩号','终点桩号']
xlsx = path + '\\' + '总表.xlsx'
df_all.to_excel(xlsx.decode('utf-8'), index=False)
