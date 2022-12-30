#coding=utf-8
import arcpy
import pandas as pd
arcpy.env.overwriteOutput = True
pd.set_option('display.width',100)
path = r'E:\2022年项目\0729理塘断面\102'
arcpy.env.workspace = path
xlsx = path + '\\' + 'dmd.xlsx'
df = pd.read_excel(xlsx.decode('utf-8'))
cnList = []
for name,value in df.iterrows():
    cn = [df.loc[name,'x'],df.loc[name,'y'],df.loc[name,'elev'],df.loc[name,'dh'],df.loc[name,'dmh']]
    cnList.append(cn)
p = arcpy.CreateFeatureclass_management(path,'dmd','POINT')
arcpy.AddField_management(p,'elev','TEXT')
arcpy.AddField_management(p,'dh','TEXT')
arcpy.AddField_management(p,'dmh','TEXT')
yb = arcpy.da.InsertCursor(p,['SHAPE@X','SHAPE@Y','elev','dh','dmh'])
for cn in cnList:
    print cn
    yb.insertRow(cn)
del yb
dmh1Lst = [a[4] for a in cnList]
dmhLst = list(set(dmh1Lst))
i = 0
lp = []
for i in range(0, len(dmhLst)):
    pg = []
    groupLst = []
    for cn in cnList:
        if cn[4] == dmhLst[i]:
            groupLst.append(cn)

    for p in groupLst:
        xp = [p[0], p[1]]
        pg.append(xp)
    i += 1
    lp.append(arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in pg])))
arcpy.env.outputZFlag = 'Enabled'
Line = arcpy.CopyFeatures_management(lp, path + '\\' + 'dmx.shp')
print 'COPY OK'
with arcpy.da.UpdateCursor(Line, ['SHAPE@', 'SHAPE@X', 'SHAPE@Z','SHAPE@Y'], explode_to_points=True) as yb:
    for row in yb:
        for cn in cnList:
            if abs(row[1] - float(cn[0])) < 0.1 and abs(row[3] - float(cn[1])) <0.1:
                row[2] = round(float(cn[2]),2)
                print cn[3]
                yb.updateRow(row)
