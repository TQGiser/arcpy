#coding=utf-8
import arcpy
import os
import pandas as pd
import F
path = r'E:\2021年项目\1223管理范围线提取\划界成果\湖泊管理范围线、桩牌'
arcpy.env.workspace = path
dmals = F.listFiles(path,'','x')
xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-99.shp'
df = pd.read_excel(r'E:\资料\19湖泊信息.xlsx'.decode('utf-8'))
for dmal in dmals:
    print dmal
    spatial_ref = arcpy.Describe(dmal).spatialReference
    if '99' in spatial_ref.name:
        xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-99.shp'
    elif '102' in spatial_ref.name:
        xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-102.shp'
    with arcpy.da.SearchCursor(dmal,'SHAPE@') as yb:
        for row in yb:
            with arcpy.da.SearchCursor(xzjx,['SHAPE@','XZQMC_1','XZQDM']) as yb2:
                for row2 in yb2:
                    if row2[0].contains(row[0]):
                        riverName = dmal.encode('utf-8').split('桩牌\\')[1].split('\\范围线')[0]
                        xzq = row2[1].encode('utf-8')
                        pac = row2[2]
                        path2 = r'E:\2021年项目\1223管理范围线提取\甘孜州\19个湖泊'
                        arcpy.CreateFolder_management(path2,riverName)
                        newDmal = path2 + '\\' +riverName + '\\' + '{}.shp'.format((riverName + xzq+ '段'))
                        arcpy.Project_management(dmal,newDmal,out_coor_system="GEOGCS['GCS_China_Geodetic_Coordinate_System_2000',"
                                                                              "DATUM['D_China_2000',SPHEROID['CGCS2000',6378137.0,298.257222101]]"
                                                                              ",PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]",)
                        for name, value in df.iterrows():
                            if riverName.decode('utf-8') in df.loc[name, '湖泊名称'.decode('utf-8')]:
                                sx = df.loc[name, '所在水系'.decode('utf-8')]
                        arcpy.AddField_management(newDmal,'HNNM','TEXT')
                        arcpy.DeleteField_management(newDmal,drop_field="FID_;Entity;Layer;Color;Linetype;Elevation;LineWt;RefName;1")
                        if 'FID_范围线'.decode('utf-8') in [field.name for field in arcpy.ListFields(newDmal)]:
                            arcpy.DeleteField_management(newDmal,drop_field='FID_范围线')
                        arcpy.AddField_management(newDmal,'RIVER','TEXT')
                        arcpy.AddField_management(newDmal,'PAC','LONG')
                        arcpy.AddField_management(newDmal,'SXPCDC','TEXT')
                        arcpy.AddField_management(newDmal,'岸别','TEXT')
                        arcpy.AddField_management(newDmal,'县（区）','TEXT')
                        with arcpy.da.UpdateCursor(newDmal,['SHAPE@','HNNM','RIVER','PAC','SXPCDC','岸别','县（区）']) as yb3:
                            for row3 in yb3:
                                row3[1] = sx
                                row3[2] = riverName
                                row3[3] = pac
                                row3[6] = xzq
                                yb3.updateRow(row3)

