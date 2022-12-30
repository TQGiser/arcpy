# coding=utf-8
import matplotlib.pyplot as plt
import pandas as pd
import os
import mpl_toolkits.axisartist.axislines as axislines

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
path = r'E:\2022年项目\0815理塘断面表格\ok\中曲河'.decode('utf-8')
outPath = r'E:\2022年项目\0815理塘断面表格\ok\pdf'.decode('utf-8')
os.chdir(path)
lst = []
for i, v, m in os.walk(path):
    lst = m
    riverName = i.split('ok\\')[1]
try:
    os.mkdir(outPath + '\\' + '{}pdf'.format(riverName.encode('utf-8')).decode('utf-8'))
except:
    pass
pdfPath = outPath + '\\' + '{}pdf'.format(riverName.encode('utf-8')).decode('utf-8')
for i in range(0, len(lst), 4):
    sublocation = 1
    for file in lst[i:i + 4]:
        print file
        figure = plt.gcf()
        figure.set_facecolor('white')
        df = pd.read_excel(file, header=1)
        plt.subplot(2, 2, sublocation)
        finame = df.columns.values[0]
        if  '水边'.decode('utf-8') in df['Unnamed: 2'].values:
            sbdlstx1 = '%.2f' % df[df['Unnamed: 2'] == '水边'.decode('utf-8')]['{}'.format(finame)].iloc[0]
            sbdlsty1 = '%.2f' % df[df['Unnamed: 2'] == '水边'.decode('utf-8')]['Unnamed: 1'].iloc[0]
            sbdlstx2 = '%.2f' % df[df['Unnamed: 2'] == '水边'.decode('utf-8')]['{}'.format(finame)].iloc[1]
            sbdlsty2 = '%.2f' % df[df['Unnamed: 2'] == '水边'.decode('utf-8')]['Unnamed: 1'].iloc[1]
        else:
            sbdlstx1 = '%.2f' % df[df['Unnamed: 2'] == '水边(坎下)'.decode('utf-8')]['{}'.format(finame)].iloc[0]
            sbdlsty1 = '%.2f' % df[df['Unnamed: 2'] == '水边(坎下)'.decode('utf-8')]['Unnamed: 1'].iloc[0]
            sbdlstx2 = '%.2f' % df[df['Unnamed: 2'] == '水边(坎下)'.decode('utf-8')]['{}'.format(finame)].iloc[1]
            sbdlsty2 = '%.2f' % df[df['Unnamed: 2'] == '水边(坎下)'.decode('utf-8')]['Unnamed: 1'].iloc[1]
        xlst = []
        ylst = []

        for index, value in df.iterrows():
            xlst.append(value.loc['{}'.format(finame)])
            ylst.append(value.loc['Unnamed: 1'])
            plt.xlabel('里程'.decode('utf-8'))
            plt.ylabel('高程'.decode('utf-8'))
        xmax = max(xlst[2:])
        xmin = min(xlst[2:])
        ymax = max(ylst[2:])
        ymin = min(ylst[2:])
        if ymax - ymin < 10:
            plt.xlim((xmin, xmax))
            plt.ylim((ymin, ymax))
            plt.axis([xmin, xmax, ymin, ymax + 10])
        else:
            plt.xlim((xmin, xmax))
            plt.ylim((ymin, ymax))
            plt.axis([xmin, xmax, ymin, ymax])
        pic = pdfPath + '\\' + finame + '.pdf'
        plt.title('%s' % finame)
        plt.plot(xlst[1:], ylst[1:], color='red', label='地面线'.decode('utf-8'))
        plt.plot([sbdlstx1, sbdlstx2], [sbdlsty1, sbdlsty2], color='blue', label='现实水位线'.decode('utf-8'))
        plt.legend(loc='best', fontsize='x-small')

        arpX = (float(sbdlstx1) + float(sbdlstx2))/2
        if xmax<100.0:
            plt.annotate('现实水位:{}米'.format(sbdlsty1).decode('utf-8'),
                         xy=(arpX, sbdlsty1),
                         xytext=(((xmax + xmin) / 2 -10),
                                 ((ymin + ymax) / 2 - 1) + 2),
                         arrowprops=dict(arrowstyle='->',
                                         connectionstyle='arc3', color='g'))
        else:
            plt.annotate('现实水位:{}米'.format(sbdlsty1).decode('utf-8'),
                         xy=(arpX, sbdlsty1),
                         xytext=(((xmax + xmin) / 2 -50),
                                 ((ymin + ymax) / 2 - 1) + 2),
                         arrowprops=dict(arrowstyle='->',
                                         connectionstyle='arc3', color='g'))
        plt.grid(linestyle=':', color='b')
        # ax = plt.gca()                                      #设置Y轴显示比例尺
        # ax.set_aspect(6)                                   #设置Y轴显示比例尺
        sublocation += 1
    plt.show()
    figure.savefig(pic, dpi=800)
