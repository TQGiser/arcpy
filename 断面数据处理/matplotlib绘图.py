#coding=utf-8
import matplotlib.pyplot as plt
import pandas as pd
import os
import mpl_toolkits.axisartist.axislines as axislines
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
path = r'D:\2021年项目\0512达曲断面\达曲河道断面成果原始\达曲河道断面成果\达曲河道断面成果表'.decode('utf-8')
outpath = r'D:\2021年项目\0512达曲断面\pdf'.decode('utf-8')
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
        sbdlstx1 = df[df['备注'.decode('utf-8')] == '水边'.decode('utf-8')]['另点距'.decode('utf-8')].iloc[0]
        sbdlsty1 = df[df['备注'.decode('utf-8')] == '水边'.decode('utf-8')]['高程'.decode('utf-8')].iloc[0]
        sbdlstx2 = df[df['备注'.decode('utf-8')] == '水边'.decode('utf-8')]['另点距'.decode('utf-8')].iloc[1]
        sbdlsty2 = df[df['备注'.decode('utf-8')] == '水边'.decode('utf-8')]['高程'.decode('utf-8')].iloc[1]
        xlst = []
        ylst = []
        finame = df.loc[0,'另点距'.decode('utf-8')]
        for index,value in df.iterrows():
            xlst.append(value.loc['另点距'.decode(('utf-8'))])
            ylst.append(value.loc['高程'.decode('utf-8')])
            plt.xlabel('另点距'.decode('utf-8'))
            plt.ylabel('高程'.decode('utf-8'))
        xmax = max(xlst[1:])
        xmin = min(xlst[1:])
        ymax = max(ylst[1:])
        ymin = min(ylst[1:])
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
        plt.plot([sbdlstx1,sbdlstx2],[sbdlsty1,sbdlsty2],color = 'blue',label = '现实水位线'.decode('utf-8'))
        plt.legend(loc='best',fontsize = 'x-small')
        plt.annotate('现实水位:{}米'.format(sbdlsty1).decode('utf-8'),xy = (sbdlstx1,sbdlsty1),xytext = (((xmax+xmin)/2 - 50),((ymin+ymax)/2 -1) + 2),arrowprops = dict(arrowstyle = '->',
                    connectionstyle = 'arc3',color = 'g'))
        plt.grid(linestyle = ':',color = 'b')
        # ax = plt.gca()                                      #设置Y轴显示比例尺
        # ax.set_aspect(6)                                   #设置Y轴显示比例尺
        sublocation += 1
    plt.show()
    figure.savefig(pic,dpi = 800)



