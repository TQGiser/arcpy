# coding=utf-8
def time_t(a):
    b = int(a.split('小时')[0])
    c = int((a.split('小时')[-1]).split('分')[0])
    d = int((a.split('分')[-1]).rstrip('秒'))
    re = b*3600 + c*60 + d
    return re
print(time_t('2小时33分55秒'))