# coding=utf-8
import arcpy
import F
arcpy.env.overwriteOutput = True
path = r'E:\2022年项目\1116小程序\temp\102'
outPath = r'E:\2022年项目\1116小程序\stuff'
WKID4326Path = r'E:\2022年项目\1116小程序\ok\WKID4326'
WKID4543Path = r'E:\2022年项目\1116小程序\ok\WKID4543'
dmaaTempPath = r'E:\2022年项目\1116小程序\dmaaTempPath'
dmaaFdPath = r'E:\2022年项目\1116小程序\dmaaFdPath'
dmalTempPath = r'E:\2022年项目\1116小程序\dmalTempPath'
xzq = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-102.shp'
dmals = F.listFiles(path,'','x')
for dmal in dmals:
    try:
        arcpy.CreateFolder_management(r'E:\2022年项目\1116小程序','ok')
        arcpy.CreateFolder_management(r'E:\2022年项目\1116小程序\ok', 'WKID4326')
        arcpy.CreateFolder_management(r'E:\2022年项目\1116小程序\ok', 'WKID4543')
    except:
        pass
    riverName = arcpy.Describe(dmal).baseName.encode('utf-8').replace('雅江县段','')
    print riverName
    arcpy.CreateFolder_management(r'E:\2022年项目\1116小程序\ok\WKID4326',riverName)
    arcpy.CreateFolder_management(r'E:\2022年项目\1116小程序\ok\WKID4543', riverName)
    dmalPath =arcpy.Describe(dmal).path
    lp = []
    spList = []
    with arcpy.da.SearchCursor(dmal,'SHAPE@') as yb:
        for row in yb:
            sp_x = row[0].firstPoint.X
            sp_y = row[0].firstPoint.Y
            cn = [sp_x,sp_y]
            spList.append(cn)
    lp.append(arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in spList])))
    epList = []
    with arcpy.da.SearchCursor(dmal,'SHAPE@') as yb:
        for row in yb:
            ep_x = row[0].lastPoint.X
            ep_y = row[0].lastPoint.Y
            cn = [ep_x,ep_y]
            epList.append(cn)
    lp.append(arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in epList])))
    Line = arcpy.CopyFeatures_management(lp, outPath + '\\' +'{}辅助线.shp'.format(riverName))
    asline = outPath + '\\' + '{}辅助线.shp'.format(riverName)

    dmaa_blank = arcpy.FeatureToPolygon_management(in_features='{};{}'.format(dmal.encode('utf-8'),asline),
                                      out_feature_class=dmaaTempPath + '\\' +'{}管理范围面.shp'.format(riverName))

    dmaa_fd = arcpy.Identity_analysis(in_features=dmaa_blank,
                                      identity_features=xzq,
                                      out_feature_class=dmaaFdPath +  '\\' + '{}分段管理范围面.shp'.format(riverName),
                                      join_attributes="ALL",
                                      cluster_tolerance="",
                                      relationship="NO_RELATIONSHIPS")
    dmaaCnList = []
    with arcpy.da.SearchCursor(dmaa_fd,['SHAPE@','XZQMC_1','XZQMC']) as yb:
        for row in yb:
            cn = [row[0],'{}管理范围面'.format(riverName),'四川省','甘孜藏族自治州',row[1],row[2]]
            dmaaCnList.append(cn)
    Dmaa = arcpy.CreateFeatureclass_management(WKID4543Path + '\\'+riverName,'管理范围面.shp', 'POLYGON')
    arcpy.DefineProjection_management(Dmaa, coor_system='4543')
    arcpy.AddField_management(Dmaa,'名称','TEXT')
    arcpy.AddField_management(Dmaa, '省', 'TEXT')
    arcpy.AddField_management(Dmaa, '市（州）', 'TEXT')
    arcpy.AddField_management(Dmaa, '区（县）', 'TEXT')
    arcpy.AddField_management(Dmaa, '乡镇', 'TEXT')
    cs = arcpy.da.InsertCursor(Dmaa, ['SHAPE@','名称','省','市（州）','区（县）','乡镇'])
    for cn in dmaaCnList:
        cs.insertRow(cn)
    arcpy.Project_management(Dmaa,WKID4326Path + '\\' + riverName + '\\' + '管理范围面.shp','4326')

    dmal_fd = arcpy.Identity_analysis(in_features=dmal,
                                      identity_features=xzq,
                                      out_feature_class=dmalTempPath +  '\\' + '{}分段管理范围线.shp'.format(riverName),
                                      join_attributes="ALL",
                                      cluster_tolerance="",
                                      relationship="NO_RELATIONSHIPS")
    cnList = []
    with arcpy.da.SearchCursor(dmal_fd,['SHAPE@','XZQMC_1','XZQMC','岸别']) as yb:
        for row in yb:
            cn = [row[0],'{}管理范围线'.format(riverName),'四川省','甘孜藏族自治州',row[1],row[2],row[3]]
            cnList.append(cn)
    Dmal = arcpy.CreateFeatureclass_management(WKID4543Path + '\\'+riverName,'管理范围线.shp', 'POLYLINE')
    arcpy.DefineProjection_management(Dmal, coor_system='4543')
    arcpy.AddField_management(Dmal,'名称','TEXT')
    arcpy.AddField_management(Dmal, '省', 'TEXT')
    arcpy.AddField_management(Dmal, '市（州）', 'TEXT')
    arcpy.AddField_management(Dmal, '区（县）', 'TEXT')
    arcpy.AddField_management(Dmal, '乡镇', 'TEXT')
    arcpy.AddField_management(Dmal, '岸别', 'TEXT')
    arcpy.DeleteField_management(Dmal,'Id')
    cs = arcpy.da.InsertCursor(Dmal, ['SHAPE@','名称','省','市（州）','区（县）','乡镇','岸别'])
    for cn in cnList:
        cs.insertRow(cn)
    arcpy.Project_management(Dmal, WKID4326Path + '\\' + riverName + '\\' + '管理范围线.shp', '4326')
