#coding=utf-8
import arcpy
import F
import os

path = r'E:\2023年项目\0506二院数据\EY'
path2 = r'E:\2023年项目\0506二院数据\CS'
path3 = r'E:\2023年项目\0506二院数据\甘孜州州管'

dmalsEY = F.listFiles(path,'','x')
dmalsLake =  F.listFiles(path3,'143个湖泊'.decode('utf-8'),'x')
dmalCS = F.listFile(path2,'','x')

def fr(dmal,xzq,riverName):
    with arcpy.da.SearchCursor(dmal,['SHAPE@','名称','XZQ']) as yb:
        for row in yb:
            if(row[1].encode('utf-8') == riverName and row[2].encode('utf-8') ==xzq):
                return  row[0]
# 县级河流
for dmal in dmalsEY:
    xzq = dmal.split('\\')[4].encode('utf-8')
    print xzq
    with arcpy.da.UpdateCursor(dmal,['SHAPE@','RIVER']) as yb:
        for row in yb:

            shape = fr(dmalCS,xzq,"%s" % row[1].encode('utf-8'))
            if(shape != None):
                print row[1]
                row[0] = shape;
                yb.updateRow(row)
            # else:
            #     yb.deleteRow()


#
# def fl(dmal,lakeName):
#     with arcpy.da.SearchCursor(dmal,['SHAPE@','名称']) as yb:
#         for row in yb:
#             if(row[1].encode('utf-8') == lakeName):
#                 return  row[0]
#
#
# # 143lake
# for dmal in dmalsLake:
#     xzq = dmal.split('\\')[4].encode('utf-8')
#     with arcpy.da.UpdateCursor(dmal,['SHAPE@','RIVER']) as yb:
#         for row in yb:
#             shape = fl(dmalCS,"%s" % row[1].encode('utf-8'))
#             if(shape != None):
#                 row[0] = shape;
#                 yb.updateRow(row)
#             else:
#                 print row[1]
#                 yb.deleteRow()

# with arcpy.da.UpdateCursor(dmalsEY,['SHAPE@','RIVER']) as yb:
#     for row in yb:
#         shape = fr(dmalCS, "%s" % row[1].encode('utf-8'))
#         if(shape != None):
#             row[0] = shape;
#             yb.updateRow(row)
#         else:
#             yb.deleteRow()
#
#         # print row[1]sik
#
#         # shape = fr(dmalCS,"%s"%row[1].encode('utf-8'))
#         # row[0] = shape;
#         # yb.updateRow(row)
#
#         # if(shape != None):
#         #     print row[1]
#         #     row[0] = shape;
#         #     yb.updateRow(row)
