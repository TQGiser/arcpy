# coding=utf-8
import arcpy
import pandas as pd
path = r'E:\2022年项目\0707沙朗沟断面\slg'
arcpy.env.workspace = path
d = r'E:\2022年项目\0707沙朗沟断面\slg\ldq.shp'
Fzx = r'E:\2022年项目\0707沙朗沟断面\slg\fzx.shp'
cnList = []
with arcpy.da.SearchCursor(d,['SHAPE@','dmh','SHAPE@X','SHAPE@Y','elev']) as yb1:
    for row in yb1:
        with arcpy.da.SearchCursor(Fzx,'SHAPE@') as yb2:
            for row2 in yb2:
                cn = [row[1],row[0].distanceTo(row2[0]),row[2],row[3],row[4]]
                cnList.append(cn)
df = pd.DataFrame(cnList,columns=['dmh','dis','x','y','h'])
df_all = pd.DataFrame(columns=['dmh','dis','x','y','h'])
df2 = df.groupby('dmh')
for name,group in df2:
    df3 = group
    df3.sort_values(by='dis',ascending=True, inplace=True)
    print name
    df3.to_csv(path.decode('utf') + '\\' + 'csv'.decode('utf-8') + '\\'+ (r'{}.csv').format(name).decode('utf-8'),index=False)
    # df_all=df_all.append(df3)
# df_all.to_csv(r'E:\2022年项目\0420许曲断面线\a.csv'.decode('utf-8'),index=False)