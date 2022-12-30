#coding=utf-8
import xlwt
import pandas as pd
df = pd.read_excel(r'C:\Users\Administrator\Desktop\新建文件夹\达曲河道断面成果表.xls'.decode('utf-8'),header= 1)
df2 = pd.read_excel(r'C:\Users\Administrator\Desktop\新建文件夹\达曲河道断面成果表4.25.xls'.decode('utf-8'),header= 1)
df['dmh'] = 0
df2['dmh'] = 0
a = 1
for index,value in df.iterrows():

    if df.loc[index,'点号'.decode('utf-8')] == 1:
        value['dmh'] = a
        a += 1
    df.loc[index,'dmh'] = a
df.dropna(axis=0,how='any',inplace=True)

a = 1
for index,value in df2.iterrows():
    if df2.loc[index,'点号'.decode('utf-8')] == 1:
        value['dmh'] = a
        a += 1
    df2.loc[index,'dmh'] = a
df2.dropna(axis=0,how='any',inplace=True)

df3 = pd.concat([df,df2],axis=1)
df3.to_excel(r'C:\Users\Administrator\Desktop\新建文件夹\A.xls'.decode('utf-8'))
# 0618处理//////////////////////////////////////////////////////////////////////////////////////
#coding=utf-8
import xlwt
import pandas as pd
df = pd.read_excel(r'D:\2021年项目\0618热曲断面表格处理\新建文件夹\A.xlsx'.decode('utf-8'))
df2 = df.groupby('dmh')
df3 = pd.DataFrame({'X':[],'Y':[],'DMH':[]})
for name,group in df2:
    x1 = group.loc[int(group['点号'.decode('utf-8')].idxmin()), 'X']
    y1 = group.loc[int(group['点号'.decode('utf-8')].idxmin()), 'Y']
    x2 = group.loc[int(group['点号'.decode('utf-8')].idxmax()), 'X']
    y2 = group.loc[int(group['点号'.decode('utf-8')].idxmax()), 'Y']
    print y1,x1,'RQ-' + '%03.0f'%(name-1)
    print y2,x2,'RQ-' + '%03.0f'%(name-1)