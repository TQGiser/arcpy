#coding=utf-8
import arcpy
import os
import pandas as pd
path = r'D:\2021年项目\0708湖泊改库'
xls = r'D:\2021年项目\0708湖泊改库\all.xls'.decode('utf-8')
df = pd.read_excel(xls)
arcpy.env.workspace = path
walk = arcpy.da.Walk(r'D:\2021年项目\0708湖泊改库\湖泊修改MDB', datatype="FeatureClass", type='Point')
for i, v, m in walk:
    for s in m:
        try:
            if 'DMAP' in s:
                dmap =  os.path.join(i,s)
                dmap_shp = path + '\\' + 'stuff' + '\\' + '{}.shp'.format(dmap.encode('utf-8').split('.mdb')[0].split('\\')[-1])
                if '#' in dmap_shp:
                    dmap_shp = path + '\\' + 'stuff' + '\\' + '{}.shp'.format(dmap.encode('utf-8').split('.mdb')[0].split('\\')[-1].replace('#',''))
                arcpy.CopyFeatures_management(dmap,dmap_shp)
                arcpy.AddField_management(dmap_shp, '桩名'.decode('utf-8'), 'TEXT')
                arcpy.AddField_management(dmap_shp, '里程', 'TEXT')
                arcpy.AddField_management(dmap_shp, '所在位置'.decode('utf-8'), 'TEXT')
                arcpy.AddField_management(dmap_shp, '经度'.decode('utf-8'), 'TEXT')
                arcpy.AddField_management(dmap_shp, '纬度'.decode('utf-8'), 'TEXT')
                arcpy.AddField_management(dmap_shp, 'X', 'TEXT')
                arcpy.AddField_management(dmap_shp, 'Y', 'TEXT')
                arcpy.AddField_management(dmap_shp, 'H', 'TEXT')
                arcpy.CalculateField_management(dmap_shp, '桩名', '!NAME!', 'PYTHON_9.3')
                arcpy.CalculateField_management(dmap_shp, '所在位置', '!COUNTY! + !TOWN!', 'PYTHON_9.3')
                arcpy.AddGeometryAttributes_management(Input_Features=dmap_shp, Geometry_Properties="POINT_X_Y_Z_M",
                                                       Length_Unit="", Area_Unit="", Coordinate_System="4490")
                arcpy.CalculateField_management(dmap_shp, '经度', '!POINT_X!', 'PYTHON_9.3')
                arcpy.CalculateField_management(dmap_shp, '经度', "'E' + !经度!.split('.')[0] + '.' + !经度!.split('.')[1][0:8] + '°'.decode('utf-8')", 'PYTHON_9.3')
                arcpy.CalculateField_management(dmap_shp, '纬度', '!POINT_Y!', 'PYTHON_9.3')
                arcpy.CalculateField_management(dmap_shp, '纬度', "'N' + !纬度!.split('.')[0] + '.' + !纬度!.split('.')[1][0:8] + '°'.decode('utf-8')", 'PYTHON_9.3')
                arcpy.CalculateField_management(dmap_shp,'X',"'%.4f'%!shape.centroid.Y!",'PYTHON_9.3')
                arcpy.CalculateField_management(dmap_shp, 'Y', "'%.4f'%!shape.centroid.X!", 'PYTHON_9.3')
                arcpy.DeleteField_management(in_table=dmap_shp,drop_field="POINT_X;POINT_Y;POINT_Z;POINT_M;GB;NAME;HNNM;RIVER;BANK;NUM;TYPE;REASON;OWAG;SEWAGE;DEPT;TARGET;PRESENT;PROVINCE;CITY;COUNTY;TOWN;CODE;LONG;LAT;LOC;WRRG;NAME_RE;ENG_STAT;START_DATE;BDTM;ENG_GRAD;TEGR;MAIN_BUILD;INS_CAP;FIRM_POW;RAT_HEAD;UNNU;GMYA;ADAG;ADPR;ADM_DEP;CLAS;DGPROP;MODE;PAC;WRRCD;WFRCD;CAPLT_Y;CAPLT;DRNM;PROP;TOT_DIS;SEW_SOUR;MAIN_POLL;LIC_CODE;SETAG;WRRE;EXMAG;MNAG;MNFRG;COUNT_;FUNC;VOL;ELEV;STCD;STNM;STTP;WAIN_WASO_;AREA;USAGE_;WASU_OBJ_T;WASU_TOWN_;DPYN;YEAR;WQLE;GRWA_TYPE;WELL_NUMS;MUL_AVER_E;RANG;POP;GRAD;U_NAME;CORE;CONTA_PERS;ADDR;ZIP;OFFI_TEL;FAX;MAIN_DUTY;WORK_POP_N;TREA_UNIT_;SERV_OBJ;AERA;CHLE;MONI_CONT;TIME_;DATE_;NOTE;EFF_DATE;EXPR_DATE;STACOD;FEAID;VERS;RuleID")
                with arcpy.da.UpdateCursor(dmap_shp, ['桩名', '里程', 'H']) as yb:
                    for row in yb:
                        lc = df[df['桩名（编号）'.decode('utf-8')] == '{}'.format(row[0].encode('utf-8')).decode('utf-8')][
                            '里程'.decode('utf-8')].values[0]
                        elev = '%.2f' % \
                               df[df['桩名（编号）'.decode('utf-8')] == '{}'.format(row[0].encode('utf-8')).decode('utf-8')][
                                   'H'].values[0]
                        row[1] = lc
                        row[2] = elev
                        yb.updateRow(row)
                arcpy.TableToExcel_conversion(dmap_shp, r'D:\2021年项目\0708湖泊改库\xls\{}.xls'.format(dmap.encode('utf-8').split('.mdb')[0].split('\\')[-1]))

                print '{} is done'.format(dmap_shp)
        except Exception as e:
            print '{} {}'.format(dmap.encode('utf-8').split('.mdb')[0].split('\\')[-1],e)



