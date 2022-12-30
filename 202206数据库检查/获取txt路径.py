#coding=utf-8
import arcpy
import pandas as pd
import os
path = r'\\192.168.255.12\河湖检查\甘孜藏族自治州\道孚县水利局-20211220'
outpath = r'E:\2022年项目\0621甘孜断面\道孚\csv'
cnList = []
for i,v,m in os.walk(path.decode('utf-8')):
    if '断面数据成果' in i.encode('utf-8'):
        for a in m :
            if '.txt' in a.encode('utf-8'):
                txt = os.path.join(i,a)
                XZQ = txt.split('\\', 12)[6]
                riverName = txt.split('\\', 12)[7]
                t = open(txt,'r').readlines()
                for a in t:
                    b = a.replace(' ', '')
                    try:
                        cn = [XZQ, riverName, b.split(',', 6)[0], b.split(',', 6)[2], b.split(',', 6)[3], b.split(',', 6)[4]]
                    except:
                        print riverName
                    cnList.append(cn)
df = pd.DataFrame(cnList, columns=['行政区', '河流', 'Num','x','y','h'])
csv = outpath + '\\' + 'All_FromTXT.csv'
df.to_csv(csv.decode('utf-8'), encoding='gbk', index=False)



