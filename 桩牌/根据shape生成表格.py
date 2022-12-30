# coding=utf-8
import arcpy
import os
workspace = r'D:\2021年项目\0609湖泊表格\湖泊管理范围线、桩牌'.decode('utf-8')
shps = []
walk = arcpy.da.Walk(workspace, topdown=True, datatype="FeatureClass",type='Point')
xzjShp = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-99.shp'
for dirpath, dirnames, filenames in walk:
    # Disregard any folder named 'back_up' in creating list of rasters
    # if "桩".decode('utf-8') not in dirnames:
    #     dirnames.remove('back_up')
    for filename in filenames:
        if "桩".decode('utf-8')  in filename:
            shps.append(os.path.join(dirpath, filename))
a = 1
for shp in shps:
    name = '四川省甘孜藏族自治州' + shp.encode('utf-8').split('\桩')[0].split('\\')[-1] + '管理线桩'
    arcpy.DefineProjection_management(shp, coor_system='4542')
    arcpy.AddField_management(shp, '桩名(编号)'.decode('utf-8'), 'TEXT')
    arcpy.AddField_management(shp, '里程a', 'TEXT')
    arcpy.AddField_management(shp, '所在位置'.decode('utf-8'), 'TEXT')
    arcpy.AddField_management(shp, '经度'.decode('utf-8'), 'TEXT')
    arcpy.AddField_management(shp, '纬度'.decode('utf-8'), 'TEXT')
    arcpy.AddField_management(shp,'X','TEXT')
    arcpy.AddField_management(shp,'Y','TEXT')
    arcpy.AddField_management(shp, 'H', 'TEXT')
    arcpy.CalculateField_management(shp, '桩名_编号_'.decode('utf-8'), '!名称!', 'PYTHON_9.3')
    arcpy.CalculateField_management(shp, '里程a', '!里程!', 'PYTHON_9.3')
    tempShp = arcpy.Identity_analysis(shp, xzjShp,out_feature_class=r"D:\2021年项目\stuff\桩_Identity{}".format(a),
                            join_attributes="ALL", cluster_tolerance="", relationship="NO_RELATIONSHIPS")
    a += 1
    with arcpy.da.SearchCursor(tempShp,['XZQMC_1','XZQMC']) as yb:
        for row in yb:
            wz = row[0] + row[1]
            pass
    with arcpy.da.UpdateCursor(shp, '所在位置'.decode('utf-8')) as yb:
        for row in yb:
            row[0] = wz
            yb.updateRow(row)
    arcpy.AddGeometryAttributes_management(shp, "POINT_X_Y_Z_M", Coordinate_System="4490")
    arcpy.CalculateField_management(shp, '经度'.decode('utf-8'), '!POINT_X!', 'PYTHON_9.3')
    arcpy.CalculateField_management(shp, '纬度'.decode('utf-8'), '!POINT_Y!', 'PYTHON_9.3')
    with arcpy.da.UpdateCursor(shp, ['经度'.decode('utf-8'), '纬度'.decode('utf-8')]) as yb:
        for row in yb:
            row[0] = 'E'.decode('utf-8') + str(row[0]).split('.')[0] + '.'.decode('utf-8') + str(row[0]).split('.')[1][0:8] + '°'.decode('utf-8')
            row[1] = 'N'.decode('utf-8') + str(row[1]).split('.')[0] + '.'.decode('utf-8') + str(row[1]).split('.')[1][0:8] + '°'.decode('utf-8')
            yb.updateRow(row)
    arcpy.DeleteField_management(shp,['POINT_X','POINT_Y','POINT_M'])
    arcpy.AddXY_management(shp)
    arcpy.CalculateField_management(shp, 'X', "'%.4f'%round(!POINT_Y!,4)", 'PYTHON_9.3')
    arcpy.CalculateField_management(shp, 'Y', "'%.4f'%round(!POINT_X!,4)", 'PYTHON_9.3')
    arcpy.DeleteField_management(shp, 'POINT_X')
    arcpy.DeleteField_management(shp, 'POINT_Y')
    arcpy.DeleteField_management(shp,['Id','名称'.decode('utf-8'),'x坐标'.decode('utf-8'),'y坐标'.decode('utf-8'),'里程'.decode('utf-8'),])
    arcpy.TableToExcel_conversion(shp,r'D:\2021年项目\0609湖泊表格\aaa\{}.xls'.format(name))
    print '{} is done'.format(name)