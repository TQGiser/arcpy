import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import arcpy
import os
from arcpy.sa import *
os.chdir('d:/test')
arcpy.env.workspace = 'D:/TEST'
a = arcpy.ListRasters("","TIF")
for name in a:
    print(name.decode('utf-8','ignore'))