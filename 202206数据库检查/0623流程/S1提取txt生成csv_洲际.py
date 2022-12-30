#coding=utf-8
import arcpy
import pandas as pd
import os
path = r'E:\2022年项目\0621甘孜断面\洲际\庆达沟'
txtpath = path + '\\' + 'txt'
outpath = path + '\\' + 'csv'
cnList = []
for i,v,m in os.walk(txtpath.decode('utf-8')):
    for a in m :
        txt = os.path.join(i,a)
        XZQ = txt.split('\\')[6].replace('.txt','')
        riverName = txt.split('\\')[4]
        t = open(txt,'r').readlines()
        for a in t:
            try:
                dm =  a.replace(' ','').split(',')[0]
                zb_x = a.replace(' ','').split(',')[2]
                zb_y = a.replace(' ','').split(',')[3]
                zb_h = a.replace(' ','').split(',')[4]
                cn = [XZQ, riverName, dm, zb_x, zb_y, zb_h]
                cnList.append(cn)
            except:
                print txt
df = pd.DataFrame(cnList, columns=['行政区','河流','Num','x','y','h'])
csv = outpath + '\\' + 'All_FromTXT.csv'
df.to_csv(csv.decode('utf-8'),encoding='gbk',index=False)



