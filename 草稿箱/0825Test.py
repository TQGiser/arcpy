#coding=utf-8
import arcpy
tl = r'E:\workData\20230825岸线规划\茨巫沟\DLG\5年线.shp'
def query_l_legnth(poline_file):
    cs = arcpy.da.SearchCursor(poline_file,'SHAPE@')
    ls = [row[0] for row in cs]
    for l in ls:
        print l.length,l.pointCount