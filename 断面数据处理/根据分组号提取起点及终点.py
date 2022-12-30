#coding=utf-8
import xlwt
import pandas as pd
df = pd.read_excel(r'C:\Users\Administrator\Desktop\新建文件夹\A.xls'.decode('utf-8'))
df2 = df.groupby('dmh')
df3 = pd.DataFrame({'X':[],'Y':[],'DMH':[]})
for name,group in df2:
    x1 = group.loc[group['点号'.decode('utf-8')].min(), 'X']
    y1 = group.loc[group['点号'.decode('utf-8')].min(), 'Y']
    x2 = group.loc[group['点号'.decode('utf-8')].max()-1,'X']
    y2 = group.loc[group['点号'.decode('utf-8')].max()-1, 'Y']
    dmh = 'RQ-' + str('%03.0f'%(name -1))
    for index,value in df3.iterrows():
        df3[index,'X'] = x1
        df3[index,'Y'] = y1
        df3[index,'DMH'] = dmh
print df3