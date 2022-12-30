# coding=utf-8
'''re = 0
def bh()
    global re
    a = 1
    b = 1
    if(re == 0):
        re = a
    else:
        re = re + b
    return re'''
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
# 根据值范围计算角度
def cal(d1,d2):
  ang=d2+180-d1
  if(ang<0):
    ang=-ang
  elif(ang>180 and ang<360):
    ang=360-ang
  elif(ang>360 or ang == 360):
    ang =ang-360
  return ang

def Reclass(WellYield):
    if (WellYield == 8):
        return "1W段注记"
    elif (WellYield == 1.6):
        return "2K段注记"

def cl(bb):
    if bb == u"1：10000段":
       return "1W段注记"
    if bb == u"1:2000段":
       return "2K段注记"

def cl(a):
    if a>0 and a<90:
        return a
    if a>90 and a<180:
        b = a - 90
        return b
    if a>180 and a<270:
        b = a-180
        return b
    if a>270 and a<360:
        b = a-270
        return b
    # 

def cl(a,b):
    if a == 'L':
        return b
    if a == 'R':
        c = b -18

