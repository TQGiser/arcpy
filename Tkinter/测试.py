# coding=utf-8
import arcpy
import os
import math
import pandas as pd
import F
import shutil
import tkinter as tk
# window = tk.Tk()
# window.title('test window')
# window.geometry('500x500')
# on_hit = False
# def hit_me():
#     global on_hit
#     if on_hit == False:
#         on_hit = True
#         var.set(get_text())
#     else:
#         on_hit = False
#         var.set('')
# e = tk.Entry(window,show = None)
# e.pack(padx =20,pady = 20)
# def get_text():
#     text = e.get()
#     return text
#
# var = tk.StringVar()
# label1 = tk.Label(window,textvariable = var,bg = 'red',font = ('Arial',12),width =12,height =1)
# label1.pack()
# button1 = tk.Button(window,text='校正无断面中线及设置桩位信息',width =30,height = 1,command = hit_me)
# button1.pack()
# window.mainloop()

#
# master = tk.Tk()
# tk.Label(master, text="作品：").grid(row=0)
# tk.Label(master, text="作者：").grid(row=1)
# e1 = tk.Entry(master)
# e2 = tk.Entry(master)
# e1.grid(row=0, column=1, padx=10, pady=5)
# e2.grid(row=1, column=1, padx=10, pady=5)
# def show():
#     print("作品：《%s》" % e1.get())
#     print("作者：%s" % e2.get())
#     e1.delete(0, "end")
#     e2.delete(0, "end")
# tk.Button(master, text="获取信息", width=10, command=show).grid(row=3, column=0, sticky="w", padx=10, pady=5)
# tk.Button(master, text="退出", width=10, command=master.quit).grid(row=3, column=1, sticky="e", padx=10, pady=5)
# master.mainloop()

master = tk.Tk()
tk.Label(master, text="出图影像大小控制").grid(row=0)
e1 = tk.Entry(master)
e1.grid(row=0, column=1, padx=10, pady=5)
def show():
    global fbl
    fbl = e1.get()
def quit():
    master.destroy()
tk.Button(master, text="确定", width=10, command=show).grid(row=3, column=0, sticky="w", padx=10, pady=5)
tk.Button(master,text='退出',width=10,command=quit).grid(row=3,column=5,sticky='w',padx=10, pady=5)
master.mainloop()

