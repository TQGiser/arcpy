#coding = utf-8
import pandas as pd
import os
from docxtpl import DocxTemplate
os.chdir(r'C:\Users\Administrator\Desktop\M09打包文件\M09C01\批量邀请函制作')
df = pd.read_excel('邀请函.xlsx')
for i in range(len(df)):
    dtdic = df.iloc[i,:].to_dict()
    doc = DocxTemplate('邀请函_模板.docx')
    doc.render(dtdic)
    doc.save(r'.\result\{}的邀请函.docx'.format(dtdic['姓名']))