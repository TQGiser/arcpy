# coding=utf-8
import arcpy
import os
import random
import shutil
path = r'D:\2021年项目\0601湖泊划界\方哥'.decode('utf-8')
filelst = []
for i, v, m in os.walk(path):
    if '县\\' in str(i.encode('utf-8')):
        filelst.append(i)
for path2 in filelst:
    try:
        path = path2
        DLMC = str(path2.encode('utf-8')).split('\\')[-2]
        gdbname = str(path2.encode('utf-8')).split('\\')[-2] + str(path2.encode('utf-8')).split('\\')[-1]
        arcpy.env.workspace = path
        arcpy.CreateFileGDB_management(path, gdbname)
        gdbpath = path.encode('utf-8') + '\\' + gdbname + '.gdb'
        shpfile = 'dmal.shp'
        arcpy.FeatureClassToFeatureClass_conversion(shpfile, '{}.gdb'.format(gdbname), 'dmal')
        arcpy.env.workspace = gdbpath
        with arcpy.da.SearchCursor('dmal', ['NAME','elev']) as yb:
            for row in yb:
                a = row[0]
                lakename = a.encode('utf-8')
                elev = row[1]
        arcpy.CreateRoutes_lr('dmal', 'NAME', '{}'.format(lakename))
        lcd = '{}全部里程点'.format(lakename)
        dzz = '{}电子桩'.format(lakename)
        arcpy.FeatureVerticesToPoints_management(lakename, lcd)
        arcpy.AddXY_management(lcd)
        arcpy.CreateFeatureclass_management(gdbpath, dzz, 'POINT', spatial_reference=lcd, has_m='ENABLED')
        lst = []
        lstM = []
        dzzcnlst = []
        with arcpy.da.SearchCursor(lcd, ['POINT_X', 'POINT_Y', 'POINT_M']) as yb:
            for row in yb:
                qdcn = (row[0], row[1],0)
                continue
        dzzcnlst.append(qdcn)
        print dzzcnlst
        with arcpy.da.SearchCursor(lcd, ['POINT_X', 'POINT_Y', 'POINT_M']) as yb:
            for row in yb:
                lst.append([row[0], row[1], row[2]])
                lstM.append(row[2])
        zpNum = 4
        zpM = 0
        for i in range(0, zpNum-1):
            fdcd = max(lstM) / zpNum
            zpM += fdcd
            lowerX = []
            lowerY = []
            lowerM = []
            higherX = []
            higherY = []
            higherM = []
            for x, y, m in lst:
                if m < zpM:
                    lowerX.append(x)
                    lowerY.append(y)

                    lowerM.append(m)
                else:
                    higherX.append(x)
                    higherY.append(y)
                    higherM.append(m)
            x1 = lowerX[-1]
            y1 = lowerY[-1]
            m1 = lowerM[-1]
            x2 = higherX[0]
            y2 = higherY[0]
            m2 = higherM[0]
            x3 = x1 - (x1 - x2) * (zpM - m1) / (m2 - m1)
            y3 = y1 - (y1 - y2) * (zpM - m1) / (m2 - m1)
            cn = (x3, y3, zpM)
            dzzcnlst.append(cn)
        yb = arcpy.da.InsertCursor(dzz, ['SHAPE@X', 'SHAPE@Y', 'SHAPE@M'])
        for i in dzzcnlst:
            yb.insertRow(i)
        arcpy.AddField_management(dzz, 'NAME', 'TEXT')
        with arcpy.da.UpdateCursor(dzz, 'NAME') as yb:
            num = 1
            for row in yb:
                row[0] = lakename + '-00' + str(num)
                num += 1
                yb.updateRow(row)
        arcpy.AddField_management(dzz, '里程'.decode('utf-8'), 'TEXT')
        arcpy.AddField_management(dzz, '所在位置'.decode('utf-8'), 'TEXT')
        arcpy.AddField_management(dzz, '经度'.decode('utf-8'), 'TEXT')
        arcpy.AddField_management(dzz, '纬度'.decode('utf-8'), 'TEXT')
        arcpy.AddGeometryAttributes_management(dzz, "POINT_X_Y_Z_M", Coordinate_System="4490")
        arcpy.CalculateField_management(dzz, '经度'.decode('utf-8'), '!POINT_X!', 'PYTHON_9.3')
        arcpy.CalculateField_management(dzz, '纬度'.decode('utf-8'), '!POINT_Y!', 'PYTHON_9.3')
        arcpy.DeleteField_management(dzz, 'POINT_X')
        arcpy.DeleteField_management(dzz, 'POINT_Y')
        arcpy.DeleteField_management(dzz, 'POINT_M')
        arcpy.AddField_management(dzz, 'X', 'TEXT')
        arcpy.AddField_management(dzz, 'Y', 'TEXT')
        arcpy.AddXY_management(dzz)
        arcpy.CalculateField_management(dzz, 'X', "'%.4f'%round(!POINT_Y!,4)", 'PYTHON_9.3')
        arcpy.CalculateField_management(dzz, 'Y', "'%.4f'%round(!POINT_X!,4)", 'PYTHON_9.3')
        arcpy.DeleteField_management(dzz, 'POINT_X')
        arcpy.DeleteField_management(dzz, 'POINT_Y')
        with arcpy.da.UpdateCursor(dzz, ['经度'.decode('utf-8'), '纬度'.decode('utf-8')]) as yb:
            for row in yb:
                row[0] = 'E'.decode('utf-8') + str(row[0]).split('.')[0] + '.'.decode('utf-8') + str(row[0]).split('.')[1][0:8] + '°'.decode('utf-8')
                row[1] = 'N'.decode('utf-8') + str(row[1]).split('.')[0] + '.'.decode('utf-8') + str(row[1]).split('.')[1][0:8] + '°'.decode('utf-8')
                yb.updateRow(row)
        arcpy.CalculateField_management(dzz, '里程'.decode('utf-8'),
                                        "'K' + str( !POINT_M! /1000).split('.')[0]+ '+' + '%03.0f'%float(str( !POINT_M! ).split('.')[0][-3:]) ",
                                        'PYTHON_9.3')
        with arcpy.da.UpdateCursor(dzz, '所在位置'.decode('utf-8')) as yb:
            for row in yb:
                row[0] = DLMC
                yb.updateRow(row)
        arcpy.AddField_management(dzz,'H','TEXT')
        arcpy.DeleteField_management(dzz,'POINT_M')
        # with arcpy.da.UpdateCursor(dzz, 'H') as yb:                                                                   #不用随机数设置高程，
        #     sjs = (random.randint(1,9)/100)
        #     for row in yb:
        #         row[0] = elev + float(random.randint(1,9))/100
        #         yb.updateRow(row)
        #         print row[0]
        with arcpy.da.UpdateCursor(dzz, 'H') as yb:                                                                     #用dmal的elev作为高程，
            for row in yb:
                row[0] = '%.2f'%float(elev)
                yb.updateRow(row)
        shpPath = path.encode('utf-8') + '\\' + dzz
        arcpy.CopyFeatures_management(dzz,shpPath)
        arcpy.TableToExcel_conversion(dzz,r'D:\2021年项目\0601湖泊划界\电子桩表格\{}.xls'.format(gdbname))
        print '{}is done'.format(gdbname)
    except:
        print '{}is not done'.format(gdbname)
