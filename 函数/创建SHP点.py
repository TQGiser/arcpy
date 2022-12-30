def creatPoint(p_cn,path,shpName):
    point = arcpy.Point()
    pointList = []
    for p in p_cn:
        point.X = p[0]
        point.Y = p[1]
        pg = arcpy.PointGeometry(point)
        pointList.append(pg)
        arcpy.CopyFeatures_management(pointList,path + '\\' + '{}.shp'.format(shpName))