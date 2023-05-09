# coding=utf-8
import arcpy
import pandas as pd
import F

path = r'E:\2023年项目\0506二院数据\OK'

dmals = F.listFiles(path, '', 'x')


def frn(dmal):
    riverList = []
    with arcpy.da.SearchCursor(dmal, ['SHAPE@', 'RIVER']) as yb:
        for row in yb:
            if (row[1] not in riverList):
                riverList.append(row[1])
            else:
                print dmal,row[1]



for dmal in dmals:
    frn(dmal)