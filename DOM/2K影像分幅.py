#coding=utf-8
import arcpy
import os
import shutil
import re
out_path = r"D:\2021年项目\TEST\过程文件".decode('utf-8')
path = r'E:\达曲影像\process'.decode('utf-8')
result_path = r'D:\2021年项目\TEST\成果文件'.decode('utf-8')
raster_folder = r'D:\2021年项目\TEST\优化图像'.decode('utf-8')
arcpy.env.workspace = path
os.chdir(path)
rasters_ys = []
rasters_8bit = []
clip_all_frame = []

DLMC = '雅江县段'
for i,v,m in os.walk(path):
    for rasname in m:
        if rasname.endswith('.tif'):
            rasters_ys.append(rasname)
for name in rasters_ys:
    print(name)
    fn = name.strip('.tif')
    ras = arcpy.Raster(name)
    arcpy.DefineProjection_management(name, coor_system='4543')
    ex = ras.extent
    x = ex.XMin
    y = ex.YMin
    x1 = ex.XMax
    y1 = ex.YMax
    xlen = ex.XMax - ex.XMin
    ylen = ex.YMax - ex.YMin
    cod1 = str(x) + ' ' + str(y)
    cod2 = str(x) + ' ' + str(y1 + 10)
    cod3 = str(x1) + ' ' + str(y1)
    print(cod1, cod2, cod3)
    arcpy.env.workspace = out_path  # 设置生成文件地址
    ras_fw = r'fw.shp'
    arcpy.env.outputZFlag = 'Disabled'
    fn1_fishname_all = fn + '.shp'
    arcpy.CreateFishnet_management(fn1_fishname_all,template= ras,labels= 'NO_LABELS',
                                  origin_coord=cod1,y_axis_coord=cod2,corner_coord = cod3,number_columns = '',
                                  number_rows = '' ,geometry_type='POLYGON',cell_width=1000,cell_height=1000)

    arcpy.env.outputZFlag = 'Enabled'
    fn3 = fn + '_copy' + '.shp'
    arcpy.CopyFeatures_management(fn1_fishname_all, fn3)
    fn4 = fn + '_cross' + '.shp'
    arcpy.SpatialJoin_analysis(fn3,ras_fw,fn4,join_operation='JOIN_ONE_TO_MANY',join_type='KEEP_COMMON')
    with arcpy.da.UpdateCursor(in_table=fn4, field_names="NAME") as yb:
      for row in yb:
         if row[0] == ' ':
            yb.deleteRow()
    arcpy.DeleteField_management(in_table=fn4, drop_field="Join_Count;TARGET_FID;JOIN_FID;Id;Id_1")
    arcpy.AddField_management(fn4, '图幅编号', 'TEXT', field_length='50')
    crs_sorted = fn + '_sorted' + '.shp'
    arcpy.Sort_management(fn4, crs_sorted, sort_field="Shape ASCENDING", spatial_sort_method='UL')
    # arcpy.Delete_management(fn3)
    # arcpy.Delete_management(ras_fw)
    # arcpy.Delete_management(fn1_fishname_all)
    # arcpy.Delete_management(fn4)
    tif_transto_8bit = name.strip('.tif') + '8bit' + '.tif'
    arcpy.env.compression = 'NONE'
    arcpy.CopyRaster_management(name, tif_transto_8bit, pixel_type='8_BIT_UNSIGNED', format='TIFF')
    arcpy.env.workspace = out_path
    with arcpy.da.UpdateCursor(crs_sorted, ['图幅编号', 'NAME', 'DLMC']) as yb:
            step = 1
            for row in yb:
               bh = '%03.0f' % step
               step += 1
               fh = '-'
               row[0] = row[1] + row[2] + fh + bh
               yb.updateRow(row)
    with arcpy.da.SearchCursor(crs_sorted,['图幅编号','SHAPE@']) as yb:
       for row in yb:
          foderName = row[0].encode('utf-8')
          arcpy.CreateFolder_management(out_path,foderName)
          buffDis = 10
          buffshp = row[1]
          buffshped = row[0] + '.shp'
          shapeName =buffshped.replace('-','')
          print(shapeName)
          mask = arcpy.GraphicBuffer_analysis(buffshp, shapeName, buffDis)
          ras2 = tif_transto_8bit
          rm = arcpy.sa.ExtractByMask(ras2, mask)
          rm.save('{}.tif'.format(foderName))
for i,v,m in os.walk(out_path):
    for name5 in m:
        if name5.endswith('8bit.tif'):
            delname = name5
            del_ras = arcpy.Raster(delname)
            arcpy.Delete_management(del_ras)
os.chdir(out_path)
tiflis = []
tfwlis = []
for i,v,m in os.walk(out_path):
   for name6 in m:
     if name6.endswith('.tif'):
         tiflis.append(name6)
   for name7 in m:
     if name7.endswith('.tfw'):
         tfwlis.append(name7)
for file2 in tfwlis:
   b = file2
   foder_name2 = b.strip('.tfw')
   shutil.copy(b,foder_name2)
for file in tiflis:
   a = os.path.join(out_path,file)
   foder_name = a.strip('.tif')
   print(a)
   print(foder_name)
   shutil.copy(a,foder_name)

