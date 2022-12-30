# coding=utf-8
import pandas as pd
import matplotlib
import math
path = r'D:\2021年项目\0425热曲断面\dmd.xls'.decode('utf-8')
df = pd.read_excel(path)
df['pj'] = 0
df2 = df.groupby('dm')
for name,group in df2:
    x0 = group[group['QD'] == '起点'.decode('utf-8')]['X']
    y0 = group[group['QD'] == '起点'.decode('utf-8')]['Y']
    for index,value in group.iterrows():
        value['pj'] = math.sqrt((value['X'] - x0) ** 2 + (value['Y'] - y0) ** 2)
        df.loc[index, 'pj'] = value['pj']
df3 = df.groupby('dm')
for name,group in df3:
    df4 = group
    df4.sort_values(by = 'pj',ascending= True,inplace = True)
    dms = pd.Series(name)
    df5 = pd.concat([dms,df4],ignore_index= True)
    filename = r'D:\2021年项目\0425热曲断面\process'.decode('utf-8') + '\\' + name + '.xls'
    df5.to_excel(filename, index=False)
df.sort_values(by = ['dm','pj'],ascending= True,inplace = True)
allfile = r'D:\2021年项目\0425热曲断面\process'.decode('utf-8') + '\\' + 'rqdmall' +'.xls'
df.to_excel(allfile, index=False)