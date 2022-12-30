#coding=utf-8
import arcpy
import pandas as pd
import math
import os
def listFiles(path, keyword, type):
    shps = []
    arcpy.env.workspace = path
    if type == 'd':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Point')
    elif type == 'x':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Polyline')
    elif type == 'm':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Polygon')
    for path, name, file in walk:
        for a in file:
            if keyword in a:
                shp = os.path.join(path, a)
                shps.append(shp)
    return shps
path = r'E:\2021年项目\1019甘孜州全部河流点转线'
shps = listFiles(path,'','d')
for shp in shps:
    xName =  shp.split('.')[0].split('\\')[4]
    riverName = shp.split('.')[0].split('\\')[-1]
    fileName = xName + riverName
    print fileName
    cnList = []
    with arcpy.da.SearchCursor(shp,'SHAPE@') as yb:
        for row in yb:
            pcn = [row[0].centroid.X,row[0].centroid.Y]
            cnList.append(pcn)
    Lines = []
    Lines.append(arcpy.Polyline(arcpy.Array([arcpy.Point(*cn) for cn in cnList])))
    shp = arcpy.CopyFeatures_management(Lines, r'E:\2021年项目\1019甘孜州全部河流点转线\甘孜州河流里程表转shp成果\lines' + '\\' + '{}.shp'.format(fileName.encode('utf-8')))
    arcpy.AddField_management(shp,'NAME','TEXT')
    with arcpy.da.UpdateCursor(shp,'NAME') as yb:
        for row2 in yb:
            row2[0] = fileName
            yb.updateRow(row2)






