# coding=utf-8
import arcpy
import pinyin
path = r'D:\2021年项目\0616WL'.decode('utf-8')
arcpy.env.workspace = path
arcpy.CreateFolder_management(path,'dem')
arcpy.CreateFolder_management(path,'OK')
arcpy.CreateFolder_management(path,'stuff')
boua = 'BOUA.shp'
spatial_ref = arcpy.Describe(boua).spatialReference
with arcpy.da.SearchCursor('BOUA.shp',['SHAPE@','NAME']) as yb:
    for row in yb:
        try:
            lakeName = row[1].encode('utf-8')
            buffBouaName = str(lakeName)  + 'Buff'
            buffBoua = arcpy.GraphicBuffer_analysis(row[0],r'D:\2021年项目\0616WL\stuff\{}'.format(buffBouaName),10)
            clipTerlName = str(lakeName) + '.shp'
            clipTerl = arcpy.Clip_analysis('terl.shp',buffBoua,r'D:\2021年项目\0616WL\stuff\{}'.format(clipTerlName))
            tinName = str(lakeName)  + 'Tin'
            tin = arcpy.CreateTin_3d(r'D:\2021年项目\0616WL\stuff\{}'.format(tinName),spatial_reference=spatial_ref,in_features=clipTerl)
            demName = pinyin.get_initial('{}'.format(lakeName)).replace(' ', '').capitalize()
            outDemPath = r'D:\2021年项目\0616WL\dem' + '\\' + demName.encode('utf-8')
            dem = arcpy.TinRaster_3d(tin,r'D:\2021年项目\0616WL\stuff\{}'.format(demName),sample_distance='CELLSIZE 2')
            arcpy.Clip_management(in_raster=dem,out_raster=outDemPath,
                                  in_template_dataset=buffBoua, nodata_value="-9999",
                                  clipping_geometry="ClippingGeometry", maintain_clipping_extent="NO_MAINTAIN_EXTENT")
            print '{} is done'.format(lakeName)
        except Exception as e:
            print '{} {}'.format(lakeName, e)


