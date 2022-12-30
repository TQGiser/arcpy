#coding=utf-8
import arcpy
import os
path = r'E:\2022年项目\0422达曲影像\达曲'
arcpy.env.workspace = path
arcpy.env.overwriteOutput=True
walk = arcpy.da.Walk(path,topdown = True,datatype='RasterDataset',type='TIF')
tiflst = []
for i,v,m in walk:
    for tif in m:
        tiflst.append(os.path.join(i,tif))
gdb = arcpy.CreateFileGDB_management(path,'temp')
mosaicDataPath = path + '\\' + 'temp.gdb'

mosaicData = arcpy.CreateMosaicDataset_management(mosaicDataPath,'fw',coordinate_system='4543')
for tif in tiflst:
    arcpy.AddRastersToMosaicDataset_management(mosaicData, 'Raster Dataset', tif)
arcpy.DefineMosaicDatasetNoData_management(mosaicData,'3',bands_for_nodata_value="ALL_BANDS '255 255 255'")
arcpy.BuildFootprints_management(mosaicData,approx_num_vertices=-1)
fwShp = path + '\\' + 'fw.shp'
eage = path + '\\' + 'temp.gdb' + '\\' + 'AMD_fw_BND'
arcpy.env.outputZFlag = 'Enabled'
arcpy.CopyFeatures_management(eage,fwShp)
