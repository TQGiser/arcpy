#coding=utf-8
import arcpy
import os
import math
import pandas as pd
import F
path = r'E:\2021年项目\1213理塘桩牌表'
tks = F.listFiles(path,'','m')
dmaps = F.listFiles(path,'','d')
cnList = []
for dmap in dmaps:
    print dmap
    spatial_ref = arcpy.Describe(dmap).spatialReference
    if '99' in spatial_ref.name:
        fdh = 99
    elif '102' in spatial_ref.name:
        fdh = 102
    with arcpy.da.SearchCursor(dmap,['SHAPE@','NAME','ELEV','RuleID','NUM','COUNTY','TOWN','RIVER']) as yb:
        for row in yb:
            zm = row[1]
            lc = row[4]
            wz = row[5] + row[6]
            jd = 'E' + '：'.decode('utf-8') + str(
                '%0.8f' % round(F.XY2LatLon(row[0].centroid.X, row[0].centroid.Y, fdh)[1], 8)) + '°'.decode('utf-8')
            wd = 'N' + '：'.decode('utf-8') + str(
                '%0.8f' % round(F.XY2LatLon(row[0].centroid.X, row[0].centroid.Y, fdh)[0], 8)) + '°'.decode('utf-8')
            x = str('%0.4f' % round(row[0].centroid.Y))
            y = str('%0.4f' % round(row[0].centroid.X))
            gc = '%0.2f' % round(row[2], 2)
            if row[3] == 2 or row[3] == 3:
                bt = '实体桩桩位'
            elif row[3] == 4:
                bt = '告示牌'

            xq = row[5] + row[6]
            dm = '手动填写！！！'
            dw = '四川创数智慧科技股份有限公司'
            rq = '2021.12'
            riverName = row[7]
            if row[3] == 2:
                bz = '实体桩'
            elif row[3] == 3:
                bz = '移位桩'
            elif row[3] == 4:
                bz = '告示牌'
            for tk in tks:
                with arcpy.da.SearchCursor(tk,['SHAPE@','name']) as yb2:
                    for row2 in yb2:
                        if row2[0].contains(row[0]):
                            # riverName = row2[1].encode('utf-8').split('理塘县')[0]
                            if 'H' in row2[1].encode('utf-8') and '-' in row2[1].encode('utf-8'):
                                tkName = row2[1].encode('utf-8').split('-')[1]
                            else:
                                tkName = row2[1].encode('utf-8')
                            print row2[1], riverName, zm,tkName
                            cn = [zm,lc,wz,jd,wd,x,y,gc,bt,tkName,'手动填写',xq,dm,dw,rq,riverName,bz]
#                             cnList.append(cn)
# df = pd.DataFrame(cnList,columns=['桩名','里程','位置','经度','纬度','X','Y','高程','表头','图幅','编号','辖区','地名',
#                                   '单位','日期','river','备注'])
# df.to_excel(path.decode('utf-8') + '\\' + 'all.xlsx',index=False)



