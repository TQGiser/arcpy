# coding=utf-8
import arcpy
import os
import math
import pandas as pd
pd.set_option('display.width',1000)
import F
path = r'E:\2021年项目\1117康定划界成果\xls'.decode('utf-8')
arcpy.env.workspace = r'E:\2021年项目\1025康定划界\aaa'
xlsList = []
for i,v,m in os.walk(path):
    for xls in m:
        xlsList.append(os.path.join(i, xls))
for xls in xlsList:
    df = pd.read_excel(xls,header=0)
    df.columns = ['A','B','C','D','E','F','G', 'H','I']
    i = 0
    for name,value in df.iterrows():
        if type(df.loc[name,'I']) == unicode:
            if '实体桩'.decode('utf-8') in df.loc[name,'I']:
                i+=1
                riverName = (df.loc[name, 'A']).split('-')[0]
    if not i == 0:

        with arcpy.da.SearchCursor(r'E:\2021年项目\1025康定划界\aaa\康定市实体桩及告示牌预设.shp',['河流名称','桩名']) as yb:
            a = 0
            for row in yb:
                if riverName in row[1]:
                    a+=1
        print riverName,i,a