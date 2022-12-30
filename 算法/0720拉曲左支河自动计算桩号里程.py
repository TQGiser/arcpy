# coding=utf-8
import arcpy
import os
import math
arcpy.env.workspace = r'D:\T2'
zx = r'D:\T2\zx.shp'
p = r'D:\T2\p1.shp'
spatial_ref = arcpy.Describe(p).spatialReference
if '99' in spatial_ref.name:
    xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-99.shp'
elif '102' in spatial_ref.name:
    xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-102.shp'
cn_lst = []
np_lst = []
river_name = raw_input('河流名称:')
arcpy.AddField_management(p,'lc_float','DOUBLE')
arcpy.AddField_management(p,'BANK','SHORT')
arcpy.AddField_management(p,'num_px','SHORT')
with arcpy.da.SearchCursor(zx,['OID@','SHAPE@X','SHAPE@Y','SHAPE@M'],explode_to_points = True) as yb:
    i = 0
    for row in yb:
        cn = [row[1],row[2],row[3]]
        cn_lst.append(cn)
        i += 1
with arcpy.da.UpdateCursor(p,['SHAPE@X','SHAPE@Y','lc_float','BANK']) as yb:
    for row in yb:
        x3 = row[0]
        y3 = row[1]
        px_lst = []
        for i in range(0,len(cn_lst)):
            dis = (math.sqrt((x3-cn_lst[i][0])**2 + (y3 - cn_lst[i][1])**2))
            m = cn_lst[i][2]
            px_p = [dis,m,cn_lst[i][0],cn_lst[i][1]]
            px_lst.append(px_p)
        cn_sort = sorted(px_lst, key=lambda s: s[0])
        x1 = cn_sort[0][2]
        y1 = cn_sort[0][3]
        x2 = cn_sort[1][2]
        y2 = cn_sort[1][3]
        m_sort = sorted(px_lst, key=lambda s: s[0])
        x1_m =m_sort[0][1]
        x2_m =m_sort[1][1]
        if x1_m < x2_m:
            d = (y1 - y2) * x3 + (x2 - x1) * y3 + x1 * y2 - x2 * y1
        elif x1_m > x2_m:
            d = (y2 - y1)*x3+(x1-x2)*y3 +x2*y1-x1*y2
        czx = ((x3 - x1) * (x1 - x2) + (y3 - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (x1 - x2) + x1
        czy = ((x3 - x1) * (x1 - x2) + (y3 - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (y1 - y2) + y1
        np_m = x1_m + math.sqrt((czx-x1)**2 + (czy - y2)**2)
        if d<0:
            row[3] = 0
        elif d>0:
            row[3] = 1
        row[2] = np_m
        yb.updateRow(row)
np_cn_lst_left = []
with arcpy.da.SearchCursor(p,['lc_float','BANK','SHAPE@X','SHAPE@Y'],'"BANK" = 0') as yb:
     for row in yb:
        cn = [row[2],row[3],row[0],row[1],0]
        np_cn_lst_left.append(cn)
np_cn_lst_left = sorted(np_cn_lst_left,key=lambda s: s[2])
for i in range(0,len(np_cn_lst_left)):
    np_cn_lst_left[i][4] = i
np_cn_lst_right = []
with arcpy.da.SearchCursor(p,['lc_float','BANK','SHAPE@X','SHAPE@Y'],'"BANK" = 1') as yb:
    for row in yb:
        cn = [row[2],row[3],row[0],row[1],0]
        np_cn_lst_right.append(cn)
np_cn_lst_right = sorted(np_cn_lst_right,key=lambda s: s[2])
for i in range(0,len(np_cn_lst_right)):
    np_cn_lst_right[i][4] = i

with arcpy.da.UpdateCursor(p,['lc_float','BANK','SHAPE@X','SHAPE@Y','num_px'],'"BANK" = 0') as yb:
    for row in yb:
        for i in range(0,len(np_cn_lst_left)):
            if row[2] == np_cn_lst_left[i][0]:
                num = np_cn_lst_left[i][4]
                row[0] = (np_cn_lst_right[i][2] + np_cn_lst_left[i][2]) / 2
        row[4] = num + 1
        yb.updateRow(row)
with arcpy.da.UpdateCursor(p,['lc_float','BANK','SHAPE@X','SHAPE@Y','num_px'],'"BANK" = 1') as yb:
    for row in yb:
        for i in range(0,len(np_cn_lst_right)):
            if row[2] == np_cn_lst_right[i][0]:
                num = np_cn_lst_right[i][4]
                row[0] = (np_cn_lst_right[i][2]+ np_cn_lst_left[i][2])/2
        row[4] = num + 1
        yb.updateRow(row)
arcpy.AddField_management(p,'NAME','TEXT')
arcpy.AddField_management(p,'NUM','TEXT')
with arcpy.da.UpdateCursor(p,['NAME','NUM','num_px','BANK','lc_float']) as yb:
    for row in yb:
        if row[3] == 0:
            row[0] = river_name + '-理塘县左' + '%04d'%row[2]
        if row[3] == 1:
            row[0] = river_name + '-理塘县右' + '%04d' % row[2]
        row[1] = 'K' + str(int(row[4]/1000))+ '+' + str(row[4]/1000).split('.')[1][0:3]
        yb.updateRow(row)
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
                                "'E' + !经度!.split('.')[0] + '.' + !经度!.split('.')[1][0:8] + '°'.decode('utf-8')",
                                'PYTHON_9.3')
arcpy.CalculateField_management(p, '纬度', '!POINT_Y!', 'PYTHON_9.3')
arcpy.CalculateField_management(p, '纬度',
                                "'N' + !纬度!.split('.')[0] + '.' + !纬度!.split('.')[1][0:8] + '°'.decode('utf-8')",
                                'PYTHON_9.3')
arcpy.CalculateField_management(p, 'X', "'%.4f'%!shape.centroid.Y!", 'PYTHON_9.3')
arcpy.CalculateField_management(p, 'Y', "'%.4f'%!shape.centroid.X!", 'PYTHON_9.3')
arcpy.DeleteField_management(p, drop_field="OBJECTID;lc_float;num_px;POINT_X;POINT_Y;POINT_Z;POINT_M")
with arcpy.da.SearchCursor(xzjx,['SHAPE@','XZQMC','XZQMC_1']) as yb:
    for row in yb:
        with arcpy.da.UpdateCursor(p,['SHAPE@','位置'.decode('utf-8'),'NAME']) as yb2:
            for row2 in yb2:
                if row[0].contains(row2[0]):
                    print row2[2],row[1],row[2]
                    row2[1] = row[2] + row[1]
                    yb2.updateRow(row2)