#coding=utf-8
import arcpy
path = r'D:\邱程\Test'
arcpy.env.workspace = path
shpM = r'D:\邱程\Test\甘孜州乡镇界-面.shp'
shpX = r'D:\邱程\Test\临水边界线.shp'

with arcpy.da.UpdateCursor(shpX,['SHAPE@','名称','乡镇']) as yb1:
    for row1 in yb1:
        List = []
        with arcpy.da.SearchCursor(shpM,['SHAPE@','XZQMC']) as yb2:
            for row2 in yb2:
                if row2[0].crosses(row1[0]):
                    List.append(row2[1])
        row1[2] = ','.join(List)
        yb1.updateRow(row1)
