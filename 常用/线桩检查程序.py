# coding=utf-8
import arcpy
import os
import math
import F
path = r'E:\2021年项目\1101苦西绒沟\OK'
dmapShp = F.listFile(path, '线桩'.decode('utf-8'), 'd')
# dmxShp = F.listFile(path, '断面'.decode('utf-8'), 'x')
# dmalShp = F.listFile(path, '管理范围线'.decode('utf-8'), 'x')
for row in arcpy.da.SearchCursor(dmapShp,['NAME','Lc']):
    print row[0],row.next