import arcpy

arcpy.CheckOutExtension("spatial")

arcpy.gp.overwriteOutput=1

arcpy.env.workspace = "D:\\shuju"

rasters = arcpy.ListRasters("*", "tif")

mask= "D:\\shiyan_ls\\bj.shp"

for raster in rasters:

    print(raster)

    out= "D:\\shuchu\\"+"clip_"+raster

    arcpy.gp.ExtractByMask_sa(raster, mask, out)

    print("clip_"+raster+"  has done")

print("All done")