#coding=utf-8
import arcpy
import F
dem = r'E:\数据\甘孜藏族自治州12.5米DEM\甘孜藏族自治州.tif'
path = r'D:\CesiumData\3DPLTest\xshzx3Dall.shp'
arcpy.env.workspace = path
sp2d = F.listFile(path,'all','x')
i=0
with open(r"e:\name.txt",'w') as f:
    with arcpy.da.UpdateCursor(sp2d,['SHAPE@','SHAPE@Z'],explode_to_points=True) as yb:
        for row in yb:
            E = row[0].centroid.X
            N = row[0].centroid.Y
            D = int(arcpy.GetCellValue_management(in_raster=dem, location_point='{} {}'.format(E, N)).getOutput(0)) + 5
            f.write(str(i))
            f.write(",")
            f.write(str(E))
            f.write(",")
            f.write(str(N))
            f.write(",")
            f.write(str(D))
            f.write(",")
            print E, N, D,i,
            # row[1]= D
            # yb.updateRow(row)
            i+=10
            # break
