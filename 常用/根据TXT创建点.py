#coding=utf-8
import arcpy
import os
import F

F.createPointFromTxt(r'E:\2022年项目\0511康定断面\康定外业成果\外业成果\石\（康定市布恰巴沟断面成果）\布恰巴沟断面采集散点数据.txt'.decode('utf-8'),r'E:\2022年项目\0511康定断面','dmd')