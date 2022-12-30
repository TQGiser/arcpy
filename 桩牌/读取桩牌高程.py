#coding=utf-8
import arcpy
import os
import shutil
path = r'E:\2021年项目\1202理塘2K划界\勇杰几玛\shape'
try:
    arcpy.CreateFolder_management(path,'stuff')
except:
    pass
stuffDir = path + '\\' + 'stuff'
arcpy.env.workspace = path
def listFile(path, keyword, type):
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
    return shp
dmap = listFile(path,'线桩'.decode('utf-8'),'d')
terl = listFile(path,'terl','x')
spatial_ref = arcpy.Describe(terl).spatialReference
try:
    arcpy.AddField_management(dmap,'H2','TEXT')
except:
    pass
with arcpy.da.UpdateCursor(dmap,['SHAPE@','NAME','SHAPE@X','SHAPE@Y','H2','FID']) as yb:
    for row in yb:
        try:
            pName = (row[1][-5:].encode('utf-8')).replace('-','')
            clipShp = stuffDir + '\\' + pName + 'cliped.shp'
            arcpy.GraphicBuffer_analysis(row[0],clipShp, "200 Meters")
            clipTerl = stuffDir + '\\' + pName + 'clipTerl.shp'
            arcpy.Clip_analysis(terl,clipShp,clipTerl)
            if '左' in pName:
                ras = stuffDir + '\\' + 'L' + pName.replace('左', '')
            if '右' in pName:
                ras = stuffDir + '\\' + 'R' + pName.replace('右', '')
            arcpy.TopoToRaster_3d(clipTerl,ras,cell_size="1",extent=clipShp)
            elev = str(arcpy.GetCellValue_management(in_raster=ras,location_point='{} {}'.format(row[2],row[3])))
            row[4] = '%.2f'%(round(float(elev),2))
            yb.updateRow(row)

            print '{} is done'.format(pName)
        except Exception as e:
            print '{} has problem with {}'.format(pName,e)
shutil.rmtree(path.decode('utf-8') + '\\' + 'stuff')