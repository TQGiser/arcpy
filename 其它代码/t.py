#arcpy.SetRasterProperties_management(rasters,nodata= [[1,254],[2,254],[3,254]])            #设置栅格nodata值
# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "朗村隆巴沟8bit.tif"
arcpy.SetRasterProperties_management(in_raster="朗村隆巴沟8bit.tif", data_type="", statistics="", stats_file="", nodata="1 255;2 255;3 255", key_properties="")

# rasters = []
# for i,v,m in os.walk(path):
#     for rasname in m:                                                                                                    ################################
#         if rasname.endswith('.tif'):
#             rasters.append(rasname)                                                                                                 #复制出8bit栅格,会漏像元！！！！！！！！！！
# for name in rasters:
#     tif_transto_8bit = name.strip('.tif') + '8bit' + '.tif'
#     arcpy.CopyRaster_management(name,tif_transto_8bit,nodata_value= '254',pixel_type= '8_BIT_UNSIGNED',format='TIFF')    #################################
arcpy.gp.RasterCalculator_sa('Con(IsNull("朗村隆巴沟"),254,("朗村隆巴沟"))', "C:/Users/Administrator/Documents/ArcGIS/Default.gdb/rastercalc1")