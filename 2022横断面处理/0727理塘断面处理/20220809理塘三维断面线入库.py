#coding=utf-8
import arcpy
import F
path = r'E:\2022年项目\0802理塘入库\shps'
arcpy.env.workspace = path
dmals = F.listFiles(path,'','x')
riverNameList = []
for dmal in dmals:
    riverName = arcpy.Describe(dmal).basename.encode('utf-8')
    riverNameList.append(riverName)
    # arcpy.AddField_management(dmal,'RuleID','LONG')
    # arcpy.CalculateField_management(dmal, 'RuleID', '8', 'PYTHON_9.3')
    # arcpy.AddField_management(dmal,'NAME','TEXT')
    # arcpy.CalculateField_management(dmal, 'NAME', '!dmh!', 'PYTHON_9.3')
path2 = r'E:\2022年项目\0802理塘入库\mdball'
arcpy.env.workspace= path2
mdbs = arcpy.ListFiles('*.mdb')
for mdb in mdbs:
    riverName = arcpy.Describe(mdb).name.replace('.mdb', '').encode('utf-8')
    if riverName in riverNameList:
        print mdb
        mdb = r'E:\2022年项目\0802理塘入库\mdball\{}'.format(mdb.encode('utf-8'))
        dmal = r'E:\2022年项目\0802理塘入库\shps\{}.shp'.format(riverName)
        dmalInMdb = mdb + '\\' + 'DLG' + '\\' + 'DMAL'
        arcpy.Append_management(dmal,dmalInMdb,schema_type='NO_TEST')
