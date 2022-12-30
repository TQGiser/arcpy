#coding=utf-8
import arcpy
import math
import matplotlib.pylab as plt
path = r'D:\Test'
arcpy.env.workspace = path
infc = r'D:\Test\p1.shp'.decode('utf-8')
x_lst = []
y_lst = []
cn_lst = []
with arcpy.da.UpdateCursor(infc,['SHAPE@X','SHAPE@Y'],explode_to_points = True) as yb:
    for row in yb:
        x_lst.append(row[0])
        y_lst.append(row[1])
x1 = x_lst[0]
y1 = y_lst[0]
x2 = x_lst[1]
y2 = y_lst[1]
x3 = x_lst[2]
y3 = y_lst[2]
czx = ((x3-x1)*(x1-x2) + (y3-y1)*(y1 - y2))/((x1-x2)**2 + (y1-y2)**2)*(x1 - x2) + x1
czy = ((x3-x1)*(x1-x2) + (y3-y1)*(y1 - y2))/((x1-x2)**2 + (y1-y2)**2)*(y1 - y2) + y1
print x1,y1
print x2,y2
print x3,y3
print czx,czy
# czx = (((x3-x1)*(x1-x2) + (y3-y1)*(y1 - y2))*(x1 - x2)*(y1 - y2))(x1-x2) + x1
# czy = (((x3-x1)*(x1-x2) + (y3-y1)*(y1 - y2))*(x1 - x2)*(y1 - y2))(y1 - y2) + y1

