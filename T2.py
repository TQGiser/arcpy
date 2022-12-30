
import arcpy
dmal = '拉曲管理范围线'
glq = '拉曲功能区'
with arcpy.da.SearchCursor(glq,"SHAPE@") as yb1:
    for row1 in yb1:
        with arcpy.da.SearchCursor(dmal,"SHAPE@") as yb2:
            for row2 in yb2:
                print row1[0].intersect(row2[0],2)
                
with arcpy.da.SearchCursor(glq,"SHAPE@") as yb1:
    for row1 in yb1:
        with arcpy.da.SearchCursor(dmal,"SHAPE@") as yb2:
            for row2 in yb2:
                tl = row1[0].intersect(row2[0],2)
                print tl.length
                
with arcpy.da.SearchCursor(glq,"SHAPE@") as yb1:
    for row1 in yb1:
        with arcpy.da.SearchCursor(dmal,"SHAPE@") as yb2:
            for row2 in yb2:
                tl = row1[0].intersect(row2[0],2)
                print tl.length
                

with arcpy.da.SearchCursor(glq,"SHAPE@") as yb1:
    for row1 in yb1:
        with arcpy.da.SearchCursor(dmal,"SHAPE@") as yb2:
            if not row2[0].disjoint(row1[0]):
                tl = row1[0].intersect(row2[0],2)
                print tl.length
                
with arcpy.da.SearchCursor(glq,"SHAPE@") as yb1:
    for row1 in yb1:
        with arcpy.da.SearchCursor(dmal,"SHAPE@") as yb2:
            if not row2[0].disjoint(row1[0]):
                tl = row1[0].intersect(row2[0],2)
                print tl.firstPoint.X,tl.firstPoint.Y
                
with arcpy.da.SearchCursor(glq,"SHAPE@") as yb1:
    for row1 in yb1:
        with arcpy.da.SearchCursor(dmal,"SHAPE@") as yb2:
            for row2 in yb2:
                if not row2[0].disjoint(row1[0]):
                    tl = row1[0].intersect(row2[0],2)
                    print tl.firstPoint.X,tl.firstPoint.Y


