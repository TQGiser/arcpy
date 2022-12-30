#coding=utf-8
import arcpy
import os
import pandas as pd
import F
arcpy.env.overwriteOutput = True
path = r'E:\2022年项目\0119交煤田\OK\湖泊'
arcpy.env.workspace = path
dmaas = F.listFiles(path,'','m')
for dmaa in dmaas:
    spatial_ref = arcpy.Describe(dmaa).basename
    if '99' in spatial_ref:
        xzjx = r'D:\资料\甘孜乡镇\甘孜县界-99.shp'
    elif '102' in spatial_ref:
        xzjx = r'D:\资料\甘孜乡镇\甘孜县界-102.shp'
    try:
        arcpy.AddField_management(dmaa,'XZQDM','TEXT')
        arcpy.DeleteField_management(dmaa,'ID')
    except:
        pass
    with arcpy.da.UpdateCursor(dmaa,['SHAPE@','NAME','XZQDM']) as yb:
        for row in yb:
            with arcpy.da.SearchCursor(xzjx,['SHAPE@','XZQDM','XZQMC']) as yb2:
                for row2 in yb2:
                    if row2[0].contains(row[0]):
                        print row[1],row2[2],row2[1]
                        row[2] = row2[1]
                        yb.updateRow(row)
