#coding=utf-8
def degreeTrans(ys):
    a = ys.decode('utf-8')
    du = a.replace('E','').replace('°'.decode('utf-8'),'').split('.')[0] + '°'.decode('utf-8')
    fen = str('%02d'%int(float('0.' + a.replace('E','').replace('°'.decode('utf-8'),'').split('.')[1])*60)) + "'".decode('utf-8')
    miao = str('%02d'%int(float('0.' + str(float('0.' + a.replace('E','').replace('°'.decode('utf-8'),'').split('.')[1])*60).split('.')[1])*60))
    miao2 = '.'.decode('utf-8') + str('%03d'%round(float(str(float('0.' + str(float('0.' + a.replace('E','').replace('°'.decode('utf-8'),'').split('.')[1])*60).split('.')[1])*60).split('.')[1])/1000000))[0:3] + '"'.decode('utf-8')
    dfm = du + fen + miao + miao2
    b = round(float(str(float('0.' + str(float('0.' + a.replace('E','').replace('°'.decode('utf-8'),'').split('.')[1])*60).split('.')[1])*60).split('.')[1])/100)
    return b
# d = str(int(float(du))) + '°'.decode('utf-8') + str('%02d'%int(float('0.' + du.split('.')[1])*60)) + "'".decode('utf-8') + str(float('0.' + str(round(float('0.' + b.split('.')[1])*60,4)).split('.')[1])*60)

print du
print fen
print miao
print miao2
print dfm
print round(float(str(float('0.' + str(float('0.' + a.replace('E','').replace('°'.decode('utf-8'),'').split('.')[1])*60).split('.')[1])*60).split('.')[1])/100)
