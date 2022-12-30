#coding=utf-8
import arcpy
import os
path = "D:/2021年项目/0317雅江北桩确认".decode('utf-8')
mxdpath = "D:/2021年项目/0317雅江北桩确认/断面位置图.mxd".decode('utf-8')
os.chdir(path)
arcpy.env.workspace = path
mxd = arcpy.mapping.MapDocument(mxdpath)
shppath = '断面图框.shp'
pageWide = mxd.pageSize.width
pageHeight = mxd.pageSize.height
tl = arcpy.mapping.ListLayoutElements(mxd,'','图例')[0]
znz = arcpy.mapping.ListLayoutElements(mxd,'','North Arrow')[0]
dmx = arcpy.mapping.ListLayoutElements(mxd,'','dmx')[0]
sjk = arcpy.mapping.ListLayoutElements(mxd,'','图层')[0]
sjkWidth = sjk.elementWidth
x2 = sjk.elementPositionX
x = tl.elementPositionX
y = tl.elementPositionY
h = tl.elementHeight
w = tl.elementWidth
x1 = znz.elementPositionX
y1 = znz.elementPositionY
h1 = znz.elementHeight
w1 = znz.elementWidth
jx2 = x - x2
tl_l = [x,y]
tl_r = [float(sjkWidth) + x2 - w - jx2,y]
znz_l = [x1,y1]
znz_r = [float(sjkWidth) + x2 - w1 - jx2,y1]
print(pageWide,sjkWidth,x2)
for pagenum in range(1,mxd.dataDrivenPages.pageCount + 1):
    mxd.dataDrivenPages.currentPageID = pagenum
    cursor = arcpy.SearchCursor(shppath)
    for i in cursor:
        if i.FID == pagenum-1:# and i.dmx == 'LCLBG-001':
            name = i.NAME2
            filename = name.encode('utf-8')
            if i.tl=='1':
                tl_X = tl_l[0]
                tl_Y = tl_l[1]
            elif i.tl=='2':
                tl_X = tl_r[0]
                tl_Y = tl_r[1]
            if i.znz == '1':
                znz_X = znz_l[0]
                znz_Y = znz_l[1]
                print(znz_X,znz_Y)
            elif i.znz == '2':
                znz_X = znz_r[0]
                znz_Y = znz_r[1]
                print(znz_X,znz_Y)
            dmx.text = i.dmx
            tl.elementPositionX = tl_X
            tl.elementPositionY = tl_Y
            znz.elementPositionX = znz_X
            znz.elementPositionY = znz_Y
            mxd.save
            arcpy.mapping.ExportToJPEG(mxd,r'D:\2021年项目\0720雅江图册\断面位置图' + '\\' + filename + ".jpg",resolution = 800)