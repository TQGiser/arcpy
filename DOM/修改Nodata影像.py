#coding=utf-8
import arcpy
path = r'E:\测试文件夹\达曲甘孜县段-001'.decode('utf-8')
outpath = path + '\\' + 'stuff'
arcpy.env.workspace = path
tif = arcpy.ListRasters('','tif')
tifName = tif[0].split('.')[0].encode('utf-8')
arcpy.CreateFolder_management(path,'stuff')
arcpy.env.workspace = outpath
b1 =path + '\\' + tif[0] + '\\' + 'Band_1'
b1_nodata = arcpy.gp.IsNull_sa(b1)
b1_temp = outpath +'\\' + 'b1_temp.tif'
b1_ok = arcpy.gp.Con_sa(b1_nodata,254,b1_temp,b1,"value = 1")
b2 = path + '\\' + tif[0] + '\\' + 'Band_2'
b2_nodata = arcpy.gp.IsNull_sa(b2)
b2_temp = outpath +'\\' + 'b2_temp.tif'
b2_ok = arcpy.gp.Con_sa(b2_nodata,254,b2_temp,b2,"value = 1")
b3 = path + '\\' + tif[0] + '\\' + 'Band_3'
b3_nodata = arcpy.gp.IsNull_sa(b3)
b3_temp = outpath +'\\' + 'b3_temp.tif'
b3_ok = arcpy.gp.Con_sa(b3_nodata,254,b3_temp,b3,"value = 1")
okRas = path.encode('utf-8') + '\\' + '{}ok.tif'.format(tifName)
arcpy.CompositeBands_management(in_rasters="{};{};{}".format(b1_temp.encode('utf-8'),b2_temp.encode('utf-8'),b3_temp.encode('utf-8')), out_raster=okRas)