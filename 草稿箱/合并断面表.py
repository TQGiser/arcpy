# coding=utf-8
import arcpy
import os
import math
import pandas as pd
import F
import shutil
path = r'C:\Users\Administrator\Desktop\新建文件夹'.decode('utf-8')
os.chdir(path)
lst = []

for i,v,m in os.walk(path):
    for xls in m:
        lst.append(os.path.join(i, xls))
# for xls in lst:
#     print xls
#     df = pd.read_excel(xls,header=1)
#     for name,value in df.iterrows():
#         if type(df.loc[name,'另点距'.decode('utf-8')]) is unicode:
#             if '-' in df.loc[name,'另点距'.decode('utf-8')]:
#                 dmmc = df.loc[name,'另点距'.decode('utf-8')]
#                 i =0
#         a = [df.loc[name,'Y'],df.loc[name,'X'],df.loc[name,'高程'.decode('utf-8')],i,dmmc]
#         cnList.append(a)
#         i+=1
# df = pd.DataFrame(cnList,columns=['A','B','C','D','E'])
# df.to_excel(path + '\\' + 'all.xlsx',index=False)
# df = pd.read_excel(r'E:\2021年项目\1202理塘断面处理\2\岔若柯.xls'.decode('utf-8'))
cnList = []
for xls in lst:
    print xls
    df = pd.read_excel(xls)
    dmhList = []
    for index,row in df.iterrows():
        # print df.iloc[index,1],type(df.iloc[index,1])

        if type(df.iloc[index,1]) is unicode and '-'.decode('utf-8') in df.iloc[index, 1] :
            dmhList.append(df.iloc[index,1])
        if len(dmhList) >0 :
            a = [df.iloc[index,0],df.iloc[index,1],df.iloc[index,2],df.iloc[index,3],df.iloc[index,4],df.iloc[index,5],dmhList[-1]]
            cnList.append(a)
df = pd.DataFrame(cnList,columns=['A','B','C','D','E','F','G'])
df.to_excel(path + '\\' + 'all.xlsx',index = False)

