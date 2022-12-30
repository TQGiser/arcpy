#coding=utf-8
import arcpy
import pandas as pd
import os
path = r'\\192.168.255.12\河湖检查\甘孜藏族自治州\石渠县水利局'
outpath = r'E:\2022年项目\0621甘孜断面\石渠\csv'
cnList = []
for i,v,m in os.walk(path.decode('utf-8')):
    if '断面数据成果' in i.encode('utf-8'):
        for a in m :
            if '.txt' in a.encode('utf-8'):
                txt = os.path.join(i,a)
                XZQ = txt.split('\\', 12)[5]
                riverName = txt.split('\\', 12)[8]
                t = open(txt,'r').readlines()
                print txt
                print XZQ,riverName
                for a in t:
                    try:
                        dm =  a.replace(' ','').split(',')[0]
                        zb_x = a.replace(' ','').split(',')[2]
                        zb_y = a.replace(' ','').split(',')[3]
                        zb_h = a.replace(' ','').split(',')[4]
                        # print txt
                        # print XZQ,riverName,dm,zb_x,zb_y,zb_h
                        cn = [XZQ, riverName, dm, zb_x, zb_y, zb_h]
                        cnList.append(cn)
                    except:
                        print txt
                    # print txt
                    # print XZQ,riverName,dm,zb_x,zb_y,zb_h
                    # b = a.replace(' ', '')
#                     try:
#                         cn = [XZQ, riverName, b.split(',', 6)[0], b.split(',', 6)[2], b.split(',', 6)[3], b.split(',', 6)[4]]
#                     except:
#                         print riverName

df = pd.DataFrame(cnList, columns=['行政区','河流','Num','x','y','h'])
# df.to_excel(r'E:\2022年项目\0621甘孜断面\德格\csv\2.xlsx'.decode('utf-8'),index=False)
csv = outpath + '\\' + 'All_FromTXT.csv'
df.to_csv(csv.decode('utf-8'),encoding='gbk',index=False)



