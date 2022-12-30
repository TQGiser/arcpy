#coding=utf-8
import arcpy
import pythonaddins
import os

class ButtonClass1(object):
    """Implementation for DOM_P_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        path = pythonaddins.OpenDialog('选择DOM目录'.decode('utf-8'))
        arcpy.env.overwriteOutput = True
        arcpy.env.workspace = path

        tifs = []
        for i, v, m in os.walk(path.decode('utf-8'), topdown=True):
            for a in m:
                if '.tif' in a:
                    tif = os.path.join(i, a)
                    tifs.append(tif)
        for tif in tifs:
            print tif
            c_tif = 'fixed' + arcpy.Describe(tif).name.encode('utf-8')
            c_tif_path = arcpy.Describe(tif).path.encode('utf-8')
            # arcpy.env.cellSize = 0.2
            arcpy.env.cellSize = 0.2
            arcpy.env.nodata = 'MAP_DOWN'
            arcpy.env.compression = 'NONE'
            arcpy.CopyRaster_management(tif, c_tif_path + '\\' + c_tif,
                                        config_keyword="",
                                        background_value="0",
                                        nodata_value="255",
                                        onebit_to_eightbit="NONE",
                                        colormap_to_RGB="NONE",
                                        pixel_type="8_BIT_UNSIGNED",
                                        scale_pixel_value="NONE",
                                        RGB_to_Colormap="NONE",
                                        format="TIFF", transform="NONE")
