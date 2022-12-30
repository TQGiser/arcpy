# coding=utf-8
import arcpy
import F
arcpy.env.overwriteOutput = True
path = r'E:\2022年项目\0802理塘入库\xls'
d = F.listFile(path, '', 'd')
cnLst = []
arcpy.env.overwriteOutput = True
with arcpy.da.SearchCursor(d, ['SHAPE@X', 'SHAPE@Y', 'elev', 'dh', 'dmh']) as yb:
    for p in yb:
        cn = [p[0], p[1], p[2], p[3], p[4]]
        cnLst.append(cn)
dmh1Lst = [a[4] for a in cnLst]
dmhLst = list(set(dmh1Lst))
i = 0
lp = []
for i in range(0, len(dmhLst)):
    pg = []
    groupLst = []
    for cn in cnLst:
        if cn[4] == dmhLst[i]:
            groupLst.append(cn)

    for p in groupLst:
        xp = [p[0], p[1]]
        pg.append(xp)
    i += 1
    lp.append(arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in pg])))
arcpy.env.outputZFlag = 'Enabled'
Line = arcpy.CopyFeatures_management(lp, path + '\\' + 'dmx.shp')
arcpy.AddField_management(Line,'dmh','text')
print 'COPY OK'
with arcpy.da.UpdateCursor(Line, ['SHAPE@', 'SHAPE@X', 'SHAPE@Z','dmh'], explode_to_points=True) as yb:
    for row in yb:
        for cn in cnLst:
            if abs(row[1] - float(cn[0])) < 0.1:
                row[2] = round(float(cn[2]),2)
                row[3] = cn[4]
                print cn[3]
                yb.updateRow(row)