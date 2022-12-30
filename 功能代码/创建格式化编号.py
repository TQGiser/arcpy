# coding=utf-8
import arcpy
re = 0
def bh(x):
    global re
    a = 1
    b = 1
    if(re == 0):
        re = a
    else:
        re = re + b
    return re
step = 0
def bh():
    global step,code
    pStart = 1
    pInterval = 1
    if (step == 0):
        step = pStart
    else:
        step = step + pInterval
    code = '%02.0f'%step         #04为00001.....
    return code

def cl(bb):
    if bb == 2:
        return 910100
    elif bb == 27:
        return  910100
    elif bb == 4:
        return  910104

def cl(bb):
    if '左'.decode('utf-8') in bb:
        return 0
    if '右'.decode('utf-8') in bb:
        return 1

arcpy.CreateFeatureclass_management()
def cl(bb):
    if bb == 2:
        return '实体桩'
    elif bb == 27:
        return  '电子桩'
    elif bb == 4:
        return  '告示牌'
