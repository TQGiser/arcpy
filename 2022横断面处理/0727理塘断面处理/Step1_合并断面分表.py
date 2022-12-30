# coding=utf-8
import os
import pandas as pd
path = r'E:\2022年项目\0815理塘断面表格\xls\99'.decode('utf-8')
os.chdir(path)
lst = []
for i,v,m in os.walk(path):
    for xls in m:
        lst.append(os.path.join(i, xls))
cnList = []
for xls in lst:
    print xls
    df = pd.read_excel(xls)
    dmhList = []
    for index,row in df.iterrows():
        if type(df.iloc[index,1]) is unicode and '-'.decode('utf-8') in df.iloc[index, 1] :
            dmhList.append(df.iloc[index,1])
        if len(dmhList) >0 :
            a = [df.iloc[index,0],df.iloc[index,1],df.iloc[index,2],df.iloc[index,3],df.iloc[index,4],df.iloc[index,5],dmhList[-1]]
            cnList.append(a)
df = pd.DataFrame(cnList,columns=['dh','dis','elev','bz','y','x','dmh'])
df.to_excel(path + '\\' + 'all.xlsx',index = False)
