# coding=utf-8
import arcpy
import os
import pandas as pd
import F
path = r'E:\理塘划界成果'
arcpy.env.workspace = path
mdbs = arcpy.ListFiles('*.mdb')
cnList = []
for mdb in mdbs:
    print mdb
    riverName = mdb.replace('.mdb','')
    dmap = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'DMAP'
    DLG = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG'
    spatial_ref = arcpy.Describe(DLG).spatialReference
    print spatial_ref.name
    if '99' in spatial_ref.name:
        fdh = 99
    elif '102' in spatial_ref.name:
        fdh = 102
    with arcpy.da.SearchCursor(dmap,['SHAPE@','NAME','NUM','COUNTY','TOWN','ELEV','RuleID']) as yb:
        for row in yb:
            if row[6] ==2 or row[6] ==3 or row[6] == 4:
                zm = row[1]
                print zm
                lc = row[2]
                wz = row[3] + row[4]
                jd ='E' + '：'.decode('utf-8') + str('%0.8f'%round(F.XY2LatLon(row[0].centroid.X,row[0].centroid.Y,fdh)[1],8)) + '°'.decode('utf-8')
                wd = 'N' + '：'.decode('utf-8') + str('%0.8f'%round(F.XY2LatLon(row[0].centroid.X,row[0].centroid.Y,fdh)[0],8)) + '°'.decode('utf-8')
                x = str('%0.4f'%round(row[0].centroid.Y))
                y = str('%0.4f'%round(row[0].centroid.X))
                gc = '%0.2f'%round(row[5],2)

                if row[6] == 2 or row[6] == 3:
                    bt = '实体桩桩位'
                elif row[6] ==4:
                    bt = '告示牌'
                xq = row[3] + row[4]
                dm = '手动填写！！！'
                dw = '四川创数智慧科技股份有限公司'
                rq = '2021.11'
                if row[6] == 2:
                    bz = '实体桩'
                elif row[6] ==3:
                    bz = '移位桩'
                elif row[6] == 4:
                    bz = '告示牌'
                cn = [zm, lc, wz, jd, wd, x, y, gc,bt,'手动填写',xq,dm,dw,rq,riverName,bz]
                cnList.append(cn)
df = pd.DataFrame(cnList,columns=['桩名','里程','位置','经度','纬度','X','Y','高程','表头','编号','辖区','地名',
                                  '单位','日期','river','备注'])
df.to_excel(r'E:\理塘划界成果\a.xlsx'.decode('utf-8'),index=False)
