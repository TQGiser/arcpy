#coding=utf-8
import arcpy
path = r'D:\2021年项目\0625点线矛盾'.decode('utf-8')
arcpy.env.workspace = path
infc = r'D:\2021年项目\0625点线矛盾\RQDM.shp'.decode('utf-8')
with arcpy.da.SearchCursor(infc,['FID','SHAPE@']) as yb:
    for row in yb:
        for part in row[1]:
            for pnt in part:
                print pnt.Z