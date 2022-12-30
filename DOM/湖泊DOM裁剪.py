# coding=utf-8
import arcpy
import os
import shutil
import re
DLMC = '稻城县段'
path = r'C:\Users\Administrator\Desktop\新建文件夹\稻城影像'.decode('utf-8')
outpath = r'C:\Users\Administrator\Desktop\新建文件夹\新建文件夹'.decode('utf-8')
outpath2 = r'C:\Users\Administrator\Desktop\新建文件夹\新建文件夹 (2)'.decode('utf-8')
arcpy.env.workspace = path
rass = arcpy.ListRasters('*','TIF')
for ras in rass:
    with arcpy.da.SearchCursor('HC.shp',['SHAPE@','图幅号'.decode('utf-8')]) as yb:
        for row in yb:
            try:
                tifname = row[1].split('稻城县'.decode('utf-8'))[0] + '.tif'
                outRas = outpath + '\\' +row[1] + '.tif'
                # inras = arcpy.sa.ExtractByMask(tifname,row[0])
                # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
                # The following inputs are layers or table views: "卓玛拉措.tif", "Export_Output"
                inras = arcpy.Clip_management(in_raster=tifname, out_raster=outRas,
                                      in_template_dataset=row[0], nodata_value="255",
                                      clipping_geometry="ClippingGeometry", maintain_clipping_extent="MAINTAIN_EXTENT")
                arcpy.env.compression = 'NONE'
                outRas2 = outpath2 + '\\' + row[1] + '.tif'
                arcpy.CopyRaster_management(in_raster=inras,out_rasterdataset=outRas2,pixel_type='8_BIT_UNSIGNED')
                print '{} is done'.format(tifname)
            except Exception as e:
                print '{} {}'.format(tifname.encode('utf-8'), e)