# coding=utf-8
import arcpy
import os
import pandas as pd
import F
path = r'E:\测试文件夹\导SHP'
arcpy.env.workspace = path
mdbs = arcpy.ListFiles('*.mdb')
cnList = []
for mdb in mdbs:
    print mdb
    riverName = mdb.replace('.mdb','')
    dmap = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'DMAP'
    with arcpy.da.SearchCursor(dmap,['SHAPE@','NAME','NUM','COUNTY','TOWN','ELEV','RuleID']) as yb:
        for row in yb:
            if row[6] ==2 or row[6] ==3 or row[6] == 4:
                zm = row[1]
                print zm
                lc = row[2]
                wz = row[3] + row[4]
                jd ='E' + '：'.decode('utf-8') + str('%0.8f'%round(F.XY2LatLon(row[0].centroid.X,row[0].centroid.Y,99)[1],8)) + '°'.decode('utf-8')
                wd = 'N' + '：'.decode('utf-8') + str('%0.8f'%round(F.XY2LatLon(row[0].centroid.X,row[0].centroid.Y,99)[0],8)) + '°'.decode('utf-8')
                x = str('%0.4f'%round(row[0].centroid.Y))
                y = str('%0.4f'%round(row[0].centroid.X))
                gc = '%0.2f'%round(row[5],2)
                if row[6] == 2 or row[6] == 3:
                    bt = '实体桩桩位'
                elif row[6] ==4:
                    bt = '告示牌'
                tk2K = F.listFile(r'E:\巴塘划界资料\图框','巴塘2K'.decode('utf-8'),'m')
                tk1W = F.listFile(r'E:\巴塘划界资料\图框','巴塘1W'.decode('utf-8'),'m')
                tfname = []
                with arcpy.da.SearchCursor(tk2K,['SHAPE@','name']) as yb2:
                    for row2 in yb2:
                        if row2[0].contains(row[0]):
                            tf =row2[1]
                            tfname.append(tf)
                if len(tfname) == 0:
                    with arcpy.da.SearchCursor(tk1W,['SHAPE@','name']) as yb2:
                        for row2 in yb2:
                            if row2[0].contains(row[0]):
                                tf = row2[1]
                                tfname.append(tf)
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
                cn = [zm, lc, wz, jd, wd, x, y, gc,bt,tfname[0],'手动填写',xq,dm,dw,rq,riverName,bz]
                cnList.append(cn)
df = pd.DataFrame(cnList,columns=['桩名','里程','位置','经度','纬度','X','Y','高程','表头','图幅','编号','辖区','地名',
                                  '单位','日期','river','备注'])
df.to_excel(path.decode('utf-8') + '\\' + 'a.xlsx',index=False)
