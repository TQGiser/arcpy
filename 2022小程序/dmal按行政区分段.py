# coding=utf-8
import arcpy
import F
arcpy.env.overwriteOutput = True
path = r'E:\2022年项目\1116小程序\temp\102'
outpath = r'E:\2022年项目\1116小程序\dmal_fd'
okPath = r'E:\2022年项目\1116小程序\ok'
dmals = F.listFiles(path,'','x')
xzq = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-102.shp'
for dmal in dmals:
    cnList = []
    riverName = arcpy.Describe(dmal).baseName.encode('utf-8').replace('雅江县段','')
    arcpy.CreateFolder_management(r'E:\2022年项目\1116小程序\dmal_fd', riverName)
    dmal_fd = arcpy.Identity_analysis(in_features=dmal,
                            identity_features=xzq,
                            out_feature_class=outpath + '\\' + riverName + '\\' + '管理范围线.shp',
                            join_attributes="ALL",
                            cluster_tolerance="",
                            relationship="NO_RELATIONSHIPS")
    with arcpy.da.SearchCursor(dmal_fd,['SHAPE@','县（区）','XZQMC','岸别']) as yb:
        for row in yb:
            cn = [row[0],'{}管理范围线'.format(riverName),'四川省','甘孜藏族自治州','雅江县',row[2],row[3]]
            cnList.append(cn)
    Dmal = arcpy.CreateFeatureclass_management(okPath, '{}.shp'.format(riverName), 'POLYLINE')
    arcpy.AddField_management(Dmal,'名称','TEXT')
    arcpy.AddField_management(Dmal, '省', 'TEXT')
    arcpy.AddField_management(Dmal, '市（州）', 'TEXT')
    arcpy.AddField_management(Dmal, '区（县）', 'TEXT')
    arcpy.AddField_management(Dmal, '乡镇', 'TEXT')
    arcpy.AddField_management(Dmal, '岸别', 'TEXT')
    cs = arcpy.da.InsertCursor(Dmal, ['SHAPE@','名称','省','市（州）','区（县）','乡镇','岸别'])
    for cn in cnList:
        cs.insertRow(cn)