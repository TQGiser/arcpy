#coding=utf-8
import arcpy
import os
import F
import pandas as pd
df = pd.read_excel(r'E:\测试文件夹\test\1.xlsx'.decode('utf-8'))
for name,value in df.iterrows():
    print df.loc[name,'name'],F.DFM_To_D2((df.loc[name,'n']).encode('utf-8')),F.DFM_To_D2((df.loc[name,'e']).encode('utf-8'))
