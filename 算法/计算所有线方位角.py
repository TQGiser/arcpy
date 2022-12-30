# coding=utf-8
import math
import numpy as np
import matplotlib.pylab as plt

p1 = [1.0, -1.0]
p2 = [2.0, 2.0]
p3 = [-1.0, 1.0]
p4 = [-2.0, -2.0]
cn_lst = [[1.0, -1.0], [2.0, 2.0], [-1.0, 1.0], [-2.0, -2.0]]
for i in range(0, len(cn_lst)):
    for j in range(0, len(cn_lst)):
        a = float(cn_lst[j][0]) - float(cn_lst[i][0])
        b = float(cn_lst[j][1]) - float(cn_lst[i][1])
        if not a == 0.0:
            if a > 0 and b > 0:
                angle = 180 * math.atan(abs(a) / abs(b)) / math.pi
            if a > 0 and b < 0:
                angle = 180 * math.atan(abs(a) / abs(b)) / math.pi + 90
            if a < 0 and b > 0:
                angle = 180 * math.atan(abs(a) / abs(b)) / math.pi +270
            if a < 0 and b < 0:
                angle = 180 * math.atan(abs(a) / abs(b)) / math.pi + 180
            print a, b, 'line{}->{} angle is :'.format(i, j), ' ', angle

        # print i,j,a,b

# print len(cn)
# def fwj(cn_lst):
#     for i in range(0,len(cn_lst) + 1):
#         if cn
# p12 = math.atan(abs(p2[0] - p1[0])/abs(p2[1] - p1[1]))
# print 180*p12/math.pi
# p23 = math.atan(abs(p3[0] - p2[0])/abs(p3[1] - p2[1]))
# print 180*p23/math.pi + 180
# p34 = math.atan(abs(p4[0] - p3[0])/abs(p4[1] - p3[1]))
# print 180*p34/math.pi + 180
# p41 = math.atan(abs(p1[0] - p4[0])/abs(p1[1] - p4[1]))
# print 180*p41/math.pi
# p24 = math.atan(abs(p4[0] - p2[0])/abs(p4[1] - p2[1]))
# print 180*p24/math.pi
# p42 = math.atan(abs(p2[0] - p4[0])/abs(p2[1] - p4[1]))
# print 180*p42/math.pi + 180
# p13 = math.atan(abs(p3[0] - p1[0])/abs(p3[1] - p1[1]))
# print 180*p13/math.pi + 270
# p31 = math.atan(abs(p1[0] - p3[0])/abs(p1[1] - p3[1]))
# print 180*p31/math.pi + 90
