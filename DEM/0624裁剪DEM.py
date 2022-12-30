#coding=utf-8
import arcpy
import os
import pandas as pd
import pinyin
arcpy.env.overwriteOutput = True
path = r'E:\2021年项目\新建文件夹\DEM\czlbg'
arcpy.env.workspace = path
dem = r'D:\2021年项目\0827裁剪DEM\cjdem'
tk = r'D:\2021年项目\0827裁剪DEM\格则沟图框面.shp'.decode('utf-8')
arcpy.CreateFolder_management(path,'stuff')
arcpy.CreateFolder_management(path,'新建文件夹')
arcpy.CreateFolder_management(path,'OK')
arcpy.CreateFolder_management(path,'temp')
with arcpy.da.SearchCursor(tk,['SHAPE@','图名']) as yb:
    for row in yb:
        a = row[1].encode('utf-8')
        print a
        arcpy.CreateFolder_management(r'D:\2021年项目\0827裁剪DEM\stuff',a)
        arcpy.CreateFolder_management(r'D:\2021年项目\0827裁剪DEM\新建文件夹', a)
        arcpy.CreateFolder_management(r'D:\2021年项目\0827裁剪DEM\OK', a)
        demName = pinyin.get_initial('{}'.format(a)).replace(' ', '').capitalize()
        demFolderName =  pinyin.get_initial('{}'.format(a)).replace(' ', '')
        demByTk = r'D:\2021年项目\0827裁剪DEM\stuff'.decode('utf-8') + '\\' + a.decode('utf-8') + '\\' + demName.decode('utf-8')
        shpName = a.replace('-','')
        tk = arcpy.GraphicBuffer_analysis(row[0],r'D:\2021年项目\0827裁剪DEM\stuff\{}.shp'.format(shpName), 5)
        ysdem = arcpy.Clip_management(in_raster=dem, out_raster=demByTk, in_template_dataset=tk,nodata_value="-9999",
                              clipping_geometry="ClippingGeometry", maintain_clipping_extent="MAINTAIN_EXTENT")
        okdem = r'D:\2021年项目\0827裁剪DEM\新建文件夹'.decode('utf-8') + '\\' + a.decode('utf-8') + '\\' + demName.decode('utf-8')
        arcpy.Resample_management(ysdem,okdem,'2')
        arcpy.env.workspace = r'D:\2021年项目\0827裁剪DEM\temp'
        dem_nodata = arcpy.gp.IsNull_sa(okdem)
        dem999 = r'D:\2021年项目\0827裁剪DEM\OK'.decode('utf-8') + '\\' + a.decode('utf-8') + '\\' + demName.decode('utf-8')
        arcpy.gp.Con_sa(dem_nodata, -9999, dem999, okdem, "value = 1")
        renameFolder = r'D:\2021年项目\0827裁剪DEM\OK'.decode('utf-8') + '\\' + a.decode('utf-8')
        os.chdir(renameFolder)  # 将dem小写转为大写开头
        ys = '{}'.format(demFolderName.decode('utf-8'))
        print ys
        print type(ys)
        new = '{}'.format(demFolderName.decode('utf-8').capitalize())
        print new
        print type(new)
        os.rename(ys,new)
        # arcpy.DefineProjection_management(tkdem, spatial_ref)  # dem改名后需重定义投影

