import arcpy
import os
import sys
from arcpy.ia import *

os.chdir(r'E:\2021年项目\0205-125个湖泊\0329')
arcpy.env.workspace = r'E:\2021年项目\0205-125个湖泊\0329'
shp = r'E:\2021年项目\0205-125个湖泊\TK.shp'
path = r'E:\2021年项目\0205-125个湖泊\0329'
lack_name = '扎杰龙瓦'
raster = arcpy.Raster(r'E:\2021年项目\0205-125个湖泊\1.tif')
