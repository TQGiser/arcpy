# coding=utf-8
import arcpy
dmal = r'E:\2022年项目\0420许曲断面线\许曲划界成果7.1.mdb\DLG\DMAL'
path = r'E:\2022年项目\0420许曲断面线'
cnList = []
with arcpy.da.SearchCursor(dmal,['SHAPE@X','SHAPE@Y','SHAPE@Z','NAME'],where_clause="RuleID = 8",explode_to_points=True) as yb:
    for row in yb:
        cn = [row[0],row[1],row[2],row[3]]
        cnList.append(cn)
p =r'E:\2022年项目\0420许曲断面线\DMD.shp'
yb = arcpy.da.InsertCursor(p,['SHAPE@X','SHAPE@Y','SHAPE@Z','DMH'])
for cn in cnList:
    yb.insertRow(cn)
del yb