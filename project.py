# -*- coding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib import parse
from tkinter import *
from tkinter import ttk
from urllib.parse import urlencode

def deltree(tree):
    x = tree.get_children()
    for i in x:
        tree.delete(i)

def get_data(url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html,"html.parser")
    data = bsObj.findAll("div",{"class":"col-lg-3 col-sm-6 col-6 text-center my-5"})
    creat_tree(data)
    
def creat_tree(data):
    deltree(tree)
    for i in data:
        str1 = i.get_text().strip('\n').split('\t')
        text = str1[0]
        case = str1[4].split('\n')[0]
        date = str1[4].split('\n')[1]
        tree.insert("",'end',text=text ,values=(case,date))

def itemSelected(event):
    obj = event.widget
    indexs = obj.curselection()
    for index in indexs:
        city_name = obj.get(index,index)
        lbl.config(text = "目前選取為：" + city_name[0])
        url_add = "city_confirmed.php?"+ urlencode([("mycity",city_name[0])])
        new_url = parse.urljoin(url,url_add.strip("+"))
        get_data(new_url)

root = Tk()
root.title("台灣 COVID-19 統計資訊")
root.geometry("600x490")

frame1 = Frame(root)
frame1.pack(side=LEFT,fill = Y)

lb1 = Listbox(frame1,font = ('微軟正黑體',12))
lb1.bind("<<ListboxSelect>>",itemSelected)
lb1.pack(side=LEFT,fill = Y)

frame2 = Frame(root)
frame2.pack(side=LEFT,fill = Y)

lbl = Label(frame2,font = ('微軟正黑體',12))
lbl.pack()

tree=ttk.Treeview(frame2,height =18)#表格
tree["columns"]=("數量","更新日期")
tree.column("數量",width=100)   #表示列,不顯示
tree.column("更新日期",width=100)
tree.heading("數量",text = "數量")  #顯示錶頭
tree.heading("更新日期",text = "更新日期")
tree.pack()

close = Button(frame2,text = "關閉",font = ('微軟正黑體',12) ,width = 8 ,height = 8, command = root.destroy)
close.pack(anchor = SE)

url = "https://covid-19.nchc.org.tw/dt_005-covidTable_taiwan.php"
html = urlopen(url)
bsObj = BeautifulSoup(html,"html.parser")
city = bsObj.findAll("span",{"style" : "font-size: 1em;"})
lb1.insert(END,"全部縣市")
for i in city:
    lb1.insert(END,i.get_text()[0:4])

root.mainloop()