#coding=utf-8
import os
import math
import arcpy
import F
import pandas as pd
def calc_abc_from_line_2d(x0, y0, x1, y1):
    a = y0 - y1
    b = x1 - x0
    c = x0*y1 - x1*y0
    return a, b, c
def lineContainPoint(x,y,line):
    x1,y1,x2,y2 = line
    d = (y2 - y1) * x + (x1 - x2) * y + x2 * y1 - x1 * y2
    if d == 0:
        return x,y
def get_line_cross_point(line1, line2):
    # x1y1x2y2
    a0, b0, c0 = calc_abc_from_line_2d(*line1)
    a1, b1, c1 = calc_abc_from_line_2d(*line2)
    x1,y1,x2,y2 = line1
    x3,y3,x4,y4 = line2
    lineContainPoint(x1,y1,line2)
    lineContainPoint(x2,y2,line2)
    D = a0 * b1 - a1 * b0
    if D != 0:
        x = (b0 * c1 - b1 * c0) / D
        y = (a1 * c0 - a0 * c1) / D
        if x > min(x1,x2) and x < max(x1,x2) and x > min(x3,x4) and x <max(x3,x4) and y > min(y1,y2) and y < max(y1,y2) and y > min(y3,y4) and y <max(y3,y4):
        # print(x, y)
            return x, y

path = r'E:\test'
arcpy.env.wokspace = path
dmx = F.listFile(path,'断面'.decode('utf-8'),'x')
dmal = F.listFile(path,'管理范围线'.decode('utf-8'),'x')
line1s = F.polylineTolines(dmal)
line2s = F.polylineTolines(dmx)
cnList = []
for line2 in line2s:
    for line1 in line1s:
        if get_line_cross_point(line1,line2) is not None:
            cn = [get_line_cross_point(line1,line2)[0],get_line_cross_point(line1,line2)[1]]
            cnList.append(cn)
print cnList
# F.creatPoint(cnList,path,'aa')
