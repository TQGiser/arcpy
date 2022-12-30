# coding=utf-8
import arcpy
import os
import math
import pandas as pd
from os.path import join,getsize
path = r'D:\2021年项目\0924预检数据\分幅后数据\125湖泊'.decode('utf-8')
os.chdir(path)
lakeList =[]
for i,v,m in os.walk(path,topdown=True):
    if '-' in i:
        if '县'.decode('utf-8') in i:
            lakeName = i.split('-')[0].split('\\D')[-1].split('\\')[-1]
            if lakeName not in lakeList:
                lakeList.append(lakeName)
for lake in lakeList:
    demfileSize = 0
    demfileNumList = []
    demdirNumList = []
    domfileSize = 0
    domfileNumList = []
    domdirNumList = []
    dlgfileSize = 0
    dlgfileNumList = []
    dlgdirNumList = []
    a = 0
    b = 0
    c = 0
    for i, v, m in os.walk(path, topdown=True):
        if lake in i and 'DEM' in i:
            a += 1
            demfileSize += sum([getsize(join(i, name)) for name in m])
            demfileNumList.append(len(m))
            demdirNumList.append(len(v))
        if lake in i and 'DOM' in i:
            b += 1
            domfileSize += sum([getsize(join(i, name)) for name in m])
            domfileNumList.append(len(m))
            domdirNumList.append(len(v))
        if lake in i and 'DLG' in i:
            c += 1
            dlgfileSize += sum([getsize(join(i, name)) for name in m])
            dlgfileNumList.append(len(m))
            dlgdirNumList.append(len(v))
    # if '月亮湖'.decode('utf-8') in lake:
    #     print lake[0:-4] + '(' + lake[-4:-2] + ')' + ':'
    # elif '五色海'.decode('utf-8') in lake:
    #     print lake[0:-4] + '(' + lake[-4:-2] + ')' + ':'
    # else:
    #     print lake[0:-4] + ':'
    print '1:2000带状数据新测/',lake,'DEM:','{}个文件，'.format(sum(demfileNumList)),'{}个文件夹'.format(a),str('%0.2f'%round((demfileSize/1048576.0),2)) + 'MB' + '。'
    print '1:2000带状数据新测/',lake,'DOM:','{}个文件，'.format(sum(domfileNumList)),'{}个文件夹'.format(b),str('%0.2f'%round((domfileSize/1048576.0),2)) + 'MB'+ '。'
    print '1:2000带状数据新测/',lake,'DLG:','{}个文件，'.format(sum(dlgfileNumList)),'{}个文件夹'.format(c),str('%0.2f'%round((dlgfileSize/1048576.0),2)) + 'MB'+ '。'