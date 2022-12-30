#coding=utf-8
import arcpy
import os
import pandas as pd
import F
path = r'E:\测试文件夹\导SHP'
arcpy.env.workspace = path
mdbs = arcpy.ListFiles('*.mdb')
for mdb in mdbs:
    riverName = arcpy.Describe(mdb).name.replace('.mdb','')
    Folder = arcpy.CreateFolder_management(path,riverName)
    dmap = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'DMAP'
    dmal = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'DMAL'
    hfcl = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'HFCL'
    dmap_shp = path + '\\' + riverName.encode('utf-8') + '\\' + '{}dmap.shp'.format(riverName.encode('utf-8'))
    dmal_shp = path + '\\' + riverName.encode('utf-8') + '\\''{}dmal.shp'.format(riverName.encode('utf-8'))
    hfcl_shp = path + '\\' + riverName.encode('utf-8') + '\\''{}hfcl.shp'.format(riverName.encode('utf-8'))
    arcpy.CopyFeatures_management(dmap, dmap_shp)
    arcpy.CopyFeatures_management(dmal, dmal_shp)
    arcpy.CopyFeatures_management(hfcl, hfcl_shp)
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
    arcpy.CalculateField_management(dmap_shp, '里程', '!NUM!', 'PYTHON_9.3')
    arcpy.CalculateField_management(dmap_shp, '经度',
                                    "'E' + str('%0.8f'%round(float( !经度!) ,8)) + '°'.decode('utf-8')",
                                    'PYTHON_9.3')
    arcpy.CalculateField_management(dmap_shp, '纬度', '!POINT_Y!', 'PYTHON_9.3')
    arcpy.CalculateField_management(dmap_shp, '纬度',
                                    "'N' + str('%0.8f'%round(float( !纬度!) ,8)) + '°'.decode('utf-8')",
                                    'PYTHON_9.3')
    arcpy.CalculateField_management(dmap_shp, 'X', "'%.4f'%!shape.centroid.Y!", 'PYTHON_9.3')
    arcpy.CalculateField_management(dmap_shp, 'Y', "'%.4f'%!shape.centroid.X!", 'PYTHON_9.3')
    arcpy.CalculateField_management(dmap_shp, 'H', "'%.2f'%!ELEV!", 'PYTHON_9.3')
    arcpy.DeleteField_management(in_table=dmap_shp,
                                 drop_field="POINT_X;POINT_Y;POINT_Z;POINT_M;GB;NAME;HNNM;"
                                            "RIVER;BANK;NUM;TYPE;REASON;OWAG;SEWAGE;DEPT;TARGET;PRESENT;"
                                            "PROVINCE;CITY;COUNTY;TOWN;CODE;LONG;LAT;LOC;WRRG;NAME_RE;"
                                            "ENG_STAT;START_DATE;BDTM;ENG_GRAD;TEGR;MAIN_BUILD;INS_CAP;FIRM_POW;"
                                            "RAT_HEAD;UNNU;GMYA;ADAG;ADPR;ADM_DEP;CLAS;DGPROP;MODE;PAC;WRRCD;WFRCD;"
                                            "CAPLT_Y;CAPLT;DRNM;PROP;TOT_DIS;SEW_SOUR;MAIN_POLL;LIC_CODE;SETAG;WRRE;"
                                            "EXMAG;MNAG;MNFRG;COUNT_;FUNC;VOL;ELEV;STCD;STNM;STTP;WAIN_WASO_;"
                                            "AREA;USAGE_;WASU_OBJ_T;WASU_TOWN_;DPYN;YEAR;WQLE;GRWA_TYPE;"
                                            "WELL_NUMS;MUL_AVER_E;RANG;POP;GRAD;U_NAME;CORE;CONTA_PERS;ADDR;ZIP;OFFI_TEL;"
                                            "FAX;MAIN_DUTY;WORK_POP_N;TREA_UNIT_;SERV_OBJ;AERA;CHLE;MONI_CONT;TIME_;DATE_;NOTE;"
                                            "EFF_DATE;EXPR_DATE;STACOD;FEAID;VERS")
    arcpy.DeleteField_management(in_table=dmal_shp,
                                 drop_field="GB;NAME;HNNM;"
                                            "RIVER;BANK;NUM;TYPE;REASON;OWAG;SEWAGE;DEPT;TARGET;PRESENT;"
                                            "PROVINCE;CITY;COUNTY;TOWN;CODE;LONG;LAT;LOC;WRRG;NAME_RE;"
                                            "ENG_STAT;START_DATE;BDTM;ENG_GRAD;TEGR;MAIN_BUILD;INS_CAP;FIRM_POW;"
                                            "RAT_HEAD;UNNU;GMYA;ADAG;ADPR;ADM_DEP;CLAS;DGPROP;MODE;PAC;WRRCD;WFRCD;"
                                            "CAPLT_Y;CAPLT;DRNM;PROP;TOT_DIS;SEW_SOUR;MAIN_POLL;LIC_CODE;SETAG;WRRE;"
                                            "EXMAG;MNAG;MNFRG;COUNT_;FUNC;VOL;ELEV;STCD;STNM;STTP;WAIN_WASO_;"
                                            "AREA;USAGE_;WASU_OBJ_T;WASU_TOWN_;DPYN;YEAR;WQLE;GRWA_TYPE;"
                                            "WELL_NUMS;MUL_AVER_E;RANG;POP;GRAD;U_NAME;CORE;CONTA_PERS;ADDR;ZIP;OFFI_TEL;"
                                            "FAX;MAIN_DUTY;WORK_POP_N;TREA_UNIT_;SERV_OBJ;AERA;CHLE;MONI_CONT;TIME_;DATE_;NOTE;"
                                            "EFF_DATE;EXPR_DATE;STACOD;FEAID;VERS;RuleID")
    arcpy.DeleteField_management(in_table=hfcl_shp,
                                 drop_field="GB;NAME;HNNM;"
                                            "RIVER;BANK;NUM;TYPE;REASON;OWAG;SEWAGE;DEPT;TARGET;PRESENT;"
                                            "PROVINCE;CITY;COUNTY;TOWN;CODE;LONG;LAT;LOC;WRRG;NAME_RE;"
                                            "ENG_STAT;START_DATE;BDTM;ENG_GRAD;TEGR;MAIN_BUILD;INS_CAP;FIRM_POW;"
                                            "RAT_HEAD;UNNU;GMYA;ADAG;ADPR;ADM_DEP;CLAS;DGPROP;MODE;PAC;WRRCD;WFRCD;"
                                            "CAPLT_Y;CAPLT;DRNM;PROP;TOT_DIS;SEW_SOUR;MAIN_POLL;LIC_CODE;SETAG;WRRE;"
                                            "EXMAG;MNAG;MNFRG;COUNT_;FUNC;VOL;ELEV;STCD;STNM;STTP;WAIN_WASO_;"
                                            "AREA;USAGE_;WASU_OBJ_T;WASU_TOWN_;DPYN;YEAR;WQLE;GRWA_TYPE;"
                                            "WELL_NUMS;MUL_AVER_E;RANG;POP;GRAD;U_NAME;CORE;CONTA_PERS;ADDR;ZIP;OFFI_TEL;"
                                            "FAX;MAIN_DUTY;WORK_POP_N;TREA_UNIT_;SERV_OBJ;AERA;CHLE;MONI_CONT;TIME_;DATE_;NOTE;"
                                            "EFF_DATE;EXPR_DATE;STACOD;FEAID;VERS;RuleID")
    print '{} is done'.format(dmap_shp)
