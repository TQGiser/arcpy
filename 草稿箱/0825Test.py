#coding=utf-8
import arcpy
tr = r'E:\test\0824拓扑问题\tr.shp'
tl1 = r'E:\test\0824拓扑问题\tl1.shp'
tl2 = r'E:\test\0824拓扑问题\tl2.shp'

cs1 = [row[0] for row in arcpy.da.SearchCursor(tr,'SHAPE@')]
cs2 = [row[0] for row in arcpy.da.SearchCursor(tl1,'SHAPE@')]
cs3 = [row[0] for row in arcpy.da.SearchCursor(tl2,'SHAPE@')]

if cs1[0].within(cs2[0]):
    print 2;

if cs1[0].contains(cs3[0]):
    print 3;

if cs1[0].touches(cs2[0]):
    print 4;

if cs1[0].touches(cs3[0]):
    print 5;