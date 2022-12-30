#coding=utf-8
import matplotlib.pyplot as plt
import pandas as pd
import os
import mpl_toolkits.axisartist.axislines as axislines
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
path = r'C:\Users\Administrator\Desktop\wn\ok'.decode('utf-8')
outpath = r'C:\Users\Administrator\Desktop\wn\pdf'.decode('utf-8')
os.chdir(path)
lst = []
for i,v,m in os.walk(path):
    lst=m
for i in range(0,len(lst),4):
    sublocation = 1
    for file in lst[i:i+4]:
        figure = plt.gcf()
        figure.set_facecolor('white')
        df = pd.read_excel(file,header= 1)
        plt.subplot(2, 2, sublocation)
        xlst = []
        ylst = []
        finame = df.loc[0,'另点距'.decode('utf-8')]
        print finame
        for index,value in df.iterrows():
            xlst.append(value.loc['另点距'.decode(('utf-8'))])
            ylst.append(value.loc['高程'.decode('utf-8')])
            plt.xlabel('另点距'.decode('utf-8'))
            plt.ylabel('高程'.decode('utf-8'))
        xmax = max(xlst[2:])
        xmin = min(xlst[2:])
        ymax = max(ylst[2:])
        ymin = min(ylst[2:])
        if ymax - ymin < 10:
            plt.xlim((xmin,xmax))
            plt.ylim((ymin,ymax))
            plt.axis([xmin,xmax,ymin,ymax+10])
        else:
            plt.xlim((xmin, xmax))
            plt.ylim((ymin, ymax))
            plt.axis([xmin, xmax, ymin, ymax])
        pic = outpath + '\\' + finame + '.pdf'
        plt.title('%s'%finame)

        plt.plot(xlst[1:],ylst[1:],color = 'red',label = '地面线'.decode('utf-8'))
        plt.legend(loc='best',fontsize = 'x-small')
        plt.grid(linestyle = ':',color = 'b')
        # ax = plt.gca()                                      #设置Y轴显示比例尺
        # ax.set_aspect(6)                                   #设置Y轴显示比例尺
        sublocation += 1
    plt.show()
    figure.savefig(pic,dpi = 800)



