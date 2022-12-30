#coding=utf-8
import arcpy
import os
import pandas as pd
import F
arcpy.env.overwriteOutput = True
df = pd.read_excel(r'E:\2021年项目\1130理塘1W段划界\理塘县73条县级河流长度统计表.xlsx'.decode('utf-8'))
path = r'E:\2021年项目\1202理塘2K划界\勇杰几玛\shape'
arcpy.env.workspace = path
dmaps = F.listFiles(path,'线桩'.decode('utf-8'),'d')

for dmap in dmaps:
    spatial_ref = arcpy.Describe(dmap).spatialReference
    if '99' in spatial_ref.name:
        xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-99.shp'
        fdh = 99
        mdbmb = r'E:\2021年项目\1130理塘1W段划界\mdb模板\99.mdb'
    elif '102' in spatial_ref.name:
        xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-102.shp'
        fdh = 102
        mdbmb = r'E:\2021年项目\1130理塘1W段划界\mdb模板\102.mdb'
    riverName = arcpy.Describe(dmap).basename.encode('utf-8').replace('管理线桩','')
    dmapPath = arcpy.Describe(dmap).path
    print riverName
    for name, value in df.iterrows():
        if riverName in (df.loc[name,'河流'.decode('utf-8')]).encode('utf-8'):
            sx = (df.loc[name,'水系'.decode('utf-8')]).encode('utf-8')
    arcpy.AddField_management(dmap,'ELEV','DOUBLE')
    try:
        arcpy.CalculateField_management(dmap,'ELEV','!H!','PYTHON_9.3')
    except:
        pass
    try:
        arcpy.CalculateField_management(dmap,'ELEV','!h!','PYTHON_9.3')
    except:
        pass
    mdb = arcpy.Copy_management(mdbmb,r'E:\测试文件夹\导SHP\{}.mdb'.format(riverName))
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
            if row[6] == 4:
                row[4] = 910104
                row[5] = '告示牌'
            elif row[6] == 2:
                row[4] = 910100
                row[5] = '实体桩'
            elif row[6] == 3:
                row[4] = 910102
                row[5] = '移位桩'
            else:
                row[4] = 910100
                row[5] = '电子桩'
            row[7] = '理塘县水利局'
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
            row[1] = '理塘县{}河道管理范围'.format(riverName)                                                                              #########
            row[2] = '202111'
            row[3] = '2021'
            row[4] = 3
            row[5] = riverName
            yb.updateRow(row)
    arcpy.RecalculateFeatureClassExtent_management(dmaaInMdb)

