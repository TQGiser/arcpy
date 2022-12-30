#coding=utf-8
import arcpy
import os
import pandas as pd
import F
df = pd.read_excel(r'E:\2021年项目\1216生断面\t.xlsx'.decode('utf-8'))
df2 = df.groupby('dmh')
i = 0
for name,group in df2:
    print 'BEGIN',name
    for index,value in group.iterrows():
        print round((df.iloc[index,3] - group.iloc[0,3]),1),round(df.iloc[index,1],2)