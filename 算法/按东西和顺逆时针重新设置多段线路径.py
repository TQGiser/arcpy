#coding=utf-8
import arcpy
import math
import matplotlib.pylab as plt
path = r'D:\Test'
arcpy.env.workspace = path
infc = r'D:\Test\l1.shp'.decode('utf-8')
x_lst = []
y_lst = []
cn_lst = []
with arcpy.da.UpdateCursor(infc,['OID@','SHAPE@X','SHAPE@Y','SHAPE@M'],explode_to_points = True) as yb:
    for row in yb:
        x_lst.append(row[1])
        y_lst.append(row[2])
for i in range(0,len(x_lst)):
    cn = [x_lst[i],y_lst[i],i]
    cn_lst.append(cn)
x = [cn_lst[i][0]  for i in range(0,len(cn_lst))]
y = [cn_lst[i][1]  for i in range(0,len(cn_lst))]
new_cn_lst = []
def pxfx(sn,ne):
    if ne == 'x':
        qd = min(cn_lst, key=lambda s: s[0])[2]
    elif ne == 'd':
        qd = max(cn_lst, key=lambda s: s[0])[2]
    if sn == 's':
        for new_cn in cn_lst:
            if new_cn[2] < qd:
                num = len(cn_lst) - qd + new_cn[2]
            elif new_cn[2] == qd:
                num = 0
            elif new_cn[2] > qd:
                num = new_cn[2] - qd
            cn = [new_cn[0], new_cn[1], num]
            new_cn_lst.append(cn)
    elif sn == 'n':
        for new_cn in cn_lst:
            if new_cn[2] < qd:
                num = qd - new_cn[2]
            elif new_cn[2] == qd:
                num = 0
            elif new_cn[2] > qd:
                num = len(cn_lst) + qd - new_cn[2]
            cn = [new_cn[0], new_cn[1], num]
            new_cn_lst.append(cn)

    return  new_cn_lst

new_cn_lst_sorted = sorted(pxfx('n','d'),key=lambda  s:s[2])
x1 = [new_cn_lst_sorted[i][0] for i in range(0,len(new_cn_lst_sorted))]
y1 = [new_cn_lst_sorted[i][1] for i in range(0,len(new_cn_lst_sorted))]
endPoint = [x1[0],y1[0],len(new_cn_lst_sorted)+1]
new_cn_lst_sorted.append(endPoint)
M = []
m = 0
for i in range(0,len(new_cn_lst_sorted)-1):
    a = math.sqrt((new_cn_lst_sorted[i][0]-new_cn_lst_sorted[i+1][0])**2 + (new_cn_lst_sorted[i][1]-new_cn_lst_sorted[i+1][1])**2)
    m1 = m + math.sqrt((new_cn_lst_sorted[i][0]-new_cn_lst_sorted[i+1][0])**2 + (new_cn_lst_sorted[i][1]-new_cn_lst_sorted[i+1][1])**2)
    m = m1
    M.append(m1)
array = arcpy.Array()

for coord in new_cn_lst_sorted:
    array.add(arcpy.Point(coord[0], coord[1]))
polyline = arcpy.Polyline(array)
arcpy.env.outputMFlag = 'Enabled'
polyline_M = arcpy.CopyFeatures_management(polyline, "D:/Test/nd.shp")
with arcpy.da.UpdateCursor(polyline_M,'SHAPE@M',explode_to_points = True) as yb:
    i = 0
    for row in yb:
        row[0] = M[i]
        i += 1
        yb.updateRow(row)

# plt.plot(x2,y2,'g-')
# plt.show()