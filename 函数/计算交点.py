import math
def cal_xy_s(x1,y1,x2,y2,s2):
    s1 =  math.sqrt(pow((x1-x2),2) + pow((y1-y2),2))
    x3 = (s1*x2 + s2*x2 - s2*x1)/s1
    y3 = (s1*y2 + s2*y2 - s2*y1)/s1
    return x3,y3
import arcpy
arcpy.Polyline(arcpy.Array([arcpy.Point(1,1),arcpy.Point(2,2)]))
def calc_abc_from_line_2d(x0, y0, x1, y1):
    a = y0 - y1
    b = x1 - x0
    c = x0*y1 - x1*y0
    return a, b, c
def get_line_cross_point(line1, line2):
    # x1y1x2y2
    a0, b0, c0 = calc_abc_from_line_2d(*line1)
    a1, b1, c1 = calc_abc_from_line_2d(*line2)
    D = a0 * b1 - a1 * b0
    if D == 0:
        return None
    x = (b0 * c1 - b1 * c0) / D
    y = (a1 * c0 - a0 * c1) / D
    # print(x, y)
    return x, y
def creatLine(xList):
    i = 0
    line = []
    for i in range(0,len(xList)-1):
        x1 = xList[i][0]
        y1 = xList[i][1]
        x2 = xList[i+1][0]
        y2 = xList[i+1][1]
        l = [x1,y1,x2,y2]
        line.append(l)
        i += 1
    return line
