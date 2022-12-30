# coding=utf-8
import arcpy
import pandas as pd
import math
pd.set_option('display.width',500)
path = r'E:\test3'
arcpy.env.workspace = path
def cal_M_AB(x,y,zx):
    px_lst = []
    a = 0
    for a in range(0, len(zx)):
        dis = (math.sqrt((x - zx[a][0]) ** 2 + (y - zx[a][1]) ** 2))
        m = zx[a][2]
        px_p = [dis, m, zx[a][0], zx[a][1]]
        px_lst.append(px_p)
    cn_sort = sorted(px_lst, key=lambda s: s[0])
    x1 = cn_sort[0][2]
    y1 = cn_sort[0][3]
    x2 = cn_sort[1][2]
    y2 = cn_sort[1][3]
    x1_m = cn_sort[0][1]
    x2_m = cn_sort[1][1]
    if x1_m < x2_m:
        d = (y1 - y2) * x + (x2 - x1) * y + x1 * y2 - x2 * y1
    elif x1_m > x2_m:
        d = (y2 - y1) * x + (x1 - x2) * y + x2 * y1 - x1 * y2
    if d < 0:
        ab = '左岸'
    elif d > 0:
        ab = '右岸'
    czx = ((x - x1) * (x1 - x2) + (y - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (x1 - x2) + x1
    czy = ((x - x1) * (x1 - x2) + (y - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (y1 - y2) + y1
    np_m = x1_m + math.sqrt((czx - x1) ** 2 + (czy - y2) ** 2)
    return np_m,ab
aera_walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass",type='Polygon')
dmal_zx_walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass",type='Polyline')
for path,name,file in aera_walk:
    glqAera= file[0]
for path,name,file in dmal_zx_walk:
    for shp in file:
        if 'DMAL' in shp:
            dmal = shp
        elif '中线'.decode('utf-8') in shp:
            zx = shp
cn_lst = []
with arcpy.da.SearchCursor(dmal,['SHAPE@','RIVER']) as dmals:
    for line in dmals:
        with arcpy.da.SearchCursor(glqAera, ['SHAPE@', 'Name','FID','SHAPE@XY']) as aeras:
            for aera in aeras:
                for part in aera[0]:
                    for pnt in part:
                        try:
                            x = pnt.X
                            y = pnt.Y
                            if not line[0].disjoint(pnt):
                                cn = [pnt.X,pnt.Y,aera[1].encode('utf-8'),aera[2]]
                                if cn not in cn_lst:
                                    cn_lst.append(cn)
                        except:
                            print aera[1],aera[2]
zxcn_lst = []
with arcpy.da.SearchCursor(zx,['OID@','SHAPE@X','SHAPE@Y','SHAPE@M'],explode_to_points = True) as yb:
    i = 0
    for row in yb:
        cn = [row[1],row[2],row[3]]
        zxcn_lst.append(cn)
groups = max([cn[3] for cn in cn_lst])
pnt_df = []
i = 0
for i in range(0,groups+1):
    cn_group = [cn for cn in cn_lst if cn[3] == i]
    xmax = sorted(cn_group, key=lambda s: s[0])[-1][0]
    xmin = sorted(cn_group, key=lambda s: s[0])[0][0]
    ymax = sorted(cn_group, key=lambda s: s[1])[-1][1]
    ymin = sorted(cn_group, key=lambda s: s[1])[0][1]
    ulLst = []
    llLst = []
    urLst = []
    lrlst = []
    for cn in cn_group:
        x = cn[0]
        y = cn[1]
        UPPER_LEFT = math.sqrt((x - xmin) ** 2 + (y - ymax) ** 2)
        LOWER_LEFT = math.sqrt((x - xmin) ** 2 + (y - ymin) ** 2)
        UPPER_RIGHT = math.sqrt((x - xmax) ** 2 + (y - ymax) ** 2)
        LOWER_RIGHT = math.sqrt((x - xmax) ** 2 + (y - ymin) ** 2)
        UL = [x, y, UPPER_LEFT]
        LL = [x, y, LOWER_LEFT]
        UR = [x, y, UPPER_RIGHT]
        LR = [x, y, LOWER_RIGHT]
        ulLst.append(UL)
        llLst.append(LL)
        urLst.append(UR)
        lrlst.append(LR)
    stPoint = min(min(ulLst, key=lambda s: s[2]), min(llLst, key=lambda s: s[2]), min(urLst, key=lambda s: s[2]),
             min(lrlst, key=lambda s: s[2]))
    cn2_lst = []
    for cn in cn_group:
        x0 = stPoint[0]
        y0 = stPoint[1]
        dis = math.sqrt((cn[0] - x0) ** 2 + (cn[1] - y0) ** 2)
        cn2 = [cn[0], cn[1], dis,cn[2],cn[3]]
        cn2_lst.append(cn2)
    cn2_lst.sort(key=lambda s: s[2])
    a = 0
    lenth = 0
    for a in range(0, len(cn2_lst) - 1):
        disPart = math.sqrt((cn2_lst[i][0] - cn2_lst[i + 1][0]) ** 2 + (cn2_lst[i][1] - cn2_lst[i + 1][1]) ** 2)
        lenth += disPart
        a += 1
    p1 = cn2_lst[0]
    p2 = cn2_lst[-1]
    m1 = cal_M_AB(p1[0],p1[1],zxcn_lst)[0]
    m2 = cal_M_AB(p2[0],p2[1],zxcn_lst)[0]
    ab = cal_M_AB(p1[0],p1[1],zxcn_lst)[1]
    if m1<m2:
        qd = p1
        zd = p2
    elif m1>m2:
        qd = p2
        zd = p1
    print qd,ab
    print zd,ab
    i +=1