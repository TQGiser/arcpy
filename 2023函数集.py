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
def creatPointShpFile_by_xlsx(xlFile,fileSavePath):
    """
    根据xlsx文件（包含x,y,name三列）创建点shape文件
    :param xlFile: xlsx文件
    :param fileSavePath: shape文件存储地址
    :return:
    """
    import pandas as pd
    arcpy.env.overwriteOutput = True
    df = pd.read_excel(xlFile.decode('utf-8'))
    p_cn = []
    for name, value in df.iterrows():
        cn = [df.loc[name, 'x'], df.loc[name, 'y'], df.loc[name, 'name']]
        p_cn.append(cn)
    p = arcpy.CreateFeatureclass_management(fileSavePath, 'newPoint', 'POINT')
    arcpy.AddField_management(p, 'name', 'TEXT')
    yb = arcpy.da.InsertCursor(p, ['SHAPE@X', 'SHAPE@Y', 'name'])
    for cn in p_cn:
        yb.insertRow(cn)
    del yb
def extract_FromMDBs(mdbsPath,featureName):
    """
    根据分幅MDB提取各层要素
    :param mdbsPath: mdb文件夹（单层，只有mdb文件）
    :param featureName: 要素名称（'TERL','HYDA')等
    :return:
    """
    arcpy.env.workspace = mdbsPath
    arcpy.env.overwriteOutput = True
    mdbs = arcpy.ListFiles('*.mdb')
    arcpy.CreateFolder_management(mdbsPath, 'single')
    arcpy.CreateFolder_management(mdbsPath, 'merge')
    shps = []
    for mdb in mdbs:
        print mdb
        shp = mdbsPath.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + featureName
        tempshpname = arcpy.Describe(mdb).name.replace('-','').replace('.mdb','') + arcpy.Describe(shp).name + '.shp'
        shp2 = arcpy.FeatureClassToFeatureClass_conversion(shp,mdbsPath + '\\' + 'single',tempshpname)
        shps.append(shp2)
    arcpy.Merge_management(shps,mdbsPath + '\\' + 'merge' + '\\' + '{}.shp'.format((featureName)))