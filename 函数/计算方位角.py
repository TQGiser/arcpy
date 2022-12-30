def calc_angle(x1,y1,x2,y2):
    angle=0
    dy= y2-y1
    dx= x2-x1
    if dx==0 and dy>0:
        angle = 0
    if dx==0 and dy<0:
        angle = 180
    if dy==0 and dx>0:
        angle = 90
    if dy==0 and dx<0:
        angle = 270
    if dx>0 and dy>0:
       angle = math.atan(dx/dy)*180/math.pi
    elif dx<0 and dy>0:
       angle = 360 + math.atan(dx/dy)*180/math.pi
    elif dx<0 and dy<0:
       angle = 180 + math.atan(dx/dy)*180/math.pi
    elif dx>0 and dy<0:
       angle = 180 + math.atan(dx/dy)*180/math.pi
    return angle