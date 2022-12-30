# coding=utf-8
import pandas as pd
import matplotlib
import math
path = r'D:\2021年项目\0425热曲断面\process\rqdmall.xls'.decode('utf-8')
df = pd.read_excel(path)
df.drop(['OBJECTID','dm','lc','QD'],axis=1,inplace=True)
df.rename(columns={'elev':'高程','岸别':'备注','pj':'另点距','X':'Y','Y':'X'},inplace=True)
df['点号'] = 0
# df = df[['点号','另点距','高程','备注','X','Y']]
print(df)