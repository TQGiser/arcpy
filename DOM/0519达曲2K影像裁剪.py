# coding=utf-8
import arcpy
import F

path = r'E:\2022年项目\0520达曲影像\达曲航飞影像\102'
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True
rases = arcpy.ListRasters('*.tif')
fw = F.listFile(path, 'fw', 'm')
tk = F.listFile(path, 'tk', 'm')
arcpy.GraphicBuffer_analysis(fw,path + '\\' + 'fw_buff_10.shp',10)
fw2 = F.listFile(path,'buff','m')
for ras in rases:
    print ras
    rasfile = path + '\\' + ras.encode('utf-8')
    arcpy.CreateFolder_management(path, ras.encode('utf-8').replace('.tif', ''))
    nP = path + '\\' + ras.replace('.tif', '').encode('utf-8')
    # arcpy.CreateFolder_management(nP, 'buffSHP')
    arcpy.CreateFolder_management(nP,'fwSHP')
    arcpy.CreateFolder_management(nP, 'extratRas')
    arcpy.CreateFolder_management(nP, 'clipRas')
    arcpy.CreateFolder_management(nP, 'okRas')

    with arcpy.da.SearchCursor(fw2, 'SHAPE@') as yb1:
        for row1 in yb1:
            with arcpy.da.SearchCursor(tk, ['SHAPE@', '图名']) as yb2:
                for row2 in yb2:
                    shp = row1[0].intersect(row2[0], 4)
                    if shp.area != 0.0:
                        # arcpy.GraphicBuffer_analysis(shp,nP + '\\' + 'buffSHP' + '\\' + row2[1].encode('utf-8').replace('-','') + '.shp',10)
                        arcpy.CopyFeatures_management(shp,nP + '\\' + 'fwSHP' + '\\' + row2[1].encode('utf-8').replace('-', '') + '.shp')
                        # arcpy.GraphicBuffer_analysis(shp, nP + '\\' + 'fwSHP' + '\\' + row2[1].encode('utf-8').replace('-', '') + '.shp', 0)
                        # mask1 = nP + '\\' + 'buffSHP' + '\\' + row2[1].encode('utf-8').replace('-', '') + '.shp'
                        mask2 = nP + '\\' + 'fwSHP' + '\\' + row2[1].encode('utf-8').replace('-', '') + '.shp'
                        with arcpy.da.SearchCursor(mask2,'SHAPE@') as yb3:
                            for row3 in yb3:
                                xmin = row3[0].extent.XMin
                                ymin = row3[0].extent.YMin
                                xmax = row3[0].extent.XMax
                                ymax = row3[0].extent.YMax
                        try:
                            envlope = "{} {} {} {}".format(xmin, ymin, xmax, ymax)
                            arcpy.env.parallelProcessingFactor = '0'
                            arcpy.env.compression = 'NONE'
                            arcpy.Clip_management(in_raster=ras,
                                                       rectangle="{} {} {} {}".format(xmin, ymin, xmax, ymax),
                                                       out_raster=nP + '\\' + 'clipRas' + '\\' + '{}.tif'.format(row2[1].encode('utf-8')),
                                                       in_template_dataset=mask2,
                                                       nodata_value="256",
                                                       clipping_geometry="ClippingGeometry",
                                                       maintain_clipping_extent="MAINTAIN_EXTENT")
                            clipRas = nP + '\\' + 'clipRas' + '\\' + '{}.tif'.format(row2[1].encode('utf-8'))
                            arcpy.env.cellSize = 0.2
                            cp = arcpy.CopyRaster_management(in_raster=clipRas,
                                                             out_rasterdataset=nP + '\\' + 'okRas' + '\\' + '{}.tif'.format(row2[1].encode('utf-8')),
                                                             config_keyword="",
                                                             background_value="",
                                                             nodata_value="",
                                                             onebit_to_eightbit="NONE",
                                                             colormap_to_RGB="NONE",
                                                             pixel_type="8_BIT_UNSIGNED",
                                                             scale_pixel_value="NONE",
                                                             RGB_to_Colormap="NONE",
                                                             format="TIFF",
                                                             transform="NONE")
                            print row2[1].encode('utf-8')  +  '     '  +   'is  done'
                        except:
                            pass
                        # except Exception as e:
                        #     print e

