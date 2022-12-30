#coding=utf-8
import arcpy
import pandas as pd
import math
import os
arcpy.env.overwriteOutput = True
path = r'D:\2021年项目\0927理塘数据库更新\根据表格生成dmap'
arcpy.env.workspace = path
df = pd.read_excel(r'D:\2021年项目\0927理塘数据库更新\表格\日布沟.xlsx'.decode('utf-8'))
p_cn = []
for name,value in df.iterrows():
    if df.loc[name,'bz'] == '电子桩'.decode('utf-8'):
        GB = 910100
        RuleID = 27
    elif df.loc[name,'bz'] == '实体桩'.decode('utf-8'):
        GB = 910100
        RuleID = 2
    else:
        GB = 910102
        RuleID = 3
    if '左0'.decode('utf-8') in df.loc[name,'name']:
        BANK = 0
    elif '右0'.decode('utf-8') in df.loc[name, 'name']:
        BANK = 1
    else:
        BANK = 9999
    cn = [df.loc[name,'name'],df.loc[name,'x'],df.loc[name,'y'],df.loc[name,'elev'],RuleID,GB,df.loc[name,'num'],BANK]
    p_cn.append(cn)
p = arcpy.CreateFeatureclass_management(path,'日布沟DMAP','POINT')
arcpy.AddField_management(p,'NAME','TEXT')
arcpy.AddField_management(p,'GB','LONG')
arcpy.AddField_management(p,'NUM','TEXT')
arcpy.AddField_management(p,'ELEV','DOUBLE')
arcpy.AddField_management(p,'RuleID','LONG')
arcpy.AddField_management(p,'BANK','TEXT')
yb = arcpy.da.InsertCursor(p,['NAME','SHAPE@X','SHAPE@Y','ELEV','RuleID','GB','NUM','BANK'])
for cn in p_cn:
    yb.insertRow(cn)
del yb