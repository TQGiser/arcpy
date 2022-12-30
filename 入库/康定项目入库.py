#coding=utf-8
import arcpy
import os
import pandas as pd
import F
arcpy.env.overwriteOutput = True
df = pd.read_excel(r'E:\2021年项目\1122康定1W段入库\康定市62条河流水系表.xlsx'.decode('utf-8'))
path = r'E:\2021年项目\1122康定1W段入库'
arcpy.env.workspace = path
xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-102.shp'
dmaps = F.listFiles(path,'线桩'.decode('utf-8'),'d')
for dmap in dmaps:
    riverName = arcpy.Describe(dmap).basename.encode('utf-8').replace('管理线桩','')
    dmapPath = arcpy.Describe(dmap).path
    print riverName
    for name, value in df.iterrows():
        if riverName in (df.loc[name,'河流名称'.decode('utf-8')]).encode('utf-8'):
            sx = (df.loc[name,'水系'.decode('utf-8')]).encode('utf-8')
    arcpy.AddField_management(dmap,'ELEV','DOUBLE')
    try:
        arcpy.CalculateField_management(dmap,'ELEV','!H!','PYTHON_9.3')
    except:
        pass
    if '备注'.decode('utf-8') in [field.name for field in arcpy.ListFields(dmap)]:
        try:
            arcpy.AddField_management(dmap,'RuleID','LONG')
        except:
            pass
        with arcpy.da.UpdateCursor(dmap,['SHAPE@','备注','RuleID']) as yb:
            for row in yb:
                if '告示牌'.decode('utf-8') in row[0]:
                    row[2] = 4
                elif '实体桩'.decode('utf-8') in row[0]:
                    row[2] = 2
                else:
                    row[2] = 27
                yb.updateRow(row)
    elif not 'RuleID' in [field.name for field in arcpy.ListFields(dmap)]:
        arcpy.AddField_management(dmap,'RuleID','LONG')
        with arcpy.da.UpdateCursor(dmap, 'RuleID') as yb:
            for row in yb:
                row[0] = 27
                yb.updateRow(row)
    elif 'RuleID' in [field.name for field in arcpy.ListFields(dmap)]:
        arcpy.CalculateField_management(dmap,'Ruleid',27,'PYTHON_9.3')
    mdb = arcpy.Copy_management(r'E:\2021年项目\1122康定1W段入库\模板.mdb',r'E:\2021年项目\1122康定1W段入库\mdb成果\{}.mdb'.format(riverName))
    dmapInMdb =  arcpy.Describe(mdb).children[0].catalogPath + '\\' + 'DMAP'
    arcpy.Append_management(dmap,dmapInMdb,schema_type='NO_TEST')
    with arcpy.da.UpdateCursor(dmapInMdb,['SHAPE@','NAME','COUNTY','TOWN','GB','TYPE','RuleID','DEPT','PROVINCE','CITY','RIVER','PAC','HNNM']) as yb:
        for row in yb:
            with arcpy.da.SearchCursor(xzjx,['SHAPE@','XZQMC','XZQMC_1','XZQDM']) as yb2:
                for row2 in yb2:
                    if row2[0].contains(row[0]):
                        print row[1],row2[1],row2[2]
                        row[2] = row2[2]
                        row[3] = row2[1]
                        row[11] = row2[3]
                        yb.updateRow(row)
            if '告示牌'.decode('utf-8') in row[1]:
                row[4] = 910104
                row[5] = '告示牌'
                row[6] = 4
            elif row[6] == 4:
                row[4] = 910104
                row[5] = '告示牌'
            elif row[6] == 2:
                row[4] = 910100
                row[5] = '实体桩'
            else:
                row[4] = 910100
                row[5] = '电子桩'
            row[7] = '康定市水利局'
            row[8] = '四川省'
            row[9] = '甘孜藏族自治州'
            row[10] = riverName
            row[12] = sx
            yb.updateRow(row)
    arcpy.RecalculateFeatureClassExtent_management(dmapInMdb)
    dmal = F.listFile(path,(riverName + '管理范围线').decode('utf-8'),'x')
    arcpy.AddField_management(dmal,'RIVER','TEXT')
    arcpy.AddField_management(dmal,'HNNM','TEXT')
    arcpy.AddField_management(dmal,'GB','LONG')
    try:
        arcpy.AddField_management(dmal,'RuleID','LONG')
    except:
        pass
    with arcpy.da.UpdateCursor(dmal,['RIVER','HNNM','RuleID','GB']) as yb:
        for row in yb:
            row[0] = riverName
            row[1] = sx
            row[2] = 2
            row[3] = 910100
            yb.updateRow(row)
    dmalInMdb = arcpy.Describe(mdb).children[0].catalogPath + '\\' + 'DMAL'
    arcpy.Append_management(dmal,dmalInMdb,schema_type='NO_TEST')
    arcpy.RecalculateFeatureClassExtent_management(dmalInMdb)
    hfclInMdb = arcpy.Describe(mdb).children[0].catalogPath + '\\' + 'HFCL'
    if F.listFile(dmapPath,'设计水位线'.decode('utf-8'),'x'):
        hfcl = F.listFile(dmapPath,'设计水位线'.decode('utf-8'),'x')
        arcpy.Append_management(hfcl, hfclInMdb, schema_type='NO_TEST')
    else:
        arcpy.Append_management(dmal,hfclInMdb, schema_type='NO_TEST')
    with arcpy.da.UpdateCursor(hfclInMdb,['GB','NAME','DATE_','VERS','RuleID']) as yb:
        for row in yb:
            row[0] = 290000
            row[1] = '设计水位线'.decode('utf-8')
            row[2] = '202111'
            row[3] = '2021'
            row[4] = 55
            yb.updateRow(row)
    arcpy.RecalculateFeatureClassExtent_management(hfclInMdb)
    F.calQZDLX(dmapPath)
    asline = dmapPath + '\\' + 'AssistLine.shp'
    dmaa = arcpy.FeatureToPolygon_management(in_features='{};{}'.format(dmal.encode('utf-8'), asline.encode('utf-8')),
                                      out_feature_class=dmapPath + '\\' + 'DMAA.shp')
    dmaaInMdb = arcpy.Describe(mdb).children[0].catalogPath + '\\' + 'DMAA'
    arcpy.Append_management(dmaa, dmaaInMdb, schema_type='NO_TEST')
    with arcpy.da.UpdateCursor(dmaaInMdb, ['GB', 'NAME','DATE_', 'VERS', 'RuleID', 'RIVER']) as yb:
        for row in yb:
            row[0] = 910100
            row[1] = '康定市{}河道管理范围'.format(riverName)                                                                              #########
            row[2] = '202111'
            row[3] = '2021'
            row[4] = 3
            row[5] = riverName
            yb.updateRow(row)
    arcpy.RecalculateFeatureClassExtent_management(dmaaInMdb)
