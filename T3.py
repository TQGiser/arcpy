# coding=utf-8
import arcpy
path = r'E:\2022年项目\0923拉曲岸线规划\test'
arcpy.env.workspace = path
arcpy.env.overwriteOutput=True
glq = r'E:\2022年项目\0923拉曲岸线规划\test\拉曲功能区.shp'
dmal = r'E:\2022年项目\0923拉曲岸线规划\test\拉曲管理范围线.shp'
lineList = []
with arcpy.da.SearchCursor(glq,["SHAPE@",'BH']) as yb1:
    for row1 in yb1:
        with arcpy.da.SearchCursor(dmal,"SHAPE@") as yb2:
            for row2 in yb2:
                if not row2[0].disjoint(row1[0]):
                    tl = row1[0].intersect(row2[0],2)
                    if tl.partCount > 1:
                        print row1[1],tl.partCount
#                     cn = [tl,row1[1]]
#                     lineList.append(cn)
# L =  arcpy.CreateFeatureclass_management(path,'checkLine.shp','POLYLINE')
# arcpy.AddField_management(L,'BH','TEXT')
# cs = arcpy.da.InsertCursor(L,['SHAPE@','BH'])
# for line in lineList:
#     # print line[0],line[1]
#     cs.insertRow([line[0],line[1]])
