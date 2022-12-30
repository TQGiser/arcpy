#coding=utf-8
import arcpy
path = r'E:\2022年项目\0802理塘入库\mdball'
arcpy.env.workspace = path
mdbs = arcpy.ListFiles('*.mdb')
for mdb in mdbs:
    riverName = arcpy.Describe(mdb).name.replace('.mdb', '').encode('utf-8')
    shp = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'DMAL'
    with arcpy.da.SearchCursor(shp,['RuleID','GB']) as yb:
        for row in yb:
            print riverName,row[0],row[1]
    # with arcpy.da.UpdateCursor(shp,['SHAPE@','RuleID']) as yb:
    #     for row in yb:
    #         if row[1] == 8:
    #             print riverName,row[1]
    #             yb.deleteRow()
