#coding=utf-8
import arcpy
import F
path = r'E:\2022年项目\1230小程序'
dmaa_all = F.listFile(path + '\\' +'99','dmaa','m')
dmal_all = F.listFile(path + '\\' +'99','dmal','x')
try:
    arcpy.CreateFolder_management(path,'ok')
except:
    pass
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True
riverList = []
with arcpy.da.SearchCursor(dmaa_all,['SHAPE@','名称','省','市（州）','区（县）','乡镇']) as yb:
    for row in yb:
        riverName = row[1].encode('utf-8').replace('管理范围面','')
        riverList.append(riverName)
        print riverName + 'dmaa'
        try:
            arcpy.CreateFolder_management(path + '\\' + 'ok',riverName)
        except:
            pass
        cn = [row[0],row[1],row[2], row[3], row[4], row[5]]
        dmaa = arcpy.CreateFeatureclass_management(path + '\\' +'ok' + '\\' + riverName,'{}管理范围面.shp'.format(riverName),'POLYGON')
        arcpy.DefineProjection_management(dmaa,coor_system='4543')
        arcpy.AddField_management(dmaa,'名称','TEXT')
        arcpy.AddField_management(dmaa, '省', 'TEXT')
        arcpy.AddField_management(dmaa, '市（州）', 'TEXT')
        arcpy.AddField_management(dmaa, '区（县）', 'TEXT')
        arcpy.AddField_management(dmaa, '乡镇', 'TEXT')
        cs = arcpy.da.InsertCursor(dmaa,['SHAPE@','名称','省','市（州）','区（县）','乡镇'])
        cs.insertRow(cn)
for river in riverList:
    expression = "名称 = '{}管理范围线'".format(river)
    cnList =[]
    with arcpy.da.SearchCursor(dmal_all,['SHAPE@','名称','省','市（州）','区（县）','乡镇','岸别'],where_clause=expression) as yb:
        for row in yb:
            riverName = row[1].encode('utf-8').replace('管理范围线','')
            print riverName + 'dmal'
            try:
                arcpy.CreateFolder_management(path + '\\' + 'ok',riverName)
            except:
                pass
            cn = [row[0],row[1],row[2], row[3], row[4], row[5],row[6]]
            cnList.append(cn)
            try:
                dmal = arcpy.CreateFeatureclass_management(path + '\\'+ 'ok' + '\\' + riverName,'{}管理范围线.shp'.format(riverName),'POLYLINE')
            except:
                pass
            arcpy.DefineProjection_management(dmal,coor_system='4543')
            arcpy.AddField_management(dmal,'名称','TEXT')
            arcpy.AddField_management(dmal, '省', 'TEXT')
            arcpy.AddField_management(dmal, '市（州）', 'TEXT')
            arcpy.AddField_management(dmal, '区（县）', 'TEXT')
            arcpy.AddField_management(dmal, '乡镇', 'TEXT')
            arcpy.AddField_management(dmal, '岸别', 'TEXT')
            cs = arcpy.da.InsertCursor(dmal,['SHAPE@','名称','省','市（州）','区（县）','乡镇','岸别'])
            for cn in cnList:
                cs.insertRow(cn)