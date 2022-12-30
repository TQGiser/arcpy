#coding=utf-8
import arcpy
import os
import pandas as pd
import F
path = r'E:\2021年项目\1227广元'
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True
mdbs = arcpy.ListFiles('*.mdb')
for mdb in mdbs:
    LFCA = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'LFCA'
    LFCL = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'LFCL'
    HFCL = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'HFCL'
    HFCA = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'HFCA'
    JBXXA = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'JBXXA'
    JBXXL = path.decode('utf-8') + '\\' + mdb + '\\' + 'DLG' + '\\' + 'JBXXL'
    cs = arcpy.da.SearchCursor(LFCA,'*',"ruleid = 14 or ruleid = 85 or ruleid = 25")
    if len([row for row in cs]) > 0 :
        print mdb, LFCA
        tempshp = arcpy.CopyFeatures_management(LFCA,path + '\\' + 'temp.shp')
        with arcpy.da.UpdateCursor(tempshp,'RuleID') as yb:
            for row in yb:
                if not (row[0] == 14 or  row[0] == 85 or row[0] == 25):
                    yb.deleteRow()
        arcpy.Append_management(tempshp,JBXXA,schema_type='NO_TEST')
        arcpy.Delete_management(tempshp)
    cs2 = arcpy.da.SearchCursor(HFCA,'*',"ruleid = 38 or ruleid = 39")
    if len([row for row in cs2]) > 0 :
        print mdb, HFCA
        tempshp = arcpy.CopyFeatures_management(HFCA,path + '\\' + 'temp.shp')
        with arcpy.da.UpdateCursor(tempshp,'RuleID') as yb:
            for row in yb:
                if not (row[0] == 38 or  row[0] == 39):
                    yb.deleteRow()
        arcpy.Append_management(tempshp,JBXXA,schema_type='NO_TEST')
        arcpy.Delete_management(tempshp)
    cs3 = arcpy.da.SearchCursor(LFCL,'*',"ruleid = 46")
    if len([row for row in cs3]) > 0 :
        print mdb, LFCL
        tempshp = arcpy.CopyFeatures_management(LFCL,path + '\\' + 'temp.shp')
        with arcpy.da.UpdateCursor(tempshp,'RuleID') as yb:
            for row in yb:
                if not (row[0] == 46):
                    yb.deleteRow()
        arcpy.Append_management(tempshp,JBXXL,schema_type='NO_TEST')
        arcpy.Delete_management(tempshp)
    cs4 = arcpy.da.SearchCursor(HFCL,'*',"ruleid = 2")
    if len([row for row in cs4]) > 0 :
        print mdb, HFCL
        tempshp = arcpy.CopyFeatures_management(HFCL,path + '\\' + 'temp.shp')
        with arcpy.da.UpdateCursor(tempshp,'RuleID') as yb:
            for row in yb:
                if not (row[0] == 2):
                    yb.deleteRow()
        arcpy.Append_management(tempshp,JBXXL,schema_type='NO_TEST')
        arcpy.Delete_management(tempshp)
