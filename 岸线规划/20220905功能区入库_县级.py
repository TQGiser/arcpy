#coding=utf-8
import arcpy
import F
import re
arcpy.env.overwriteOutput=True
path = r'E:\数据\20220901\0822岸线规划'
try:
    arcpy.CreateFolder_management(path,'县级成果')
except:
    pass
path2 = path + '\\' + '县级成果'
glqPath = r'E:\数据\20220901\0822岸线规划\glqCGCS2000\县级'
glqs = F.listFiles(glqPath,'','m')
xzjx = path + '\\' + '甘孜县界CGCS2000.shp'
for glq in glqs:
    spatial_ref = arcpy.Describe(glq).spatialReference
    riverName = arcpy.Describe(glq).baseName.replace('功能区'.decode('utf-8'), '')
    dmal = r'E:\数据\0822岸线规划\dmalCGCS2000\{}管理范围线.shp'.format(riverName.encode('utf-8'))
    zx = r'E:\数据\0822岸线规划\中线CGCS2000\{}校正后中线.shp'.format(riverName.encode('utf-8'))
    xzqList = []
    tempShps1 = []
    with arcpy.da.SearchCursor(glq, ['SHAPE@','BH','Name','AB','LENGTH','AREA','According']) as yb1:
        for row1 in yb1:
            with arcpy.da.SearchCursor(zx, 'SHAPE@') as yb4:
                for row2 in yb4:
                    LC = row2[0].measureOnLine(row1[0].labelPoint)

            with arcpy.da.SearchCursor(xzjx,['SHAPE@','XZQMC']) as yb2:
                for row2 in yb2:
                    if row2[0].contains(row1[0]) or row2[0].overlaps(row1[0]):
                        RL = re.findall('R|L',row1[1].encode('utf-8'))
                        NUM = '%03d'%int(''.join(re.findall('\d',row1[1].encode('utf-8'))))
                        BH = RL[0] + str(NUM)
                        fqmj = row1[5]
                        if row1[2] == "岸线保护区".decode('utf-8'):
                            type = 1
                        elif row1[2] == "岸线保留区".decode('utf-8'):
                            type = 2
                        elif row1[2] == "岸线控制利用区".decode('utf-8'):
                            type = 3
                        elif row1[2] == "岸线开发利用区".decode('utf-8'):
                            type = 4
                        xzq_sz = "甘孜藏族自治州"
                        xzq_qx = row2[1]
                        if row1[3] == "左岸".decode('utf-8'):
                            ab = 1
                        else:
                            ab = 2
                        with arcpy.da.SearchCursor(dmal, 'SHAPE@') as yb3:
                            for row3 in yb3:
                                if not row3[0].disjoint(row1[0]):
                                    clipLine = row1[0].intersect(row3[0],2)
                                    lng_e = clipLine.firstPoint.X
                                    lat_e = clipLine.firstPoint.Y
                                    lng_s = clipLine.lastPoint.X
                                    lat_s = clipLine.lastPoint.Y
                        basis = row1[6]
                        cn = [row1[0],row2[1],riverName,BH,fqmj,type,xzq_sz,xzq_qx,ab,row1[4],lng_s,lat_s,lng_e,lat_e,basis,LC]
                        tempShps1.append(cn)
                        if row2[1] not in xzqList:
                            xzqList.append(row2[1])
    tempShps = sorted(tempShps1,key=lambda x:x[-1], reverse=True)
    for xzq in xzqList:
        try:
            arcpy.CreateFolder_management(path2,xzq.encode('utf-8'))
        except:
            pass
        path3 = arcpy.CreateFolder_management(path2 + '\\' + xzq.encode('utf-8'),riverName.encode('utf-8'))
        Aera = arcpy.CreateFeatureclass_management(path3, 'all.shp', 'POLYGON')
        arcpy.DefineProjection_management(Aera,coor_system=spatial_ref)
        arcpy.AddField_management(Aera, 'gid', 'LONG')
        arcpy.AddField_management(Aera,'rname','TEXT',field_length=30)
        arcpy.AddField_management(Aera, 'regionid', 'TEXT',field_length = 5)
        arcpy.AddField_management(Aera, 'area', 'DOUBLE')
        arcpy.AddField_management(Aera, 'type', 'SHORT')
        arcpy.AddField_management(Aera, 'city', 'TEXT',field_length=30)
        arcpy.AddField_management(Aera, 'county', 'TEXT',field_length=30)
        arcpy.AddField_management(Aera, 'side', 'SHORT')
        arcpy.AddField_management(Aera, 'len', 'DOUBLE')
        arcpy.AddField_management(Aera, 'lng_s', 'DOUBLE')
        arcpy.AddField_management(Aera, 'lat_s', 'DOUBLE')
        arcpy.AddField_management(Aera, 'lng_e', 'DOUBLE')
        arcpy.AddField_management(Aera, 'lat_e', 'DOUBLE')
        arcpy.AddField_management(Aera,'basis','TEXT',field_length=200)
        arcpy.DeleteField_management(Aera,'id')
        arcpy.AddField_management(Aera, 'restraints', 'TEXT', field_length=1000)
        cs = arcpy.da.InsertCursor(Aera, ['SHAPE@','gid','rname','regionid','area','type','city','county','side','len','lng_s','lat_s','lng_e','lat_e','basis'])
        i = 1
        for cn in tempShps:
            if cn[1] == xzq:
                print cn[0],i, cn[2], cn[3], cn[4], cn[5], cn[6], cn[7], cn[8], cn[9],cn[10],cn[11],cn[12],cn[13],cn[14]
                cs.insertRow([cn[0],i, cn[2], cn[3], cn[4], cn[5], cn[6], cn[7], cn[8], cn[9],cn[10],cn[11],cn[12],cn[13],cn[14]])
                i+=1
        with arcpy.da.UpdateCursor(Aera, ['type', 'restraints']) as yb4:
            for row4 in yb4:
                if row4[0] == 1:
                    row4[1] = '禁止在划定的岸线保护区内投资建设除保障防洪安全、河势稳定、供水安全以及生态保护修复和环境治理项目、已建重要枢纽工程以外的项目。' \
                              '（一）为保障防洪安全和河势稳定划定的岸线保护区，禁止建设可能影响防洪安全、河势稳定的建设项目；' \
                              '（二）为保障供水安全划定的岸线保护区，区内禁止新建、扩建与供水设施和保护水源无关的建设项目；' \
                              '（三）为保护生态环境划定的岸线保护区，湿地范围内的岸线保护区禁止建设破坏湿地及其生态功能的项目；' \
                              '（四）为保护重要枢纽工程划定的岸线保护区，区内禁止建设可能影响其安全与正常运行的项目。'
                elif row4[0] == 2:
                    row4[1] = '禁止在岸线保留区内投资建设除保障防洪安全、河势稳定、供水安全、航道稳定以及生态保护修复和环境治理项目以外的项目。' \
                              '（一）规划期内，因防洪安全、河势稳定、供水安全、航道稳定及经济社会发展需要必须建设的防洪护岸、河道治理、取水、航道整治、公共管理、生态环境治理、国省重要基础设施等工程，须经充分论证并严格按照法律法规要求履行相关许可程序；' \
                              '（二）因暂不具备开发利用条件划定的岸线保留区，待河势趋于稳定，具备岸线开发利用条件后，或在不影响后续防洪治理、河道治理及航道整治的前提下，方可开发利用；' \
                              '（三）为满足生活生态岸线开发需要划定的岸线保留区，除建设生态公园、江滩风光带等项目外，不得建设其他生产设施；' \
                              '（四）规划期内暂无开发利用需求划定的岸线保留区，因经济社会发展确需开发利用的经充分论证并按照法律法规要求履行相关手续后，可参照岸线开发利用区或控制利用区管理；'
                yb4.updateRow(row4)
        gdb = arcpy.CreateFileGDB_management(path3,'岸线规划功能分区')
        arcpy.FeatureClassToFeatureClass_conversion(Aera,gdb,'岸线规划功能分区')
        arcpy.Delete_management(Aera)
