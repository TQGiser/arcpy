#coding=utf-8
import matplotlib.pyplot as plt
import pandas as pd
import os
import mpl_toolkits.axisartist.axislines as axislines
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
path = r'C:\Users\Administrator\Desktop\热曲河道断面成果'.decode('utf-8')
outpath = r'C:\Users\Administrator\Desktop\pdf'.decode('utf-8')
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
        df['高程'.decode('utf-8')] = df['高程'.decode('utf-8')].round(2)
        df['X'] = df['X'].round(2)
        df['Y'] = df['Y'].round(2)
        plt.subplot(2, 2, sublocation)
        sbdlstx = df[df['备注'.decode('utf-8')] == '水边'.decode('utf-8')]['另点距'.decode('utf-8')]
        sbdlsty = df[df['备注'.decode('utf-8')] == '水边'.decode('utf-8')]['高程'.decode('utf-8')]
        count_sbd = len(df[df['备注'.decode('utf-8')] == '水边'.decode('utf-8')])
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

        plt.plot(xlst[1:],ylst[1:],color = 'red',label = '地面线'.decode('utf-8'),linewidth = '1')


        if df['备注'.decode('utf-8')].isin(['主水边'.decode('utf-8')]).any():
            zsbx = df[df['备注'.decode('utf-8')] == '主水边'.decode('utf-8')]['另点距'.decode('utf-8')].iloc[0]
            zsby = df[df['备注'.decode('utf-8')] == '主水边'.decode('utf-8')]['高程'.decode('utf-8')].iloc[0]
            zsbx1 = df[df['备注'.decode('utf-8')] == '主水边'.decode('utf-8')]['另点距'.decode('utf-8')].iloc[1]
            zsby1 = df[df['备注'.decode('utf-8')] == '主水边'.decode('utf-8')]['高程'.decode('utf-8')].iloc[1]
            plt.plot([zsbx,zsbx1],[zsby,zsby1], color='blue', label='现实水位线'.decode('utf-8'))
            plt.annotate('现实水位:{}米'.format(zsby).decode('utf-8'),xy = (zsbx,zsby),xytext = (((xmax+xmin)/2 - 50),((ymin+ymax)/2 -1) + 2),arrowprops = dict(arrowstyle = '-|>',
                    connectionstyle = 'arc3',color = 'g'))
            for i in range(0, count_sbd - 1, 2):
                sbdlstx1 = df[df['备注'.decode('utf-8')] == '水边'.decode('utf-8')]['另点距'.decode('utf-8')].iloc[0]
                sbdlsty1 = df[df['备注'.decode('utf-8')] == '水边'.decode('utf-8')]['高程'.decode('utf-8')].iloc[0]
                plt.plot([sbdlstx.iloc[i], sbdlstx.iloc[i + 1]], [sbdlsty.iloc[i], sbdlsty.iloc[i + 1]], color='blue',linewidth = '1')
                le = plt.legend(loc='upper right', fontsize='x-small', shadow=True)
                le.get_frame().set_facecolor('w')
            # plt.legend(loc='upper right', fontsize='x-small')

        else:
            for i in range(0, count_sbd - 1, 2):
                sbdlstx1 = df[df['备注'.decode('utf-8')] == '水边'.decode('utf-8')]['另点距'.decode('utf-8')].iloc[0]
                sbdlsty1 = df[df['备注'.decode('utf-8')] == '水边'.decode('utf-8')]['高程'.decode('utf-8')].iloc[0]
                plt.plot([sbdlstx.iloc[i], sbdlstx.iloc[i + 1]], [sbdlsty.iloc[i], sbdlsty.iloc[i + 1]], color='blue',
                         label='现实水位线'.decode('utf-8'),linewidth = '1')

                plt.annotate('现实水位:{}米'.format(sbdlsty1).decode('utf-8'), xy=(sbdlstx1, sbdlsty1),
                         xytext=(((xmax + xmin) / 2 - 25), (ymin + ymax) / 2  ),
                         arrowprops=dict(arrowstyle='-|>',
                                         connectionstyle='arc3', color='g'))
                le = plt.legend(loc = 'upper right', fontsize='x-small',shadow = True)
                # plt.legend(loc='upper right', fontsize='x-small')
                le.get_frame().set_facecolor('w')
        plt.grid(linestyle = ':',color = 'b')
        # ax = plt.gca()                                      #设置Y轴显示比例尺
        # ax.set_aspect(6)                                   #设置Y轴显示比例尺
        sublocation += 1
    plt.show()
    figure.savefig(pic,dpi = 800)