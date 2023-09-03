import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.filedialog import askopenfilename
from ttkbootstrap.dialogs import Messagebox
import time
from PIL import Image, ImageTk

## 设置全局变量
img_png = None
path = None

## 设置主窗口
root = ttk.Window(
    title="基于音频信号的机房设备状态分析系统",
    size=(1024,768),
    resizable=None,
    )

## 加载模型缓冲时间
msg = Messagebox.show_info(message="检测模型加载中，请稍等")

## labelframe类
lf = ttk.Labelframe(text="上传模块",bootstyle=PRIMARY,width=100,height=60)
lf.place(x=40,y=40,width=150,height=450)

lf2 = ttk.Labelframe(text="可视化模块",bootstyle=SUCCESS,width=100,height=60)
lf2.place(x=200,y=40,width=600,height=450)

lf3 = ttk.Labelframe(text="结果模块",bootstyle=INFO,width=100,height=60)
lf3.place(x=810,y=40,width=150,height=450)

lf4 = ttk.Labelframe(text="信息提示工作台",bootstyle=WARNING,width=100,height=60)
lf4.place(x=10,y=500,width=1000,height=200)

## 图片展示函数
def display():
	img_open = Image.open(path)
	img_open = img_open.resize((600, 400), Image.Resampling.LANCZOS)
	global img_png
	img_png = ImageTk.PhotoImage(img_open)
	label_img = ttk.Label(lf2, image = img_png)
	label_img.pack()

## 通用识别函数
def button_common():
    time_now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) # 获取时间并格式化
    global path
    path = askopenfilename()
##    print(path)
    if not path:
        return
    text.insert('insert',time_now + '\n') # 打印时间
    text.insert('insert','通用音频上传中...\n')
    text.insert('insert','音频预处理中...\n')
    text.insert('insert','可视化处理中...\n')
    display() # 调用图片
    text.insert('insert','结果输出中...\n')
    text.insert('insert','\n')
    text.see(ttk.END) # 光标跟随着插入的内容移动

## 机房识别函数
def button_IDC():
    time_now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) # 获取时间并格式化
##    path = askopenfilename()
##    print(path)
##    if not path:
##        return
    text.insert('insert',time_now + '\n') # 打印时间
    text.insert('insert','机房音频上传中...\n')
    text.insert('insert','音频预处理中...\n')
    text.insert('insert','可视化处理中...\n')
    text.insert('insert','结果输出中...\n')
    text.insert('insert','\n')
    text.see(ttk.END) #光标跟随着插入的内容移动
    result_IDC.insert('insert','故障\n','broken')
##    result_IDC.insert('insert','过载\n','overload')
##    result_IDC.insert('insert','正常\n','good')
    result_IDC.see(ttk.END) 

## 设置上传模块按钮
b1 = ttk.Button(lf, text='通用音频识别', bootstyle=PRIMARY, command=button_common)
b1.place(x=10,y=130,width=130,height=40)

b2 = ttk.Button(lf, text='机房故障检测', bootstyle=(INFO,OUTLINE), command=button_IDC)
b2.place(x=10,y=230,width=130,height=40)

## 设置结果展示文本框
result_common = ttk.Text(lf3,width=10, height=20)
result_common.place(x=10,y=130,width=130,height=60)


result_IDC = ttk.Text(lf3,width=10, height=20)
result_IDC.place(x=10,y=230,width=130,height=60)

## 设置机房音频结果标签
result_IDC.tag_config("broken", background="yellow", foreground="red")
result_IDC.tag_config("overload", background="green", foreground="yellow")
result_IDC.tag_config("good", foreground="green")

## 设置信息提示文本框
text = ttk.Text(lf4)
text.pack(padx=10,pady=10,fill=BOTH)



root.mainloop()

## 编辑区
