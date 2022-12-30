# coding=utf-8
import os
import pandas as pd
import arcpy
arcpy.env.overwriteOutput=True
# path =raw_input('目录地址:').decode('utf-8')
path = r'E:\2022年项目\0621理塘断面\理塘外业成果\陈\额地仁'.decode('utf-8')
outpath = r'E:\2022年项目\0621理塘断面\dmx'
os.chdir(path)
lst = []
for i,v,m in os.walk(path):
    for xls in m:
        lst.append(os.path.join(i, xls))
cnList = []
for xls in lst:
    print xls
    df = pd.read_excel(xls)
    dmhList = []
    for index,row in df.iterrows():
        if type(df.iloc[index,1]) is unicode and '-'.decode('utf-8') in df.iloc[index, 1] :
            dmhList.append(df.iloc[index,1])
        if len(dmhList) >0 :
            a = [df.iloc[index,0],df.iloc[index,1],df.iloc[index,2],df.iloc[index,3],df.iloc[index,4],df.iloc[index,5],dmhList[-1]]
            cnList.append(a)
df = pd.DataFrame(cnList,columns=['dh','dis','elev','bz','y','x','dmh'])
cnList = []
for name,value in df.iterrows():
    cn = [df.loc[name,'x'],df.loc[name,'y'],df.loc[name,'elev'],df.loc[name,'dh'],df.loc[name,'dmh']]
    cnList.append(cn)
p = arcpy.CreateFeatureclass_management(path,'allPoint','POINT')
arcpy.AddField_management(p,'elev','TEXT')
arcpy.AddField_management(p,'dh','TEXT')
arcpy.AddField_management(p,'dmh','TEXT')
yb = arcpy.da.InsertCursor(p,['SHAPE@X','SHAPE@Y','elev','dh','dmh'])
for cn in cnList:
    if not pd.isnull(cn[0]):
        yb.insertRow(cn)
del yb
cnLst=[]
with arcpy.da.SearchCursor(p, ['SHAPE@X', 'SHAPE@Y', 'elev', 'dh', 'dmh']) as yb:
    for p in yb:
        cn = [p[0], p[1], p[2], p[3], p[4]]
        cnLst.append(cn)
shpName = arcpy.Describe(path + '\\' + 'allpoint.shp').path.encode('utf-8').split('\\')[-1]
arcpy.Delete_management(path + '\\' + 'allpoint.shp')
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
Line = arcpy.CopyFeatures_management(lp, outpath + '\\' + shpName + '.shp')
arcpy.DefineProjection_management(outpath+'\\' + shpName + '.shp',coor_system='4543')
arcpy.AddField_management(Line,'dmh','text')
with arcpy.da.UpdateCursor(Line, ['SHAPE@', 'SHAPE@X', 'SHAPE@Z','dmh','SHAPE@Y'], explode_to_points=True) as yb:
    for row in yb:
        for cn in cnLst:
            if abs(row[1] - float(cn[0])) < 0.1 and abs(row[4] - float(cn[1])) <0.1:
                row[2] = round(float(cn[2]),2)
                row[3] = cn[4]
                yb.updateRow(row)