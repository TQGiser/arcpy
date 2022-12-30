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
def listFile_Mdb(path,type):
    if type == 'd':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Point')
    elif type == 'x':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Polyline')
    elif type == 'm':
        walk = arcpy.da.Walk(path, topdown=True, datatype="FeatureClass", type='Polygon')
    for path, name, file in walk:
        for a in file:
            if a == 'DMAP':
                shp = os.path.join(path, a)
            elif a == 'DMAL':
                shp = os.path.join(path, a)
            elif a == 'DMAA':
                shp = os.path.join(path, a)
    return shp

def listFiles_Mdb(path,keyword,type):
    shps = []
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