# coding=utf-8
import arcpy
import pinyin
import os
path = r'D:\2021年项目\0616WL'.decode('utf-8')
arcpy.env.workspace = path
outpath = r'D:\2021年项目\0616WL\OK'.decode('utf-8')
tk = 'TKZS-99.shp'
spatial_ref = arcpy.Describe(tk).spatialReference
with arcpy.da.SearchCursor('TKZS-99.shp',['SHAPE@','图名'.decode('utf=8'),'图号'.decode('utf-8')]) as yb:
    for row in yb:
        try:
            lakeName = row[1].encode('utf-8')
            tk = row[2].encode('utf-8')
            demName = pinyin.get_initial('{}'.format(lakeName)).replace(' ', '').capitalize()
            b = str(lakeName).split('段')[0]
            xName = b.decode('utf-8')[-3:].encode('utf-8')
            x_folder = outpath.encode('utf-8') + '\\' + xName
            arcpy.CreateFolder_management(outpath, xName)
            arcpy.CreateFolder_management(x_folder, lakeName)
            demFolder = x_folder + '\\' + lakeName
            arcpy.CreateFolder_management(demFolder, 'DEM')
            dem2Folder = demFolder + '\\' + 'DEM'.encode('utf-8')
            tkFolder = str(lakeName) + str(tk)
            arcpy.CreateFolder_management(dem2Folder, tkFolder)
            dem = r'D:\2021年项目\0616WL\dem\{}'.format(demName)
            demByTk_dir = dem2Folder + '\\' +tkFolder + '\\' + demName.encode('utf-8') + tk
            tkdem = arcpy.Clip_management(in_raster=dem,out_raster=demByTk_dir,in_template_dataset=row[0], nodata_value="-9999",
                                  clipping_geometry="ClippingGeometry", maintain_clipping_extent="MAINTAIN_EXTENT")
            renameFolder = (dem2Folder + '\\' + tkFolder).decode('utf-8')
            os.chdir(renameFolder)                                                                                      #将dem小写转为大写开头
            ys = '{}'.format(demName + tk)
            new = '{}'.format(demName.capitalize() + tk)
            os.rename(ys,new)
            arcpy.DefineProjection_management(tkdem,spatial_ref)                                                        #dem改名后需重定义投影
            print '{} is done'.format(lakeName + tk + new)
        except Exception as e:
            print '{} {}'.format(demName,e)
