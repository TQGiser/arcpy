# coding=utf-8
import arcpy
import pandas as pd
import math
import F
arcpy.env.overwriteOutput=True
path = r'E:\2021年项目\1222岸线规划\定曲'
arcpy.env.workspace = path
dmal = F.listFile(path,'管理范围线'.decode('utf-8'),'x')
riverName = arcpy.Describe(dmal).baseName.replace('管理范围线'.decode('utf-8'),'')
qs = F.listFile(path,'桥梁'.decode('utf-8'),'m')
zx = F.listFile(path,'校正后中线'.decode('utf-8'),'x')
tempLines = []
cnList = []
sp = arcpy.Describe(dmal).spatialReference
if '99' in sp.name:
    xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-99.shp'
    fdh = 99
elif '102' in sp.name:
    xzjx = r'D:\资料\甘孜乡镇\甘孜乡镇界带县名-102.shp'
    fdh = 102
with arcpy.da.SearchCursor(dmal,'SHAPE@') as yb:
    for row in yb:
        with arcpy.da.SearchCursor(qs, ['SHAPE@','Name']) as yb2:
            for row2 in yb2:
                QName = row2[1]
                for part in row2[0]:
                    MList = []
                    for pnt in part:
                        MList.append(row[0].measureOnLine(pnt))
                    cn = [row[0].segmentAlongLine(min(MList),max(MList)),QName]
                    tempLines.append(cn)
QToL = arcpy.CreateFeatureclass_management(path,'QToL.shp','POLYLINE',template=qs,spatial_reference=sp)
cs = arcpy.da.InsertCursor(QToL,['SHAPE@','Name'])
for shp in tempLines:
    cs.insertRow([shp[0],shp[1]])
with arcpy.da.SearchCursor(QToL,['SHAPE@','Name']) as yb:
    for row in yb:
        lx = '桥梁'
        print row[1]
        if row[0] is not None :
            with arcpy.da.SearchCursor(xzjx,['SHAPE@','XZQMC','XZQMC_1']) as yb2:
                for row2 in yb2:
                    if row2[0].contains(row[0]):
                        qxmc = row2[2] + row2[1]
            with arcpy.da.SearchCursor(zx,'SHAPE@') as yb3:
                for row3 in yb3:
                    if row3[0].queryPointAndDistance(row[0].firstPoint)[3] is True:
                        ab = '右岸'
                    else:
                        ab = '左岸'
            with arcpy.da.SearchCursor(dmal,'SHAPE@') as yb4:
                for row4 in yb4:
                    m1 = row4[0].measureOnLine(row[0].firstPoint)
                    m2 = row4[0].measureOnLine(row[0].lastPoint)
                    p1x = 'E' + '%0.8f'%round(F.XY2LatLon(row[0].firstPoint.X,row[0].firstPoint.Y,fdh)[1],8) + '°'
                    p1y ='N' + '%0.8f'%round(F.XY2LatLon(row[0].firstPoint.X,row[0].firstPoint.Y,fdh)[0],8)+ '°'
                    p2x = 'E' + '%0.8f'%round(F.XY2LatLon(row[0].lastPoint.X,row[0].lastPoint.Y,fdh)[1],8) + '°'
                    p2y = 'N' + '%0.8f'%round(F.XY2LatLon(row[0].lastPoint.X,row[0].lastPoint.Y,fdh)[0],8) + '°'
                    if m1<m2:
                        qdm = m1
                        zdm = m2
                        qdx = p1x
                        qdy = p1y
                        zdx = p2x
                        zdy = p2y
                    else:
                        qdm = m2
                        zdm = m1
                        qdx = p2x
                        qdy = p2y
                        zdx = p1x
                        zdy = p1y
                    qdm2 = 'K' + str(int(qdm / 1000.0)) + '+' + '%03d' % (qdm % 1000)
                    zdm2 = 'K' + str(int(zdm / 1000.0)) + '+' + '%03d' % (zdm % 1000)
                    # if ab == '左岸':
                    #     qdm2 = 'LK' + str(int(qdm / 1000.0)) + '+' + '%03d' % (qdm % 1000)
                    #     zdm2 = 'LK' + str(int(zdm / 1000.0)) + '+' + '%03d' % (zdm % 1000)
                    # elif ab == '右岸':
                    #     qdm2 = 'RK' + str(int(qdm / 1000.0)) + '+' + '%03d' % (qdm % 1000)
                    #     zdm2 = 'RK' + str(int(zdm / 1000.0)) + '+' + '%03d' % (zdm % 1000)
            cn = [row[1],lx,ab,qxmc,'%0.2f'%round(row[0].length,2),qdx,qdy,zdx,zdy,qdm2,zdm2,qdm]
            cnList.append(cn)
