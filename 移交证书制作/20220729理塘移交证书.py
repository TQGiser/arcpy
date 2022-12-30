# coding=utf-8
import arcpy
import pandas as pd
import F

path = r'E:\2022年项目\0729理塘桩牌\temp'
arcpy.env.workspace = path
dmap = r'E:\2022年项目\0729理塘桩牌\temp\DMAPTK.shp'
cnList = []
with arcpy.da.SearchCursor(dmap, ['SHAPE@', 'NAME', 'NUM', 'COUNTY', 'TOWN', 'ELEV', 'RuleID','name_1','river']) as yb:
    for row in yb:
        zm = row[1]
        lc = row[2]
        wz = row[3] + row[4]
        jd = 'E' + '：'.decode('utf-8') + str('%0.8f' % round(row[0].centroid.X, 8)) + '°'.decode('utf-8')
        wd = 'N' + '：'.decode('utf-8') + str('%0.8f' % round(row[0].centroid.Y, 8)) + '°'.decode('utf-8')
        x = 'no need'
        y = 'no need'
        if row[6] == 2 or row[6] == 3:
            bt = '实体桩桩位'
        elif row[6] == 4:
            bt = '告示牌'
        gc = '%0.2f' % round(row[5], 2)
        tf = row[7]
        xq = row[3] + row[4]
        dm = '手动填写！！！'
        dw = '四川创数智慧科技股份有限公司'
        rq = '2022.07'
        riverName = row[8]
        if row[6] == 2:
            bz = '实体桩'
        elif row[6] == 3:
            bz = '移位桩'
        elif row[6] == 4:
            bz = '告示牌'
        cn = [zm,lc,wz,jd,wd,x,y,gc,bt,tf,'手动填写',xq,dm,dw,rq,riverName,bz]
        cnList.append(cn)
df = pd.DataFrame(cnList,columns=['桩名','里程','位置','经度','纬度','X','Y','高程','表头','图幅','编号','辖区','地名',
                                  '单位','日期','river','备注'])
df.to_excel(path.decode('utf-8') + '\\' + 'a.xlsx',index=False)
