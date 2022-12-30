#coding=utf-8
import pandas as pd
import re

pd.set_option('display.width',600)
xlsx = r'E:\2022年项目\0613转坐标\1.xlsx'.decode('utf-8')
df = pd.read_excel(xlsx)
for index,value in df.iterrows():
    e = df.loc[index,'E'].replace(' ','').encode('utf-8')
    n = df.loc[index, 'N'].replace(' ','').encode('utf-8')
    du_e = re.findall(r'\d{2,3}°',e)[0].replace('°','')
    fen_e = re.findall(r'°\d{0,2}\'',e)[0].replace('°','').replace('\'','')
    miao_e = re.findall(r'\'\d{0,3}.',e)[0].replace('\'','').replace('.','')
    miao_xs_e = re.findall(r'.\d{0,10}"',e)[0].replace('.','').replace('"','')
    du_n = re.findall(r'\d{2,3}°',n)[0].replace('°','')
    fen_n = re.findall(r'°\d{0,2}\'',n)[0].replace('°','').replace('\'','')
    miao_n = re.findall(r'\'\d{0,3}.',n)[0].replace('\'','').replace('.','')
    miao_xs_n = re.findall(r'.\d{0,10}"',n)[0].replace('.','').replace('"','')

    sjzdu_e = '%.8f'%(int(du_e) + float(fen_e)/60.0 + (float('0.' + miao_xs_e) + float(miao_e))/3600.0)
    sjzdu_n = '%.8f' % (int(du_n) + float(fen_n) / 60.0 + (float('0.' + miao_xs_n) + float(miao_n)) / 3600.0)
    print sjzdu_e,sjzdu_n
