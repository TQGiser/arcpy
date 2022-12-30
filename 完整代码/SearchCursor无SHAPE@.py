import arcpy
import os
os.chdir(r'E:\2021年项目\0319\1')
arcpy.env.workspace = (r'E:\2021年项目\0319\1')
filename = []
for i,v,m in os.walk(r'E:\2021年项目\0319\1'):
    for a in m:
        if a.endswith('.shp'):
            filename.append(a)
print(filename)
for b in filename:
    rows = arcpy.SearchCursor(b,fields='Name;CenterX;CenterY')
    for row in rows:
        print('River:{0} X={1} Y={2}'.format(row.getValue('Name'),row.getValue('CenterX'),row.getValue('CenterY')))
del rows