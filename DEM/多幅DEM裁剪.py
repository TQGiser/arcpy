# coding=utf-8
import arcpy
import os
import pinyin
path = r'E:\2021年项目\1124DEM'
arcpy.env.overwriteOutput = True
arcpy.env.workspace = path
try:
    arcpy.CreateFolder_management(path,'stuff')
    arcpy.CreateFolder_management(path,'f2')
    arcpy.CreateFolder_management(path,'ok')
    arcpy.CreateFolder_management(path,'temp')
except:
    pass
path2 = path + '\\' + 'stuff'
path3 = path + '\\' + 'f2'
path4 = path + '\\' + 'ok'
path5  = path + '\\' + 'temp'
def listdems(path,type):
    dems = []
    if type == 'TIF':
        walk = arcpy.da.Walk(path, topdown=True, datatype="RasterDataset", type='TIF')
    elif type == 'GRID':
        walk = arcpy.da.Walk(path, topdown=True, datatype="RasterDataset", type='GRID')
    elif type == 'IMG':
        walk = arcpy.da.Walk(path, topdown=True, datatype="RasterDataset", type='IMG')
    for path, name, file in walk:
        for a in file:
            dem = os.path.join(path, a)
            dems.append(dem)
    return  dems
def listFiles(path, keyword, type):
    shps = []
    arcpy.env.workspace = path
    if type == 'd':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Point')
    elif type == 'x':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Polyline')
    elif type == 'm':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Polygon')
    for path, name, file in walk:
        for a in file:
            if keyword in a:
                shp = os.path.join(path, a)
                shps.append(shp)
    return shps
dems = listdems(path,'IMG')
tks = listFiles(path,'','m')
a = arcpy.ListRasters('*')
for dem in dems:
    print dem
    with arcpy.da.SearchCursor(tks[0],['SHAPE@','图名'])as yb:
        for row in yb:
            a = row[1].encode('utf-8')
            if a.split('理塘县段-')[0] in dem.encode('utf-8'):
                arcpy.CreateFolder_management(path2, a)
                arcpy.CreateFolder_management(path3, a)
                arcpy.CreateFolder_management(path4, a)
                demName = pinyin.get_initial('{}'.format(a)).replace(' ', '').capitalize().split('-')[1]
                print demName
                demFolderName = pinyin.get_initial('{}'.format(a)).replace(' ', '')
                demByTk = path2.decode('utf-8') + '\\' + a.decode('utf-8') + '\\' + demName.decode('utf-8')
                shpName = a.replace('-', '')
                tk = arcpy.GraphicBuffer_analysis(row[0], path2.decode('utf-8') + '\\' + shpName.decode('utf-8'), 5)
                ysdem = arcpy.Clip_management(in_raster=dem, out_raster=demByTk, in_template_dataset=tk,
                                              nodata_value="-9999",
                                              clipping_geometry="ClippingGeometry",
                                              maintain_clipping_extent="MAINTAIN_EXTENT")
                okdem = path3.decode('utf-8') + '\\' + a.decode('utf-8') + '\\' + demName.decode(
                    'utf-8')
                arcpy.Resample_management(ysdem, okdem, '5')                                                         #######重采样像元大小##############
                arcpy.env.workspace = path5
                dem_nodata = arcpy.gp.IsNull_sa(okdem)
                dem999 = path4.decode('utf-8') + '\\' + a.decode('utf-8') + '\\' + demName.decode('utf-8')
                arcpy.gp.Con_sa(dem_nodata, -9999, dem999, okdem, "value = 1")
                renameFolder =path4.decode('utf-8') + '\\' + a.decode('utf-8')
                os.chdir(renameFolder)
                ys = '{}'.format(demName.decode('utf-8') )
                new = '{}'.format(demName.decode('utf-8').upper())
                os.rename(ys, new)
