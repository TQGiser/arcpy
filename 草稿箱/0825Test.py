#coding=utf-8
import arcpy
tl = r'E:\workData\20230825岸线规划\易日沟\DLG\2年线.shp'
def query_l_legnth(poline_file):
    cs = arcpy.da.SearchCursor(poline_file,'SHAPE@')
    ls = [row[0] for row in cs]
    for l in ls:
        print l.length,l.pointCount


import arcpy
arcpy.env.overwriteOutput = True
path = r'E:\test'

tp1 = r'E:\test\t1.shp'
tp2 = r'E:\test\t2.shp'

cs1 = arcpy.da.SearchCursor(tp1,'SHAPE@')
cs2 = arcpy.da.SearchCursor(tp2,'SHAPE@')

p1s = [row[0] for row in cs1]
p2s = [row[0] for row in cs2]

cps = []
for p1 in p1s:
    for p2 in p2s:
        cross_polygon = p1.intersect(p2,4)
        cps.append(cross_polygon)

aL = arcpy.CreateFeatureclass_management(path,'temp.shp','POLYGON')
cs = arcpy.da.InsertCursor(aL,['SHAPE@'])
for cp in cps:
    print cp
    cs.insertRow([cp])

# coding=utf-8
import arcpy
arcpy.env.overwriteOutput = True
path = r'E:\workData\20230908XXD\测试\84\rst'

tp1 = r'E:\workData\20230908XXD\测试\84\HB84.shp'
tp2 = r'E:\workData\20230908XXD\测试\84\土地利用84.shp'

cs1 = arcpy.da.SearchCursor(tp1,'SHAPE@')
cs2 = arcpy.da.SearchCursor(tp2,'SHAPE@')

p1s = [row[0] for row in cs1]
p2s = [row[0] for row in cs2]


i=0
for p1 in p1s:
    cps = []
    for p2 in p2s:
        cross_polygon = p1.intersect(p2,4)
        cps.append(cross_polygon)
    aL = arcpy.CreateFeatureclass_management(path,'土地利用%d'%(i), 'POLYGON')
    cs = arcpy.da.InsertCursor(aL, ['SHAPE@'])
    for cp in cps:
        print cp
        cs.insertRow([cp])
    i+=1


def extract_by_part(shpFile,shpName,ext_path):
    cs = arcpy.da.SearchCursor(shpFile,'SHAPE@')
    pls = [row[0] for row in cs]
    i=1
    for pl in pls:
        aL = arcpy.CreateFeatureclass_management(ext_path, '{}{:03}.shp'.format(shpName,i), 'POLYGON')
        cs = arcpy.da.InsertCursor(aL, ['SHAPE@'])
        cs.insertRow([pl])
        i+=1

