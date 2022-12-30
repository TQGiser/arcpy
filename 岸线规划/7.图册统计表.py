#coding=utf-8
import arcpy
import os
import pandas as pd
import F
arcpy.env.overwriteOutput = True
path = r'E:\2021年项目\1222岸线规划\定曲'
tk = F.listFile(path,'图框'.decode('utf-8'),'m')
glq = F.listFile(path,'功能区'.decode('utf-8'),'m')
spatial_ref = arcpy.Describe(tk).spatialReference
if '99' in spatial_ref.name:
    xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-99.shp'
    fdh = 99
elif '102' in spatial_ref.name:
    xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-102.shp'
    fdh = 102
cnList = []
with arcpy.da.SearchCursor(tk,['SHAPE@','name']) as yb:
    for row in yb:
        with arcpy.da.SearchCursor(glq, ['SHAPE@', 'county']) as yb2:
            for row2 in yb2:
                if row[0].overlaps(row2[0]):
                    cn = [row[1],row2[1]]
                elif row[0].contains(row2[0]):
                    cn = [row[1], row2[1]]
        cnList.append(cn)

# with arcpy.da.SearchCursor(xzjx,['SHAPE@','XZQMC','XZQMC_1']) as yb3:
#     for row3 in yb3:
#         for shp in tempShps:
#             if row3[0].overlaps(shp[0]):
#                 cn = [shp[1],row3[1],row3[2]]
#                 pass
#             elif row3[0].contains(shp[0]):
#                 cn = [shp[1],row3[1],row3[2]]
#                 pass
#             cnList.append(cn)
cnListSort = sorted(cnList,key=lambda s:s[0])
cn2List = []
i = 1
for cn in cnListSort:
    cn2 = ['规划示意图（{}/{}）'.format(i+3,len(cnListSort)+3),cn[0],cn[1]]
    cn2List.append(cn2)
    i+=1
df = pd.DataFrame(cn2List,columns=['图名','页码','行政区'])
df.to_excel(path.decode('utf-8')+ '\\'+ '页码统考表.xlsx'.decode('utf-8'),index=False)
