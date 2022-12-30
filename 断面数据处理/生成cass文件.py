df = pd.read_excel(allexcel)
df.drop(['X','Y','备注'.decode('utf-8')], axis=1, inplace=True)
a = df[df.T.isnull().any()]
for index, value in a.iterrows():
    df.loc[index, '高程'.decode('utf-8')] = value['另点距'.decode('utf-8')]
    df.loc[index,'另点距'.decode('utf-8')] = 'BEGIN'
df.drop(['点号'.decode('utf-8')],axis=1,inplace= True)
cassfile = outpath + '\\' + 'cass.xls'
df.to_excel(cassfile,index = False,header=False)