# coding=utf-8
import arcpy
import F

path = r'E:\2022年项目\0422达曲影像\达曲'
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True
ras = arcpy.ListRasters('*.tif')
fw = F.listFile(path, 'fw', 'm')
tk = F.listFile(path, 'tk', 'm')
with arcpy.da.SearchCursor(fw, 'SHAPE@') as yb1:
    for row1 in yb1:
        with arcpy.da.SearchCursor(tk, ['SHAPE@', '图号']) as yb:
            for row in yb:
                try:
                    print row[1]
                    shp = row[0].intersect(row1[0], 4)
                    tempShp = row[1] + '.shp'
                    mask = arcpy.GraphicBuffer_analysis(shp, path.decode('utf-8') + '\\' + 'temp' + '\\' + tempShp, 10)
                    shp2 = path.decode('utf-8') + '\\' + 'temp' + '\\' + row[1] + '.shp'
                    with arcpy.da.SearchCursor(shp2, 'SHAPE@') as yb2:
                        for row2 in yb2:
                            xmin = row2[0].extent.XMin
                            ymin = row2[0].extent.YMin
                            xmax = row2[0].extent.XMax
                            ymax = row2[0].extent.YMax
                    rm = arcpy.sa.ExtractByMask(ras[0], shp2)
                    rm.save(path.decode('utf-8') + '\\' + 'rastemp' + '\\' + '{}.tif'.format(row[1]))
                    print 'extract ok'
                    arcpy.ProjectRaster_management(in_raster=rm,
                                                   out_raster=path.decode(
                                                       'utf-8') + '\\' + 'projRas_84' + '\\' + '{}.tif'.format(row[1]),
                                                   out_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]",
                                                   resampling_type="NEAREST",
                                                   cell_size="9.83824498837137E-06 9.83824498837137E-06",
                                                   geographic_transform="WGS84-99", Registration_Point="",
                                                   in_coor_system="PROJCS['China_Geodetic_Coordinate_System_2000_Transverse_Mercator',GEOGCS['GCS_China_Geodetic_Coordinate_System_2000',DATUM['D_China_2000',SPHEROID['CGCS2000',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['false_easting',500000.0],PARAMETER['false_northing',0.0],PARAMETER['central_meridian',99.0],PARAMETER['scale_factor',1.0],PARAMETER['latitude_of_origin',0.0],UNIT['Meter',1.0]]",
                                                   vertical="NO_VERTICAL")

                    pr_84 = path.decode('utf-8') + '\\' + 'projRas_84' + '\\' + '{}.tif'.format(row[1])
                    # pr_84_ras = arcpy.Raster("{}".format(pr_84.encode('utf-8')))

                    print 'proj84 ok'
                    arcpy.ProjectRaster_management(in_raster=pr_84.encode('utf-8'),
                                                   out_raster=path.decode(
                                                       'utf-8') + '\\' + 'projRas_99' + '\\' + '{}.tif'.format(row[1]),
                                                   out_coor_system="PROJCS['CGCS2000_3_Degree_GK_CM_99E',GEOGCS['GCS_China_Geodetic_Coordinate_System_2000',DATUM['D_China_2000',SPHEROID['CGCS2000',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',99.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]",
                                                   resampling_type="NEAREST", cell_size="0.5 0.5",
                                                   geographic_transform="WGS84-99",
                                                   Registration_Point="",
                                                   in_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]",
                                                   vertical="NO_VERTICAL")
                    print 'proj99 ok'
                    pr_99 = path.decode('utf-8') + '\\' + 'projRas_99' + '\\' + '{}.tif'.format(row[1])
                    envlope = "{} {} {} {}".format(xmin, ymin, xmax, ymax)
                    print xmin, ymin, xmax, ymax
                    # break
                    arcpy.env.parallelProcessingFactor = '0'
                    arcpy.env.compression = 'NONE'
                    cr = arcpy.Clip_management(in_raster=pr_99.encode('utf-8'),
                                               rectangle="{} {} {} {}".format(xmin, ymin, xmax, ymax),
                                               out_raster=path.decode('utf-8') + '\\' + 'clipRas' + '\\' + '{}.tif'.format(
                                                   row[1]),
                                               in_template_dataset=shp2.encode('utf-8'),
                                               nodata_value="255",
                                               clipping_geometry="ClippingGeometry",
                                               maintain_clipping_extent="MAINTAIN_EXTENT")
                    print 'clip ok'
                    clip_ras = path.decode('utf-8') + '\\' + 'clipRas' + '\\' + '{}.tif'.format(row[1])
                    arcpy.env.cellSize = 0.5
                    cp = arcpy.CopyRaster_management(in_raster=clip_ras.encode('utf-8'),
                                                     out_rasterdataset=path.decode(
                                                         'utf-8') + '\\' + 'copyRas' + '\\' + '{}.tif'.format(row[1]),
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
                    print 'copy ok'
                except:
                    pass
