# coding=utf-8
import os
import pandas as pd
path = r'E:\2022年项目\0518康定河断面\xlsx'.decode('utf-8')
os.chdir(path)
lst = []
for i,v,m in os.walk(path):
    for xls in m:
        lst.append(os.path.join(i, xls))
cnList = []
for xls in lst:
    df= pd.read_excel(xls)
    dmh = df.columns.values[0].split('(')[1].replace(')','')
    # print df.head()
    df2=pd.read_excel(xls,header=1)
    i=1
    for index,value in df2.iterrows():
        dis = float(df2.iloc[index,0].split('+')[1])
        x = float(df2.iloc[index,2])
        y = float(df2.iloc[index,1])
        elev = float(df2.iloc[index,3])
        a = i,dis,elev,y,x,dmh
        i+=1
        cnList.append(a)
df3 = pd.DataFrame(cnList,columns=['dh','dis','elev','y','x','dmh'])
df3.to_excel(path + '\\' + 'all.xlsx',index = False)
