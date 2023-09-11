#coding=utf-8
import arcpy
tl = r'E:\workData\20230825岸线规划\易日沟\DLG\2年线.shp'
def query_l_legnth(poline_file):
    """
    :param poline_file: 线shp文件
    :return:
    """
    cs = arcpy.da.SearchCursor(poline_file,'SHAPE@')
    ls = [row[0] for row in cs]
    for l in ls:
        print l.length,l.pointCount

def extract_by_part_emptyFields(shpFile,shpName,ext_path):
    """
    将包含多个要素的shp文件释放为单个的文件，没有属性字段
    :param shpFile: 总的shp文件
    :param shpName: 提取出的文件命名前辍like:XX村_001
    :param ext_path: 释放的地址
    :return:
    """
    cs = arcpy.da.SearchCursor(shpFile,'SHAPE@')
    pls = [row[0] for row in cs]
    i=1
    for pl in pls:
        aL = arcpy.CreateFeatureclass_management(ext_path, '{}{:03}.shp'.format(shpName,i), 'POLYGON')
        cs = arcpy.da.InsertCursor(aL, ['SHAPE@'])
        cs.insertRow([pl])
        i+=1

def extract_by_part_withFields(shpFile,ext_path):
    """
    将包含多个要素的shp文件释放为单个的文件,包含属性字段
    :param shpFile: 总的shp文件
    :param shpName: 提取出的文件命名前辍like:XX村_001
    :param ext_path: 释放的地址
    :return:
    """
    fileName = arcpy.Describe(shpFile).baseName.encode('utf-8')
    cs = arcpy.da.SearchCursor(shpFile,['*'])
    shpDatasList = [row for row in cs]
    i=1
    for data in shpDatasList:
        aL = arcpy.CreateFeatureclass_management(
            ext_path,
            '{}{:03}.shp'.format(fileName,i),
            template=shpFile)
        cs = arcpy.da.InsertCursor(aL, ['*'])
        cs.insertRow(data)
        i+=1