#coding=utf-8
import arcpy
import os
import pandas as pd
path = r'D:\2021年项目\0708湖泊改库'
xls = r'D:\2021年项目\0708湖泊改库\all.xls'.decode('utf-8')
df = pd.read_excel(xls)
arcpy.env.workspace = path
walk = arcpy.da.Walk(r'D:\2021年项目\0708湖泊改库\湖泊修改MDB', datatype="FeatureClass", type='Point')
for i, v, m in walk:
    for s in m:
        if 'DMAP' in s:
            dmap =  os.path.join(i,s)
            print dmap.encode('utf-8').split('.mdb')[0].split('\\')[-1]
            dmap_shp = path + '\\' + 'stuff' + '\\' + '{}.shp'.format(dmap.encode('utf-8').split('.mdb')[0].split('\\')[-1])
            if '#' in dmap_shp:
                dmap_shp = path + '\\' + 'stuff' + '\\' + '{}.shp'.format(dmap.encode('utf-8').split('.mdb')[0].split('\\')[-1].replace('#',''))
            arcpy.CopyFeatures_management(dmap,dmap_shp)
            arcpy.AddField_management(dmap_shp, '桩名'.decode('utf-8'), 'TEXT')
            arcpy.AddField_management(dmap_shp, '里程', 'TEXT')
            arcpy.AddField_management(dmap_shp, '所在位置'.decode('utf-8'), 'TEXT')
            arcpy.AddField_management(dmap_shp, '经度'.decode('utf-8'), 'TEXT')
            arcpy.AddField_management(dmap_shp, '纬度'.decode('utf-8'), 'TEXT')
            arcpy.AddField_management(dmap_shp, 'X', 'TEXT')
            arcpy.AddField_management(dmap_shp, 'Y', 'TEXT')
            arcpy.AddField_management(dmap_shp, 'H', 'TEXT')
            arcpy.CalculateField_management(dmap_shp, '桩名', '!NAME!', 'PYTHON_9.3')
            arcpy.CalculateField_management(dmap_shp, '所在位置', '!COUNTY! + !TOWN!', 'PYTHON_9.3')
            arcpy.AddGeometryAttributes_management(Input_Features=dmap_shp, Geometry_Properties="POINT_X_Y_Z_M",
                                                   Length_Unit="", Area_Unit="", Coordinate_System="4490")
            arcpy.CalculateField_management(dmap_shp, '经度', '!POINT_X!', 'PYTHON_9.3')
            arcpy.CalculateField_management(dmap_shp, '经度', "'E' + !经度!.split('.')[0] + '.' + !经度!.split('.')[1][0:8] + '°'.decode('utf-8')", 'PYTHON_9.3')
            arcpy.CalculateField_management(dmap_shp, '纬度', '!POINT_Y!', 'PYTHON_9.3')
            arcpy.CalculateField_management(dmap_shp, '纬度', "'N' + !纬度!.split('.')[0] + '.' + !纬度!.split('.')[1][0:8] + '°'.decode('utf-8')", 'PYTHON_9.3')
            arcpy.CalculateField_management(dmap_shp,'X',"'%.4f'%!shape.centroid.Y!",'PYTHON_9.3')
            arcpy.CalculateField_management(dmap_shp, 'Y', "'%.4f'%!shape.centroid.X!", 'PYTHON_9.3')
            arcpy.DeleteField_management(in_table=dmap_shp,drop_field="POINT_X;POINT_Y;POINT_Z;POINT_M;GB;NAME;HNNM;RIVER;BANK;NUM;TYPE;REASON;OWAG;SEWAGE;DEPT;TARGET;PRESENT;PROVINCE;CITY;COUNTY;TOWN;CODE;LONG;LAT;LOC;WRRG;NAME_RE;ENG_STAT;START_DATE;BDTM;ENG_GRAD;TEGR;MAIN_BUILD;INS_CAP;FIRM_POW;RAT_HEAD;UNNU;GMYA;ADAG;ADPR;ADM_DEP;CLAS;DGPROP;MODE;PAC;WRRCD;WFRCD;CAPLT_Y;CAPLT;DRNM;PROP;TOT_DIS;SEW_SOUR;MAIN_POLL;LIC_CODE;SETAG;WRRE;EXMAG;MNAG;MNFRG;COUNT_;FUNC;VOL;ELEV;STCD;STNM;STTP;WAIN_WASO_;AREA;USAGE_;WASU_OBJ_T;WASU_TOWN_;DPYN;YEAR;WQLE;GRWA_TYPE;WELL_NUMS;MUL_AVER_E;RANG;POP;GRAD;U_NAME;CORE;CONTA_PERS;ADDR;ZIP;OFFI_TEL;FAX;MAIN_DUTY;WORK_POP_N;TREA_UNIT_;SERV_OBJ;AERA;CHLE;MONI_CONT;TIME_;DATE_;NOTE;EFF_DATE;EXPR_DATE;STACOD;FEAID;VERS;RuleID")
            with arcpy.da.UpdateCursor(dmap_shp, ['桩名', '里程', 'H']) as yb:
                for row in yb:
                    lc = df[df['桩名（编号）'.decode('utf-8')] == '{}'.format(row[0].encode('utf-8')).decode('utf-8')][
                        '里程'.decode('utf-8')].values[0]
                    elev = '%.2f' % \
                           df[df['桩名（编号）'.decode('utf-8')] == '{}'.format(row[0].encode('utf-8')).decode('utf-8')][
                               'H'].values[0]
                    row[1] = lc
                    row[2] = elev
                    yb.updateRow(row)
            arcpy.TableToExcel_conversion(dmap_shp, r'D:\2021年项目\0708湖泊改库\xls\{}.xls'.format(dmap.encode('utf-8').split('.mdb')[0].split('\\')[-1]))
            print '{} is done'.format(dmap_shp)
            #



