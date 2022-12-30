#coding=utf-8
import arcpy
path = r'E:\数据\甘孜乡镇\WGS84-总县界'
arcpy.env.workspace = path
gzxj = r'E:\数据\甘孜乡镇\WGS84-总县界\甘孜县界-84.shp'
dem = r'E:\数据\甘孜藏族自治州12.5米DEM\甘孜藏族自治州.tif'
with arcpy.da.SearchCursor(gzxj,['SHAPE@','XZQMC']) as yb:
    for row in yb:
        # print type(row[1].encode('utf-8'))
        outExtractByMask = arcpy.sa.ExtractByMask(dem,row[0])
        outExtractByMask.save(path + '\\' + '{}.tif'.format(row[1].encode('utf-8')))
