#coding=utf-8
import pandas as pd
df = pd.read_csv(r'E:\2022年项目\0621甘孜断面\白玉\All_FromMDB.csv'.decode('utf-8'),encoding='GBK')
df2 = df.groupby('RiverName')
cnList = []
for name,group in df2:
    # print len(group.index)
    i = 1
    for index,value in group.iterrows():
        cn = [name,i,round(value['x'],3),round(value['y'],3),round(value['h'],2), + len(group.index)]
        i+=1
        cnList.append(cn)
df3 = pd.DataFrame(cnList, columns=['RN', 'Num', 'x', 'y', 'h','NumOfDmd_MDB'])
df3.to_csv(r'E:\2022年项目\0621甘孜断面\白玉\对比表.csv'.decode('utf-8'),encoding='gbk', index=False)