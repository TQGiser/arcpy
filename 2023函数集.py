#coding=utf-8
import arcpy
tl = r'E:\workData\20230825岸线规划\易日沟\DLG\2年线.shp'
def query_l_legnth(poline_file):
    cs = arcpy.da.SearchCursor(poline_file,'SHAPE@')
    ls = [row[0] for row in cs]
    for l in ls:
        print l.length,l.pointCount

def extract_by_part(shpFile,shpName,ext_path):
    cs = arcpy.da.SearchCursor(shpFile,'SHAPE@')
    pls = [row[0] for row in cs]
    i=1
    for pl in pls:
        aL = arcpy.CreateFeatureclass_management(ext_path, '{}{:03}.shp'.format(shpName,i), 'POLYGON')
        cs = arcpy.da.InsertCursor(aL, ['SHAPE@'])
        cs.insertRow([pl])
        i+=1