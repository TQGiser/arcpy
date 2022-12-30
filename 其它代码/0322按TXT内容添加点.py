import arcpy
import os
arcpy.env.workspace = (r'E:\arcpy\data\0322.gdb')
os.chdir(r'/data')
'''fields = ['latitude','longitude','confid']
yb = arcpy.UpdateCursor('test3')
for name in fields:
    fn = name
    print(fn)
    arcpy.AddField_management('test3',fn, "FLOAT",field_length=50)
del yb '''                                                            #批量添加字段


f = open('NorthAmericaWildfires_2007275.txt','r')
lstFires = f.readlines()
yb = arcpy.da.InsertCursor('test3',('latitude','longitude','confid'))
for fire in lstFires:
    if 'Latitude' in fire:
        continue
    vals = fire.split(',')
    latitude = float(vals[0])
    longitude = float(vals[1])
    confid = float(vals[2])
    rowValue = (latitude,longitude,confid)
    yb.insertRow(rowValue)