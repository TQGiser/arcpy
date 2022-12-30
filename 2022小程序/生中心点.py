# coding=utf-8
import arcpy
import F

arcpy.env.overwriteOutput = True
path = r'E:\2022年项目\1230小程序\新建文件夹'
outPath = r'E:\2022年项目\1230小程序\新建文件夹'
dmaas = F.listFiles(path, '', 'm')
pList = []
for dmaa in dmaas:
    riverName = arcpy.Describe(dmaa).baseName.encode('utf-8').replace('管理范围面', '')
    dmaa4326 = arcpy.Project_management(dmaa, outPath + '\\' + '{}.shp'.format(riverName), '4326')
    with arcpy.da.SearchCursor(dmaa4326, ['SHAPE@','名称']) as yb:
        for row in yb:
            x = row[0].labelPoint.X,
            y = row[0].labelPoint.Y,
            print row[1], '%0.8f'%round(x[0],8),'%0.8f'%round(y[0],8)