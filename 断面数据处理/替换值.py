#coding=utf-8
import matplotlib.pyplot as plt
import pandas as pd
import os
import mpl_toolkits.axisartist.axislines as axislines
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
path = r'D:\2021年项目\0512达曲断面\test2\DQ-189.xls'.decode('utf-8')
df = pd.read_excel(path,header = 1)
df.replace('水边(坎下)'.decode('utf-8'),'afdasdfasdf',inplace= True)
df.to_excel( r'D:\2021年项目\0512达曲断面\test2\DQ-189-0.xls'.decode('utf-8'))
