# coding=utf-8
import matplotlib.pyplot as plt
import pandas as pd
import os
import math
import F
import mpl_toolkits.axisartist.axislines as axislines

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
path = r'E:\2022年项目\1107鲜水河断面\xlsx'.decode('utf-8')
outpath = r'E:\2022年项目\1107鲜水河断面\pdf'.decode('utf-8')
os.chdir(path)
lst = []
for i, v, m in os.walk(path):
    lst = m
for i in range(0, len(lst), 4):
    sublocation = 1
    for file in lst[i:i + 4]:
        figure = plt.gcf()
        figure.set_facecolor('white')
        df = pd.read_excel(file, header=1)
        plt.subplot(2, 2, sublocation)

        xlst = []
        ylst = []
        sbdXlst = []
        sbdYlst = []
        finame = df.loc[1, '点次'.decode('utf-8')]
        # print finame
        cnList = []
        for index, value in df.iterrows():
            n = value.loc['纵坐标（X)'.decode(('utf-8'))]
            e = value.loc['横坐标（Y)'.decode('utf-8')]
            elev = round(value.loc['高程（H)'.decode('utf-8')], 2)
            if not math.isnan(n):
                x, y = F.LatLon2XY(n, e)
                if cnList.__len__() == 0:
                    x0 = x
                    y0 = y
                    cn = [x0, y0]
                    cnList.append(cn)
                dis = round(math.sqrt((x - x0) ** 2 + (y - y0) ** 2), 2)
                xlst.append(dis)
                ylst.append(elev)
                plt.xlabel('点距'.decode('utf-8'))
                plt.ylabel('高程'.decode('utf-8'))
                if value.loc['备注'.decode(('utf-8'))] == '水边'.decode('utf-8'):
                    sbdXlst.append(dis)
                    sbdYlst.append(elev)

        xmax = max(xlst)
        xmin = min(xlst)
        ymax = max(ylst)
        ymin = min(ylst)
        if ymax - ymin < 10:
            plt.xlim((xmin, xmax))
            plt.ylim((ymin, ymax))
            plt.axis([xmin, xmax, ymin, ymax + 10])
        else:
            plt.xlim((xmin, xmax))
            plt.ylim((ymin, ymax))
            plt.axis([xmin, xmax, ymin, ymax])
        pic = outpath + '\\' + finame + '.pdf'
        plt.title('%s' % finame)

        plt.plot(xlst, ylst, color='red', label='地面线'.decode('utf-8'))
        plt.plot(sbdXlst, sbdYlst, color='blue', label='现实水位线'.decode('utf-8'))
        plt.legend(loc='best', fontsize='x-small')
        plt.annotate('现实水位:{}米'.format(sbdYlst[0]).decode('utf-8'),
                     xy=((sbdXlst[0]+sbdXlst[1])/2, (sbdYlst[0]+sbdYlst[1])/2),
                     xytext=(((xmax + xmin) / 2 - 200), ((ymin + ymax) / 2 + 1)),
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3', color='g')
                     )
        plt.grid(linestyle=':', color='b')
        # ax = plt.gca()                                      #设置Y轴显示比例尺
        # ax.set_aspect(6)                                   #设置Y轴显示比例尺
        sublocation += 1
    plt.show()
    figure.savefig(pic, dpi=800)
