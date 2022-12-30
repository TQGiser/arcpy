import os
os.chdir(r'C:\Users\Administrator\Desktop\M09打包文件\M09C02')
for i,v,m in os.walk('./original/'):
    #picslst = [os.path.join(i,v) for name in m]
    fls = [os.path.join(i,name) for name in m]
    print(fls)
    print(len(fls))
