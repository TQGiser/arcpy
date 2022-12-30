# coding=utf-8
import arcpy
import os
import math
import F
path = r'E:\测试文件夹\导MDB\斗巫巴'
arcpy.env.workspace = path
river_name = r'斗巫巴'
zx = F.listFile(path, '校正后中线'.decode('utf-8'), 'x')
p = F.listFile(path, '线桩'.decode('utf-8'), 'd')
dmx = F.listFile(path,'校正后断面'.decode('utf-8'),'x')
spatial_ref = arcpy.Describe(p).spatialReference
if '99' in spatial_ref.name:
    xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-99.shp'
elif '102' in spatial_ref.name:
    xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-102.shp'
pCnList = []
xCnList = []
try:
    arcpy.AddField_management(p, 'BANK', 'SHORT')
    arcpy.AddField_management(p, 'Lc', 'LONG')
    arcpy.AddField_management(p, 'num_px', 'SHORT')
except:
    pass
with arcpy.da.SearchCursor(zx, ['OID@', 'SHAPE@X', 'SHAPE@Y', 'SHAPE@M'], explode_to_points=True) as yb:
    i = 0
    for row in yb:
        cn = [row[1], row[2], row[3], i]
        xCnList.append(cn)
        i += 1
with arcpy.da.UpdateCursor(p, ['SHAPE@X', 'SHAPE@Y', 'FID', 'BANK', 'LC']) as yb:
    for row in yb:
        print row[2]
        x = row[0]
        y = row[1]
        num = row[2]
        cnList = []
        i = 0
        for i in range(0, len(xCnList) - 1):
            x1 = xCnList[i][0]
            y1 = xCnList[i][1]
            m1 = xCnList[i][2]
            x2 = xCnList[i + 1][0]
            y2 = xCnList[i + 1][1]
            czx = ((x - x1) * (x1 - x2) + (y - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (x1 - x2) + x1
            czy = ((x - x1) * (x1 - x2) + (y - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (y1 - y2) + y1
            czm = m1 + math.sqrt((czx - x1) ** 2 + (czy - y1) ** 2)
            czdis = (y2 - y1) * czx + (x1 - x2) * czy + x2 * y1 - x1 * y2
            d = (y2 - y1) * x + (x1 - x2) * y + x2 * y1 - x1 * y2
            if czx > min(x1, x2) and czx < max(x1, x2) and czy > min(y1, y2) and czy < max(y1, y2):
                dis = math.sqrt((x - czx) ** 2 + (y - czy) ** 2)
                cn = [num, x1, x2, dis, d, czm]
                cnList.append(cn)
            else:
                dis = math.sqrt((x - x1) ** 2 + (y - y1) ** 2)
                cn = [num, x1, x2, dis, d, czm]
                cnList.append(cn)
            cnSort = sorted(cnList, key=lambda s: s[3])
            i += 1
        if cnSort[0][4] < 0:
            row[3] = 1
        elif cnSort[0][4] > 0:
            row[3] = 0
        row[4] = int(cnSort[0][5])
        if cnSort[0][5] > max([a[2] for a in xCnList]) or abs(cnSort[0][5] - max([a[2] for a in xCnList])) < 5.0:
            row[4] = int(max([a[2] for a in xCnList]))
        yb.updateRow(row)
np_cn_lst_left = []
with arcpy.da.SearchCursor(p, ['LC', 'BANK', 'SHAPE@X', 'SHAPE@Y'], '"BANK" = 0') as yb:
    for row in yb:
        cn = [row[2], row[3], row[0], row[1], 0]
        np_cn_lst_left.append(cn)
np_cn_lst_left = sorted(np_cn_lst_left, key=lambda s: s[2])
for i in range(0, len(np_cn_lst_left)):
    np_cn_lst_left[i][4] = i
np_cn_lst_right = []
with arcpy.da.SearchCursor(p, ['LC', 'BANK', 'SHAPE@X', 'SHAPE@Y'], '"BANK" = 1') as yb:
    for row in yb:
        cn = [row[2], row[3], row[0], row[1], 0]
        np_cn_lst_right.append(cn)
np_cn_lst_right = sorted(np_cn_lst_right, key=lambda s: s[2])
for i in range(0, len(np_cn_lst_right)):
    np_cn_lst_right[i][4] = i

with arcpy.da.UpdateCursor(p, ['LC', 'BANK', 'SHAPE@X', 'SHAPE@Y', 'num_px'], '"BANK" = 0') as yb:
    for row in yb:
        for i in range(0, len(np_cn_lst_left)):
            if row[2] == np_cn_lst_left[i][0]:
                num = np_cn_lst_left[i][4]
                row[0] = (np_cn_lst_right[i][2] + np_cn_lst_left[i][2]) / 2
        row[4] = num + 1
        yb.updateRow(row)
with arcpy.da.UpdateCursor(p, ['LC', 'BANK', 'SHAPE@X', 'SHAPE@Y', 'num_px'], '"BANK" = 1') as yb:
    for row in yb:
        for i in range(0, len(np_cn_lst_right)):
            if row[2] == np_cn_lst_right[i][0]:
                num = np_cn_lst_right[i][4]
                row[0] = (np_cn_lst_right[i][2] + np_cn_lst_left[i][2]) / 2
        row[4] = num + 1
        yb.updateRow(row)
arcpy.AddField_management(p, 'NAME', 'TEXT')
arcpy.AddField_management(p, 'NUM', 'TEXT')
with arcpy.da.UpdateCursor(p, ['NAME', 'NUM', 'num_px', 'BANK', 'LC']) as yb:
    for row in yb:
        if row[3] == 0:
            row[0] = river_name + '-理塘县左' + '%04d' % row[2]  ###地方###
        if row[3] == 1:
            row[0] = river_name + '-理塘县右' + '%04d' % row[2]
        row[1] = 'K' + str(int(row[4] / 1000.0)) + '+' + '%03d' % (row[4]%1000)
        yb.updateRow(row)
# with arcpy.da.UpdateCursor(p, ['NAME', 'NUM', 'num_px', 'BANK', 'LC']) as yb:
#     for row in yb:
#         if row[3] == 0:
#             row[0] = river_name + '-康定市左' + '%04d' % row[2]  ###地方###
#         if row[3] == 1:
#             row[0] = river_name + '-康定市右' + '%04d' % row[2]
#         row[1] = 'K' + str(int(row[4] / 1000.0)) + '+' + '%03d' % (row[4]%1000)
#         yb.updateRow(row)
arcpy.AddField_management(p, '位置', 'TEXT')
arcpy.AddField_management(p, '经度'.decode('utf-8'), 'TEXT')
arcpy.AddField_management(p, '纬度'.decode('utf-8'), 'TEXT')
arcpy.AddField_management(p, 'X', 'TEXT')
arcpy.AddField_management(p, 'Y', 'TEXT')
arcpy.AddField_management(p, 'H', 'TEXT')
arcpy.AddGeometryAttributes_management(Input_Features=p, Geometry_Properties="POINT_X_Y_Z_M",
                                       Length_Unit="", Area_Unit="", Coordinate_System="4490")
arcpy.CalculateField_management(p, '经度', '!POINT_X!', 'PYTHON_9.3')
arcpy.CalculateField_management(p, '经度',
                                "'E' + str('%0.8f'%round(float( !经度!) ,8)) + '°'.decode('utf-8')",
                                'PYTHON_9.3')
arcpy.CalculateField_management(p, '纬度', '!POINT_Y!', 'PYTHON_9.3')
arcpy.CalculateField_management(p, '纬度',
                                "'N' + str('%0.8f'%round(float( !纬度!) ,8)) + '°'.decode('utf-8')",
                                'PYTHON_9.3')
arcpy.CalculateField_management(p, 'X', "'%.4f'%!shape.centroid.Y!", 'PYTHON_9.3')
arcpy.CalculateField_management(p, 'Y', "'%.4f'%!shape.centroid.X!", 'PYTHON_9.3')
arcpy.DeleteField_management(p, drop_field="OBJECTID;lc_float;num_px;POINT_X;POINT_Y;POINT_Z;POINT_M")
with arcpy.da.SearchCursor(xzjx, ['SHAPE@', 'XZQMC', 'XZQMC_1']) as yb:
    for row in yb:
        with arcpy.da.UpdateCursor(p, ['SHAPE@', '位置'.decode('utf-8'), 'NAME']) as yb2:
            for row2 in yb2:
                if row[0].contains(row2[0]):
                    row2[1] = row[2] + row[1]
                    yb2.updateRow(row2)
try:
    with arcpy.da.SearchCursor(dmx,['SHAPE@','里程'.decode('utf-8'),'H']) as yb:
        for row in yb:
            with arcpy.da.UpdateCursor(p,['SHAPE@','NUM','NAME','H']) as dmaps:
                for dmap in dmaps:
                    if dmap[0].within(row[0]):
                        print row[1],dmap[2]
                        dmap[1] = row[1]
                        dmap[3] = row[2]
                        dmaps.updateRow(dmap)
except:
    pass
