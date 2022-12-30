# coding=utf-8
import os
import pandas as pd
path = r'E:\2022年项目\0707沙朗沟断面\slg\csv'.decode('utf-8')
os.chdir(path)
lst = []
for i,v,m in os.walk(path):
    for xls in m:
        lst.append(os.path.join(i, xls))
cnList = []
for csv in lst:
    df = pd.read_csv(csv)
    # print df
    i=1
    for index,value in df.iterrows():
        a = i,df.iloc[index,1],df.iloc[index,4],'',df.iloc[index,3],df.iloc[index,2],df.iloc[index,0]
        i+=1
        cnList.append(a)
df = pd.DataFrame(cnList,columns=['dh','dis','elev','bz','y','x','dmh'])
df.to_excel(path + '\\' + 'all.xlsx',index = False)
