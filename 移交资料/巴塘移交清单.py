# coding=utf-8
import arcpy
import os
import math
import pandas as pd
from os.path import join,getsize
path = r'E:\2021年项目\1221理塘文件读取\理塘县'.decode('utf-8')
os.chdir(path)
df = pd.read_excel(r'E:\2021年项目\1202理塘2K划界\理塘县73条县级河流长度统计表.xlsx'.decode('utf-8'))
nameList = []
for name,value in df.iterrows():
    nameList.append(df.loc[name,'河流'.decode('utf-8')])

for river in nameList:
    demfileSize = 0
    demfileNumList = []
    demdirNumList = []
    domfileSize = 0
    domfileNumList = []
    domdirNumList = []
    dlgfileSize = 0
    dlgfileNumList = []
    dlgdirNumList = []
    demfileSize2 = 0
    demfileNumList2 = []
    demdirNumList2 = []
    domfileSize2 = 0
    domfileNumList2 = []
    domdirNumList2 = []
    dlgfileSize2 = 0
    dlgfileNumList2 = []
    dlgdirNumList2 = []
    dmfileSize = 0
    dmfileNumList = []
    dmdirNumList = []
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    g = 0
    for i, v, m in os.walk(path, topdown=True):
        if river in i and 'DEM' in i and '10000'.decode('utf-8') in i:
            a += 1
            demfileSize += sum([getsize(join(i, name)) for name in m])
            demfileNumList.append(len(m))
            demdirNumList.append(len(v))
        if river in i and 'DOM' in i and '10000'.decode('utf-8') in i:
            b += 1
            domfileSize += sum([getsize(join(i, name)) for name in m])
            domfileNumList.append(len(m))
            domdirNumList.append(len(v))
        if river in i and 'DLG' in i and '10000'.decode('utf-8') in i:
            c += 1
            dlgfileSize += sum([getsize(join(i, name)) for name in m])
            dlgfileNumList.append(len(m))
            dlgdirNumList.append(len(v))
        if river in i and 'DEM' in i and '2000'.decode('utf-8') in i:
            d += 1
            demfileSize2 += sum([getsize(join(i, name)) for name in m])
            demfileNumList2.append(len(m))
            demdirNumList2.append(len(v))
        if river in i and 'DOM' in i and '2000'.decode('utf-8') in i:
            e += 1
            domfileSize2 += sum([getsize(join(i, name)) for name in m])
            domfileNumList2.append(len(m))
            domdirNumList2.append(len(v))
        if river in i and 'DLG' in i and '2000'.decode('utf-8') in i:
            f += 1
            dlgfileSize2 += sum([getsize(join(i, name)) for name in m])
            dlgfileNumList2.append(len(m))
            dlgdirNumList2.append(len(v))
        if river in i and '河道断面成果'.decode('utf-8') in i:
            g += 1
            dmfileSize += sum([getsize(join(i, name)) for name in m])
            dmfileNumList.append(len(m))
            dmdirNumList.append(len(v))

    print river
    print '1:10000带状数据新测/',river,'DEM:','{}个文件，'.format(sum(demfileNumList)),'{}个文件夹'.format(a),str('%0.2f'%round((demfileSize/1048576.0),2)) + 'MB' + '。'
    print '1:10000带状数据新测/',river,'DOM:','{}个文件，'.format(sum(domfileNumList)),'{}个文件夹'.format(b),str('%0.2f'%round((domfileSize/1048576.0),2)) + 'MB'+ '。'
    print '1:10000带状数据新测/',river,'DLG:','{}个文件，'.format(sum(dlgfileNumList)),'{}个文件夹'.format(c),str('%0.2f'%round((dlgfileSize/1048576.0),2)) + 'MB'+ '。'
    print '1:2000带状数据新测/',river,'DEM:','{}个文件，'.format(sum(demfileNumList2)),'{}个文件夹'.format(d),str('%0.2f'%round((demfileSize2/1048576.0),2)) + 'MB' + '。'
    print '1:2000带状数据新测/',river,'DOM:','{}个文件，'.format(sum(domfileNumList2)),'{}个文件夹'.format(e),str('%0.2f'%round((domfileSize2/1048576.0),2)) + 'MB'+ '。'
    print '1:2000带状数据新测/',river,'DLG:','{}个文件，'.format(sum(dlgfileNumList2)),'{}个文件夹'.format(f),str('%0.2f'%round((dlgfileSize2/1048576.0),2)) + 'MB'+ '。'
    print '河道断面成果/','{}个文件，'.format(sum(dmfileNumList)),'{}个文件夹'.format(g),str('%0.2f'%round((dmfileSize/1048576.0),2)) + 'MB'+ '。'