# coding=utf-8
import arcpy
import pandas as pd
import math
import os
arcpy.env.overwriteOutput = True
path = r'D:\Test'
def listFile(path, keyword, type):
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
    return shp
shss = listFile(path, 'aaa', 'm')
cnList = []
with arcpy.da.SearchCursor(shss, ['SHAPE@', 'type', 'name', 'FID'])as yb:
    for row in yb:
        for part in row[0]:
            for pnt in part:
                cn = [pnt.X, pnt.Y,row[2],row[3]]
                cnList.append(cn)
df = pd.DataFrame(cnList,columns=['X','Y','name','FID'])
for name,group in df.groupby('FID'):
    cn2List = []
    for index,value in group.iterrows():
        cn2 = [value['X'],value['Y'],name,value['name']]
        cn2List.append(cn2)



    # fwjList = [0]
    # i = 0
    # for i in range(0, len(cn2List)-1):
    #     a = float(cn2List[i][0]) - float(cn2List[i + 1][0])
    #     b = float(cn2List[i][1]) - float(cn2List[i + 1][1])
    #     if a > 0 and b > 0:
    #         angle = 180 * math.atan(abs(a) / abs(b)) / math.pi
    #     if a > 0 and b < 0:
    #         angle = 180 * math.atan(abs(a) / abs(b)) / math.pi + 90
    #     if a < 0 and b > 0:
    #         angle = 180 * math.atan(abs(a) / abs(b)) / math.pi + 270
    #     if a < 0 and b < 0:
    #         angle = 180 * math.atan(abs(a) / abs(b)) / math.pi + 180
    #     intersectionAngle = angle - fwjList[-1]
    #     fwjList.append(angle)
    #     if  abs(intersectionAngle)>0.5 and angle != intersectionAngle:
    #         print cn2List[i][0],cn2List[i][1],cn2List[i][2],cn2List[i][3],intersectionAngle,angle
    #     i +=1
    # fwjList = [0]
    # i = 0
    # for i in range(0, len(cnList)-1):
    #     a = float(cnList[i][0]) - float(cnList[i + 1][0])
    #     b = float(cnList[i][1]) - float(cnList[i + 1][1])
    #     if a > 0 and b > 0:
    #         angle = 180 * math.atan(abs(a) / abs(b)) / math.pi
    #     if a > 0 and b < 0:
    #         angle = 180 * math.atan(abs(a) / abs(b)) / math.pi + 90
    #     if a < 0 and b > 0:
    #         angle = 180 * math.atan(abs(a) / abs(b)) / math.pi + 270
    #     if a < 0 and b < 0:
    #         angle = 180 * math.atan(abs(a) / abs(b)) / math.pi + 180
    #     intersectionAngel = angle - fwjList[-1]
    #     fwjList.append(angle)
    #     if  abs(intersectionAngel)>0.5 and angle != intersectionAngel:
    #         print cnList[i][0],cnList[i][1]
    #     i +=1