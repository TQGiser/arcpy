# coding=utf-8
import arcpy
import pandas as pd
import math
import F
pd.set_option('display.width', 500)
path = r'E:\2021年项目\1222岸线规划\达曲'
arcpy.env.workspace = path
dmal = F.listFile(path, '管理范围线'.decode('utf-8'), 'x')
riverName = arcpy.Describe(dmal).baseName.replace('管理范围线'.decode('utf-8'),'')
dmal2 = F.listFile(path, '水位线'.decode('utf-8'), 'x')
zx = F.listFile(path, '校正后中线'.decode('utf-8'), 'x')
glqAera = F.listFile(path, '功能区'.decode('utf-8'), 'm')
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
with arcpy.da.UpdateCursor(glqAera, ['SHAPE@', 'province', 'city', 'county']) as yb1:
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
    i = 0
    for row in yb:
        cn = [row[1], row[2], row[3]]
        zxcn_lst.append(cn)
cnLst = []
groupCn = []
with arcpy.da.SearchCursor(glqAera, ['SHAPE@', 'Name', 'FID', 'According', 'province', 'city', 'county']) as aeras:
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
                    groupCn.append(clipLine)
arcpy.CopyFeatures_management(groupCn,path + '\\' + 'A.shp')
