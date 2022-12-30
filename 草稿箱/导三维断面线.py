# coding=utf-8
import arcpy
import os
import math
import pandas as pd
import F

path = r'E:\2021年项目\1202理塘断面处理\102'
d = F.listFile(path, '102', 'd')
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
Line = arcpy.CopyFeatures_management(lp, path + '\\' + 'dmx102Line.shp')
print 'COPY OK'
with arcpy.da.UpdateCursor(Line, ['SHAPE@', 'SHAPE@X', 'SHAPE@Z','SHAPE@Y'], explode_to_points=True) as yb:
    for row in yb:
        for cn in cnLst:
            if abs(row[1] - float(cn[0])) < 0.1 and abs(row[3] - float(cn[1])) <0.1:
                row[2] = round(float(cn[2]),2)
                print cn[3]
                yb.updateRow(row)



# def 单独三维线():
arcpy.env.overwriteOutput = True
path = r'E:\2021年项目\1202理塘断面处理\全部三维断面线\temp'
d = F.listFile(path, 'A', 'd')
cnLst = []
Lines = []
with arcpy.da.SearchCursor(d, ['SHAPE@X', 'SHAPE@Y', 'ELEV', 'dh']) as yb:
    for p in yb:
        cn = [p[0], p[1], p[2], p[3]]
        cnLst.append(cn)
cnLst2 = sorted(cnLst, key=lambda s: s[3])
Lines.append(arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in cnLst2])))
arcpy.env.outputZFlag = 'Enabled'
Line = arcpy.CopyFeatures_management(Lines, path + '\\' + 'okLine.shp')
i = 0
with arcpy.da.UpdateCursor(Line, ['SHAPE@', 'SHAPE@X', 'SHAPE@Z'], explode_to_points=True) as yb:
    for row in yb:
        for cn in cnLst2:
            if abs(row[1] - float(cn[0])) < 0.1:
                row[2] = cn[2]
                print cn[3]
                i += 1
        yb.updateRow(row)



# arcpy.env.overwriteOutput = True
# pd.set_option('display.width',100)
# path = r'E:\2021年项目\1130巴塘断面线入库\shape'.decode('utf-8')
# arcpy.env.workspace = path
# df = pd.read_excel(r'E:\2021年项目\1130巴塘断面线入库\全部断面表格\all.xlsx'.decode('utf-8'))
# cnList = []
# for name,value in df.iterrows():
#     cn = [df.loc[name,'x'],df.loc[name,'y'],df.loc[name,'elev'],df.loc[name,'dh'],df.loc[name,'dmh']]
#     cnList.append(cn)
# p = arcpy.CreateFeatureclass_management(path,'allPoint','POINT')
# arcpy.AddField_management(p,'elev','TEXT')
# arcpy.AddField_management(p,'dh','TEXT')
# arcpy.AddField_management(p,'dmh','TEXT')
# yb = arcpy.da.InsertCursor(p,['SHAPE@X','SHAPE@Y','elev','dh','dmh'])
# for cn in cnList:
#     print cn
#     yb.insertRow(cn)
# del yb


# path = r'E:\2021年项目\1130巴塘断面线入库\全部断面表格'.decode('utf-8')
# os.chdir(path)
# lst = []
# cnList = []
# for i,v,m in os.walk(path):
#     for xls in m:
#         lst.append(os.path.join(i, xls))
# for xls in lst:
#     print xls
#     df = pd.read_excel(xls,header=1)
#     for name,value in df.iterrows():
#         if type(df.loc[name,'另点距'.decode('utf-8')]) is unicode:
#             if '-' in df.loc[name,'另点距'.decode('utf-8')]:
#                 dmmc = df.loc[name,'另点距'.decode('utf-8')]
#                 i =0
#         a = [df.loc[name,'Y'],df.loc[name,'X'],df.loc[name,'高程'.decode('utf-8')],i,dmmc]
#         cnList.append(a)
#         i+=1
# df = pd.DataFrame(cnList,columns=['A','B','C','D','E'])
# df.to_excel(path + '\\' + 'all.xlsx',index=False)


# # coding=utf-8
# import arcpy
# import os
# import math
# import pandas as pd
# import F
# arcpy.env.overwriteOutput = True
# path = r'E:\2021年项目\1130巴塘断面线入库\shape'
# d = F.listFile(path, 'a', 'd')
# cnLst = []
# Lines = []
# with arcpy.da.SearchCursor(d, ['SHAPE@X', 'SHAPE@Y', 'elev', 'Y']) as yb:
#     for p in yb:
#         cn = [p[0], p[1], p[2], p[3]]
#         cnLst.append(cn)
# cnLst2 = sorted(cnLst, key=lambda s: s[3])
# Lines.append(arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in cnLst2])))
# arcpy.env.outputZFlag = 'Enabled'
# Line = arcpy.CopyFeatures_management(Lines, path + '\\' + 'Line1201')
# i = 0
# with arcpy.da.UpdateCursor(Line, ['SHAPE@', 'SHAPE@X', 'SHAPE@Z'], explode_to_points=True) as yb:
#     for row in yb:
#         for cn in cnLst2:
#             if round(row[1], 2) == round(cn[0], 2):
#                 row[2] = cn[2]
#                 print cn[3]
#                 i += 1
#         yb.updateRow(row)

