#coding=utf-8
import arcpy
import pandas as pd
import math
import os
import F
arcpy.env.overwriteOutput = True
path = r'E:\2021年项目\1222岸线规划\定曲'
arcpy.env.workspace = path
xlsx = arcpy.ListFiles('*总表.xlsx')
p_cn = []
dfForP = pd.read_excel(path.decode('utf-8') + '\\' + xlsx[0])
for index, value in dfForP.iterrows():
    cn = [value['面中心X'.decode('utf-8')],
          value['面中心Y'.decode('utf-8')],
          value['编号'.decode('utf-8')],
          value['县级行政区'.decode('utf-8')],
          value['功能区类型'.decode('utf-8')],
          value['主要划分依据'.decode('utf-8')],
          value['岸别'.decode('utf-8')],
          value['FID'],
          value['岸线长度(km)'.decode('utf-8')],
          ]
    p_cn.append(cn)
point = arcpy.Point()
pointList = []
for p in p_cn:
    point.X = p[0]
    point.Y = p[1]
    pg = arcpy.PointGeometry(point)
    pointList.append(pg)
p = arcpy.CopyFeatures_management(pointList,path + '\\' + 'glqPoint.shp')
centerMeridian = float(dfForP['起点坐标(经度）'.decode('utf-8')].mean())

if centerMeridian <100.5:
    arcpy.DefineProjection_management(p, coor_system='4542')
    print '中央经线：{},99度带'.format(centerMeridian)
elif centerMeridian >100.5 and centerMeridian < 103.5:
    arcpy.DefineProjection_management(p, coor_system='4543')
    print '中央经线：{},102度带'.format(centerMeridian)
elif centerMeridian >103.5 :
    arcpy.DefineProjection_management(p, coor_system='4544')
    print '中央经线：{},105度带'.format(centerMeridian)
try:
    arcpy.AddField_management(p,'Name','TEXT')
    arcpy.AddField_management(p,'County','TEXT')
    arcpy.AddField_management(p,'Type','TEXT')
    arcpy.AddField_management(p,'According','TEXT')
    arcpy.AddField_management(p,'Bank','TEXT')
    arcpy.AddField_management(p,'Num','TEXT')
    arcpy.AddField_management(p,'Lenth','TEXT')
except:
    pass

with arcpy.da.UpdateCursor(p,['SHAPE@X','Name','County','Type','According','Bank','Num','Lenth']) as yb:
    for row in yb:
        for cn in p_cn:
            if round(row[0],1) ==round(cn[0],1):
                row[1] = cn[2]
                row[2] = cn[3]
                row[3] = cn[4]
                row[4] = cn[5]
                row[5] = cn[6]
                row[6] = cn[7]
                row[7] = '%0.2f'%round(cn[8],2)

        yb.updateRow(row)
glqAera = F.listFile(path,'功能区'.decode('utf-8'),'m')
arcpy.AddField_management(glqAera,'BH','TEXT')
arcpy.AddField_management(glqAera,'AB','TEXT')
arcpy.AddField_management(glqAera,'LENGTH','TEXT')

with arcpy.da.UpdateCursor(glqAera,['SHAPE@','BH','AB','LENGTH']) as yb1:
    for row1 in yb1:
        with arcpy.da.SearchCursor(p,['SHAPE@','Name','Bank','Lenth']) as yb2:
            for row2 in yb2:
                if row1[0].contains(row2[0]):
                    row1[1] = row2[1]
                    row1[2] = row2[2]
                    row1[3] = row2[3]
                    yb1.updateRow(row1)