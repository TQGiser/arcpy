import arcpy
import os
os.chdir(r'/TEST/rivers (1)')
arcpy.env.worksapce = (r'E:\arcpy\TEST\rivers (1)')
lst = []
for i,v,m in os.walk(r'/TEST/rivers (1)'):
    for name in m:
        if name.endswith('.shp'):
            lst.append(name)
print(type(lst))
for i in lst:
    name2 = i
    print(type(name2))
    myyb = arcpy.UpdateCursor(name2)
    arcpy.AddField_management(name2,'newname4','TEXT')
    print('handing:{}'.format(name2))
    for row in myyb:
        zdmc1 = 'newname4'
        zdmc2 = name2.strip('.shp')
        row.setValue(zdmc1,zdmc2)
        myyb.updateRow(row)
del row
del myyb