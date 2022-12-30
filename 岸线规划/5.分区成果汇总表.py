# coding=utf-8
import arcpy
import os
import math
import pandas as pd
import F
path = r'E:\2021年项目\1222岸线规划\定曲'
arcpy.env.workspace = path
glq = F.listFile(path,'功能区'.decode('utf-8'),'m')
dmal = F.listFile(path,'管理范围线'.decode('utf-8'),'x')
riverName = arcpy.Describe(dmal).baseName.replace('管理范围线'.decode('utf-8'),'')
spatial_ref = arcpy.Describe(glq).spatialReference
if '99' in spatial_ref.name:
    xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-99.shp'
elif '102' in spatial_ref.name:
    xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-102.shp'
groupCn = []
with arcpy.da.SearchCursor(glq,['SHAPE@','BH','AB','Name','According']) as yb:
    for row in yb:
        print row[1]
        dmalList = []
        with arcpy.da.SearchCursor(dmal,'SHAPE@') as dmals:
            for line in dmals:
                if not line[0].disjoint(row[0]):
                    clipLine = row[0].intersect(line[0],2)
                    with arcpy.da.SearchCursor(xzjx,['SHAPE@','XZQMC_1','XZQMC']) as yb2:
                        for row2 in yb2:
                            if row2[0].crosses(clipLine):
                                clipLine2 = row2[0].intersect(clipLine,2)
                                lenth = clipLine2.length
                                xq2 = row2[1] + row2[2]
                                cn = [row[1],row2[1],row[3],row2[2],lenth,xq2]
                                groupCn.append(cn)
                            elif row2[0].contains(clipLine):
                                lenth = clipLine.length
                                xq2 = row2[1] + row2[2]
                                cn = [row[1],row2[1],row[3],row2[2],lenth,xq2]
                                groupCn.append(cn)
df = pd.DataFrame(groupCn,columns=['a','b','c','d','e','f'])
groupCn2 = []
title1 = ['按区县分','','','','','']
groupCn2.append(title1)
for name,group in df.groupby('b'):
    xz = name
    allcount = group['a'].count()
    allLength = round((group['e'].sum())/1000.0,2)
    bhqcount = group[group['c'] == u'岸线保护区']['a'].count()
    bhqLength = round((group[group['c'] == u'岸线保护区']['e'].sum())/1000.0,2)
    bhqPercent = '{:.2f}%'.format(((group[group['c'] == u'岸线保护区']['e'].sum())/(group['e'].sum())*100))
    blqcount = group[group['c'] == u'岸线保留区']['a'].count()
    blqLength = round((group[group['c'] == u'岸线保留区']['e'].sum())/1000.0,2)
    blqPercent ='{:.2f}%'.format(((group[group['c'] == u'岸线保留区']['e'].sum())/(group['e'].sum())*100))
    kzlyqcount = group[group['c'] == u'岸线控制利用区']['a'].count()
    kzlyqLength = round((group[group['c'] == u'岸线控制利用区']['e'].sum())/1000.0,2)
    kzlyqPercent ='{:.2f}%'.format(((group[group['c'] == u'岸线控制利用区']['e'].sum())/(group['e'].sum())*100))
    kflyqcount = group[group['c'] == u'岸线开发利用区']['a'].count()
    kflyqLength = round((group[group['c'] == u'岸线开发利用区']['e'].sum()) / 1000.0, 2)
    kflyqPercent = '{:.2f}%'.format(((group[group['c'] == u'岸线开发利用区']['e'].sum()) / (group['e'].sum()) * 100))
    cn = [xz,allcount,allLength,bhqcount,bhqLength,bhqPercent,blqcount,blqLength,blqPercent,kzlyqcount,kzlyqLength,kzlyqPercent,kflyqcount,kflyqLength,kflyqPercent]
    groupCn2.append(cn)
title2 = ['按乡镇统计']
space = ['']
groupCn2.append(space)
groupCn2.append(title2)
for name,group in df.groupby('f'):
    xz = name
    allcount = group['a'].count()
    allLength = round((group['e'].sum())/1000.0,2)
    bhqcount = group[group['c'] == u'岸线保护区']['a'].count()
    bhqLength = round((group[group['c'] == u'岸线保护区']['e'].sum())/1000.0,2)
    bhqPercent = '{:.2f}%'.format(((group[group['c'] == u'岸线保护区']['e'].sum())/(group['e'].sum())*100))
    blqcount = group[group['c'] == u'岸线保留区']['a'].count()
    blqLength = round((group[group['c'] == u'岸线保留区']['e'].sum())/1000.0,2)
    blqPercent ='{:.2f}%'.format(((group[group['c'] == u'岸线保留区']['e'].sum())/(group['e'].sum())*100))
    kzlyqcount = group[group['c'] == u'岸线控制利用区']['a'].count()
    kzlyqLength = round((group[group['c'] == u'岸线控制利用区']['e'].sum())/1000.0,2)
    kzlyqPercent ='{:.2f}%'.format(((group[group['c'] == u'岸线控制利用区']['e'].sum())/(group['e'].sum())*100))
    kflyqcount = group[group['c'] == u'岸线开发利用区']['a'].count()
    kflyqLength = round((group[group['c'] == u'岸线开发利用区']['e'].sum()) / 1000.0, 2)
    kflyqPercent = '{:.2f}%'.format(((group[group['c'] == u'岸线开发利用区']['e'].sum()) / (group['e'].sum()) * 100))
    cn = [xz,allcount,allLength,bhqcount,bhqLength,bhqPercent,blqcount,blqLength,blqPercent,kzlyqcount,kzlyqLength,kzlyqPercent,kflyqcount,kflyqLength,kflyqPercent]
    groupCn2.append(cn)
df2 = pd.DataFrame(groupCn2,columns=['县（区）','功能区个数','长度',
                           '保护区个数','长度','占比',
                           '保留区个数','长度','占比',
                           '控制利用区个数','长度','占比',
                           '开发利用区个数','长度','占比'])
xlsx = path + '\\' + '{}县区占比表.xlsx'.format(riverName.encode('utf-8'))
df2.to_excel(xlsx.decode('utf-8'),index=False)