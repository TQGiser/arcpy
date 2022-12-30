def cal_CZ(xlist,x,y):
    cnList = []
    i = 0
    for i in range(0,len(xlist)-1):
        x1 = xlist[i][0]
        y1 = xlist[i][1]
        num = xlist[i][2]
        x2 = xlist[i + 1][0]
        y2 = xlist[i + 1][1]
        czx = ((x - x1) * (x1 - x2) + (y - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (x1 - x2) + x1
        czy = ((x - x1) * (x1 - x2) + (y - y1) * (y1 - y2)) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) * (y1 - y2) + y1
        if czx > min(x1, x2) and czx < max(x1, x2) and czy > min(y1, y2) and czy < max(y1, y2):
            dis = math.sqrt((x - czx) ** 2 + (y - czy) ** 2)
            cn = [x1, x2, dis,czx, czy,num]
            cnList.append(cn)
        else:
            dis = math.sqrt((x - x1) ** 2 + (y - y1) ** 2)
            cn = [x1, x2, dis,czx, czy,num]
            cnList.append(cn)
        cnSort = sorted(cnList, key=lambda s: s[2])
        i +=1
        Czx = cnSort[0][3]
        Czy = cnSort[0][4]
        pNum = cnSort[0][5]
    return Czx,Czy,pNum