arcpy.Delete_management(QToL)
try:
    df = F.listFile(path,'堤防'.decode('utf-8'),'x')
    with arcpy.da.SearchCursor(df, ['SHAPE@', 'Name']) as yb:
        for row in yb:
            lx = '堤防'
            print row[1]
            with arcpy.da.SearchCursor(xzjx, ['SHAPE@', 'XZQMC', 'XZQMC_1']) as yb2:
                for row2 in yb2:
                    if row2[0].contains(row[0]):
                        qxmc = row2[2] + row2[1]
            with arcpy.da.SearchCursor(dmal, 'SHAPE@') as yb4:
                for row4 in yb4:
                    m1 = row4[0].measureOnLine(row[0].firstPoint)
                    m2 = row4[0].measureOnLine(row[0].lastPoint)
                    tempLine = row4[0].segmentAlongLine(m1,m2)
                    p1x = 'E' + '%0.8f'%round(F.XY2LatLon(tempLine.firstPoint.X, tempLine.firstPoint.Y, fdh)[1], 8) + '°'
                    p1y = 'N' + '%0.8f'%round(F.XY2LatLon(tempLine.firstPoint.X, tempLine.firstPoint.Y, fdh)[0], 8) + '°'
                    p2x = 'E' + '%0.8f'%round(F.XY2LatLon(tempLine.lastPoint.X, tempLine.lastPoint.Y, fdh)[1], 8) + '°'
                    p2y = 'N' + '%0.8f'%round(F.XY2LatLon(tempLine.lastPoint.X, tempLine.lastPoint.Y, fdh)[0], 8) + '°'
                    if m1 < m2:
                        qdm = m1
                        zdm = m2
                        qdx = p1x
                        qdy = p1y
                        zdx = p2x
                        zdy = p2y
                    else:
                        qdm = m2
                        zdm = m1
                        qdx = p2x
                        qdy = p2y
                        zdx = p1x
                        zdy = p1y
                    qdm2 = 'K' + str(int(qdm / 1000.0)) + '+' + '%03d' % (qdm % 1000)
                    zdm2 = 'K' + str(int(zdm / 1000.0)) + '+' + '%03d' % (zdm % 1000)
                    # if ab == '左岸':
                    #     qdm2 = 'LK' + str(int(qdm / 1000.0)) + '+' + '%03d' % (qdm % 1000)
                    #     zdm2 = 'LK' + str(int(zdm / 1000.0)) + '+' + '%03d' % (zdm % 1000)
                    # elif ab == '右岸':
                    #     qdm2 = 'RK' + str(int(qdm / 1000.0)) + '+' + '%03d' % (qdm % 1000)
                    #     zdm2 = 'RK' + str(int(zdm / 1000.0)) + '+' + '%03d' % (zdm % 1000)
            with arcpy.da.SearchCursor(zx, 'SHAPE@') as yb3:
                for row3 in yb3:
                    if row3[0].queryPointAndDistance(row[0].firstPoint)[3] is True:
                        ab = '右岸'
                    else:
                        ab = '左岸'
            cn = [row[1], lx,ab, qxmc, '%0.2f' % round(tempLine.length, 2), qdx, qdy, zdx, zdy, qdm2, zdm2,qdm]
            cnList.append(cn)
except:
    print '没有堤防'
cnList2 = sorted(cnList,key = lambda s:s[11])
df = pd.DataFrame(cnList2,columns=['名称','涉河设施类别','岸别','县（区）','占用岸线长度（m)','起点经度','起点纬度','终点经度','终点纬度',
                                  '起点里程','终点里程','Num'])
xlsx = path + '\\' + '{}涉河设施表.xlsx'.format(riverName.encode('utf-8'))
df.to_excel(xlsx.decode('utf-8'),index=False)