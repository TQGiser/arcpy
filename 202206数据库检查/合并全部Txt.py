# coding=utf-8
import os
import pandas as pd
path = r'E:\2022年项目\0621甘孜断面\白玉'
txtFile = r'E:\2022年项目\0621甘孜断面\道孚\散点目录.txt'.decode('utf-8')
txtList = open(txtFile,'r').readlines()
cnList = []
for txt in txtList:
    XZQ = txt.split('\\',12)[6]
    riverName = txt.split('\\',12)[7]
    CS = txt.split('\\',12)[9]
    # print type(txt)
    # print XZQ,riverName,CS
    txtFile_river = r'{}'.format(txt).replace('\n','').decode('utf-8')
    t = open(txtFile_river,'r').readlines()
    for a in t:
        b = a.replace(' ','')
        try:
            cn = [XZQ,riverName,b.split(',',6)[0],b.split(',',6)[2],b.split(',',6)[3],b.split(',',6)[4]]
        except:
            print riverName
        cnList.append(cn)

df = pd.DataFrame(cnList, columns=['行政区', '河流', 'Num','x','y','h'])
csv = path + '\\' + 'All_FromTXT.csv'
df.to_csv(csv.decode('utf-8'), encoding='gbk', index=False)