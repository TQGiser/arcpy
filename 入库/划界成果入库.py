#coding=utf-8
import arcpy
import os
import pandas as pd
path = r'D:\2021年项目\0618湖泊入库\125个湖泊划界成果'.decode('utf-8')
outpath = r'D:\2021年项目\0618湖泊入库\mdb'.decode('utf-8')
workspace = path
shps = []
walk = arcpy.da.Walk(workspace, topdown=True, datatype="FeatureClass",type='Point')
xzjShp = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-99.shp'
gdbs = []
# for i,v,m in os.walk(path):
#     if 'gdb' in str(i.encode('utf-8')):
#         gdbs.append(i)
#
# for gdb in gdbs:
#     arcpy.env.workspace = gdb
#     dzz = gdb.split('\\')[5] + '电子桩'.decode('utf-8')
#     shp = gdb.replace('.gdb','') + '电子桩.shp'.decode('utf-8')
#     try:
#         arcpy.CopyFeatures_management(dzz,shp)
#     except:
#         print shp
for dirpath, dirnames, filenames in walk:
    for filename in filenames:
        if "桩".decode('utf-8')  in filename:
            shps.append(os.path.join(dirpath, filename))
for shp in shps:
    try:
        lackName = shp.split('\\')[5].encode('utf-8')
        mdbName = shp.split('\\')[4] + shp.split('\\')[5]
        spatial_ref = arcpy.Describe(shp).spatialReference
        if '99' in spatial_ref.name:
            mdb = arcpy.Copy_management(r'D:\2021年项目\0618湖泊入库\mdb模板\99.mdb',r'D:\2021年项目\0618湖泊入库\mdb\{}.mdb'.format(mdbName.encode('utf-8')))
        elif '102' in spatial_ref.name:
            mdb = arcpy.Copy_management(r'D:\2021年项目\0618湖泊入库\mdb模板\102.mdb',r'D:\2021年项目\0618湖泊入库\mdb\{}.mdb'.format(mdbName.encode('utf-8')))
        try:
            arcpy.AddField_management(shp,'NAME','TEXT')
            arcpy.AddField_management(shp,'NUM','TEXT')
            arcpy.CalculateField_management(shp,'NAME','!名称!','PYTHON_9.3')
            arcpy.CalculateField_management(shp, 'NUM', '!里程!', 'PYTHON_9.3')
        except:
            pass
        dmapPath = arcpy.Describe(mdb).path.encode('utf-8') + '\\' + '{}.mdb'.format(mdbName.encode('utf-8')) + '\\' + 'DLG' + '\\' + 'DMAP'
        arcpy.Append_management(inputs=shp,target=dmapPath,schema_type='NO_TEST')
        arcpy.RecalculateFeatureClassExtent_management(dmapPath)
        df = pd.read_excel(r'D:\2021年项目\0618湖泊入库\lakeData.xls'.decode('utf-8'))
        hnnm = df.loc[df['name'] == '{}'.format(lackName).decode('utf-8')]['d1'].values[0]                                  ############
        dlmc_1 = df.loc[df['name'] == '{}'.format(lackName).decode('utf-8')]['d2'].values[0]
        dlmc_2 = df.loc[df['name'] == '{}'.format(lackName).decode('utf-8')]['d3'].values[0]
        pacCode = df.loc[df['name'] == '{}'.format(lackName).decode('utf-8')]['d4'].values[0]
        with arcpy.da.UpdateCursor(dmapPath,['GB','HNNM','RIVER','DEPT','PROVINCE','CITY','COUNTY','TOWN','PAC','RuleID','NAME']) as yb:
            for row in yb:
                if '告示牌'.decode('utf-8') in row[10]:
                    row[0] = '910104'
                else:
                    row[0] = '910100'
                row[1] = hnnm
                row[2] = lackName
                row[3] = '甘孜藏族自治州水利局'
                row[4] = '四川省'
                row[5] = '甘孜藏族自治州'
                row[6] = dlmc_1
                row[7] = dlmc_2
                row[8] = pacCode
                if '告示牌'.decode('utf-8') in row[10]:
                    row[9] = 4
                else:
                    row[9] = 27
                yb.updateRow(row)
        walk2 = arcpy.da.Walk(arcpy.Describe(shp).path,datatype = "FeatureClass",type = 'Polyline')
        for dirpath2, dirnames2, filenames2 in walk2:
            for file2 in filenames2:
                dmal = os.path.join(dirpath2, file2)
        arcpy.AddField_management(dmal,'RIVER','TEXT')
        arcpy.AddField_management(dmal, 'NAME', 'TEXT')
        with arcpy.da.UpdateCursor(dmal,'RIVER') as yb:
            for row in yb:
                row[0] = lackName
                yb.updateRow(row)
        dmalPath = arcpy.Describe(mdb).path.encode('utf-8') + '\\' + '{}.mdb'.format(mdbName.encode('utf-8')) + '\\' + 'DLG' + '\\' + 'DMAL'
        arcpy.Append_management(inputs=dmal,target=dmalPath,schema_type='NO_TEST')
        arcpy.RecalculateFeatureClassExtent_management(dmalPath)
        with arcpy.da.UpdateCursor(dmalPath,['GB','HNNM','RuleID']) as yb:
            for row in yb:
                row[0] = '910100'
                row[1] = hnnm
                row[2] = 2
                yb.updateRow(row)
        hfclPath = arcpy.Describe(mdb).path.encode('utf-8') + '\\' + '{}.mdb'.format(mdbName.encode('utf-8')) + '\\' + 'DLG' + '\\' + 'HFCL'
        with arcpy.da.UpdateCursor(dmal,'NAME') as yb:
            for row in yb:
                row[0] = '设计洪水位线'.decode('utf-8')
                yb.updateRow(row)
        arcpy.Append_management(inputs=dmal, target=hfclPath, schema_type='NO_TEST')
        arcpy.RecalculateFeatureClassExtent_management(hfclPath)
        with arcpy.da.UpdateCursor(hfclPath,['GB','RuleID']) as yb:
            for row in yb:
                row[0] = '290000'
                row[1] = 55
                yb.updateRow(row)
        # dmaa = arcpy.FeatureToPolygon_management(dmal,r'D:\2021年项目\0618湖泊入库\stuff\{}.shp'.format(shp.split('\\')[5].encode('utf-8').replace('#','')))   ###########！！！！！去掉#
        dmaa = arcpy.FeatureToPolygon_management(dmal, r'D:\2021年项目\0618湖泊入库\stuff\{}.shp'.format(shp.split('\\')[5].encode('utf-8')))
        arcpy.AddField_management(dmaa,'RIVER','TEXT')
        with arcpy.da.UpdateCursor(dmaa,'RIVER') as yb:
            for row in yb:
                row[0] = shp.split('\\')[5]
                yb.updateRow(row)
        dmaaPath = arcpy.Describe(mdb).path.encode('utf-8') + '\\' + '{}.mdb'.format(mdbName.encode('utf-8')) + '\\' + 'DLG' + '\\' + 'DMAA'
        arcpy.Append_management(inputs=dmaa, target=dmaaPath, schema_type='NO_TEST')
        arcpy.RecalculateFeatureClassExtent_management(dmaaPath)
        with arcpy.da.UpdateCursor(dmaaPath,['GB','RIVER','OWAG','HNNM','RuleID']) as yb:
            for row in yb:
                row[0] = '910100'
                row[1] = lackName
                row[2] = '甘孜藏族自治州水利局'
                row[3] = hnnm
                row[4] = 3
                yb.updateRow(row)
        print '{} is done'.format((shp.encode('utf-8')))
    except Exception as e:
        print '{} {}'.format(shp.encode('utf-8'),e)