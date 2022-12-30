#coding=utf-8
import arcpy
import F
path = r'E:\数据\20220901\0822岸线规划'
path2 = path + '\\' + 'ok'
glqPath = r'E:\数据\20220901\0822岸线规划\glq'
glqs = F.listFiles(glqPath,'','m')
for glq in glqs:
    print glq
    spatial_ref = arcpy.Describe(glq).spatialReference
    riverName = arcpy.Describe(glq).baseName.replace('功能区'.decode('utf-8'), '')
    if '99' in spatial_ref.name:
        xzjx = path + '\\' + '甘孜县界-99.shp'
    elif '102' in spatial_ref.name:
        xzjx = path + '\\' + '甘孜县界-102.shp'
    tempShps = []
    with arcpy.da.SearchCursor(glq, ['SHAPE@','BH']) as yb1:
        for row1 in yb1:
            with arcpy.da.SearchCursor(xzjx,['SHAPE@','XZQMC']) as yb2:
                for row2 in yb2:
                    if row2[0].contains(row1[0]) or row2[0].overlaps(row1[0]):
                        print row1[1],row2[1]
                        arcpy.env.workspace = path2
                        path3 = path2 + '\\' + row2[1].encode('utf-8')
                        path4 = path3 + '\\' + riverName.encode('utf-8')
                        try:
                            arcpy.CreateFolder_management(path2,row2[1])
                        except:
                            pass
                        arcpy.env.workspace = path3
                        try:
                            arcpy.CreateFolder_management(path3, riverName)
                        except:
                            pass
                        arcpy.env.workspace = path4
                        try:
                            arcpy.CreateFileGDB_management(path4,'岸线规划功能分区')
                        except:
                            pass
                        tempShps.append(row2[0].intersect(row1[0],4))
                    # Aera = arcpy.CreateFeatureclass_management(path4, 'all.shp', 'POLYGON')
                    # cs = arcpy.da.InsertCursor(Aera, ['SHAPE@'])
                    # for shp in tempShps:
                    #     cs.insertRow([shp])

    break