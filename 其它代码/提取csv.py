import pandas as pd
import os
os.walk
os.walk('E:/BaiduNetdiskDownload/站点_20200101-20201231/')
for i, v, m in os.walk('E:/BaiduNetdiskDownload/站点_20200101-20201231/'):
    print(i)
    print(v)
    print(m)
    pass
lst = m
def get_dt(lst):
    for i in lst:
        df = pd.read_csv('E:/BaiduNetdiskDownload/站点_20200101-20201231/' + i)
        dfa = df[['date', 'hour', 'type', '1001A', '1002A', '1003A', '1004A']]
        dfa.to_excel('E:/BaiduNetdiskDownload/exl/' + i.replace('.csv','.xlsx'))
        yield dfa
df_all = pd.concat(get_dt(lst))
df_all.to_excel('E:/BaiduNetdiskDownload/exl/all.xlsx')


