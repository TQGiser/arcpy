# coding=utf-8
import arcpy
import os
import shutil
import re
DLMC = '雅江县段'
path = r'D:\2021年项目\0413分幅2k'.decode('utf-8')
work_path = path.encode('utf-8') + '\\' + '分幅'
data_path = work_path + '\\' + '原始数据'
rasProcessed_path = work_path + '\\' + '影像预处理'
result_path = work_path + '\\' + '成果文件'
arcpy.CreateFolder_management(path, '分幅')
newForderName = ['原始数据', '影像预处理', '成果文件']
for i in newForderName:
    arcpy.CreateFolder_management(work_path, i)
arcpy.env.workspace = path                                                                  #预处理
yifileList = []
for i, v, m in os.walk(path):
    for name in m:
        yifileList.append(name)
for name in yifileList:
    ras = path + '\\' + name
    targetDir = data_path.decode('utf-8')
    shutil.move(ras, targetDir)
print('文件移动完成')
arcpy.env.workspace = data_path
for ras in arcpy.ListRasters('*','tif'):
    rasProcessed = rasProcessed_path.decode('utf-8') + '\\' + ras
    arcpy.env.compression = 'NONE'
    arcpy.CopyRaster_management(ras,rasProcessed,pixel_type='8_BIT_UNSIGNED',format='TIFF')
    arcpy.Delete_management(ras)
    arcpy.DefineProjection_management(rasProcessed,coor_system='4543')
print('影像预处理完成')
arcpy.env.workspace = data_path
tmpShp = r'fw.shp'
tmpShp2 = r'1：2000分幅图框.shp'
fwProcessed = 'rasFw.shp'
tkProcessed = 'TK.shp'
arcpy.env.outputZFlag = 'Enabled'
arcpy.CopyFeatures_management(tmpShp,fwProcessed)
arcpy.CopyFeatures_management(tmpShp2,tkProcessed)
arcpy.env.outputZFlag = 'Disabled'
joinShp = 'tkJoin.shp'
arcpy.SpatialJoin_analysis(tkProcessed,fwProcessed,joinShp,join_operation='JOIN_ONE_TO_MANY',join_type='KEEP_COMMON')
joinShpSorted = 'tkJoinSorted.shp'
arcpy.Sort_management(joinShp,joinShpSorted,sort_field="Shape ASCENDING", spatial_sort_method='UL')
arcpy.AddField_management(joinShpSorted,'图幅编号',field_type='TEXT')
with arcpy.da.UpdateCursor(joinShpSorted,['图幅编号','名称']) as yb:
    for row in yb:
        row[0] = row[1]
        yb.updateRow(row)
with arcpy.da.SearchCursor(joinShpSorted, ['图幅编号', 'SHAPE@']) as yb:
    for row in yb:
        foderName = row[0].encode('utf-8')
        arcpy.CreateFolder_management(result_path,foderName)
        buffDis = 10
        buffshp = row[1]
        buffshped = row[0] + 'ys' + '.shp'
        shapeName = buffshped.replace('-', '')
        print(shapeName)
        mask = arcpy.GraphicBuffer_analysis(buffshp, shapeName, buffDis)
        fgName = DLMC.decode('utf-8')
        rasname = row[0].split('%s' % fgName)[0]
        ras = rasProcessed_path.decode('utf-8') + '\\' + rasname + '.tif'
        rm = arcpy.sa.ExtractByMask(ras, mask)
        rm.save('{}.tif'.format(foderName))
        print(ras)
tiflis = []
tfwlis = []
u_data_path = data_path.decode('utf-8')
for i,v,m in os.walk(u_data_path):
    for name6 in m:
        if name6.endswith('.tif'):
            tiflis.append(name6)
    for name7 in m:
        if name7.endswith('.tfw'):
            tfwlis.append(name7)
for file2 in tfwlis:
    b = data_path.decode('utf-8') + '\\' + file2
    foder_name2 = result_path.decode('utf-8') + '\\' + file2.strip('.tfw')
    print(b)
    print(foder_name2)
    shutil.copy(b,foder_name2)
for file in tiflis:
    a =data_path.decode('utf-8') + '\\' + file
    foder_name = result_path.decode('utf-8') + '\\' + file.strip('.tif')
    print(a)
    print(foder_name)
    shutil.copy(a,foder_name)

