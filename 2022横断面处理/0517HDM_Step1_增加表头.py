# coding=utf-8
import os
import pandas as pd
path = r'E:\2022年项目\0517霍曲横断面\河道断面成果\10000\断面数据成果'.decode('utf-8')
os.chdir(path)
lst = []
for i,v,m in os.walk(path):
    for xls in m:
        lst.append(os.path.join(i, xls))
cnList = []
for xls in lst:
    df= pd.read_excel(xls)
    dmh = df.columns.values[0]
    i = 0
    for index,value in df.iterrows():

        a = i,df.iloc[index-1,0],df.iloc[index-1,1],df.iloc[index-1,4],df.iloc[index-1,5],dmh
        i+=1
        cnList.append(a)
df = pd.DataFrame(cnList,columns=['dh','dis','elev','y','x','dmh'])
df.to_excel(path + '\\' + 'all.xlsx',index = False)
