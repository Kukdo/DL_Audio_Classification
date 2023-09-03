import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.filedialog import askopenfilename
from ttkbootstrap.dialogs import Messagebox
import time
from PIL import Image, ImageTk
import os
import librosa
from sklearn.preprocessing import scale
import numpy as np
import librosa.display
import matplotlib.pyplot as plt
from keras.models import load_model
from keras import metrics
from keras.preprocessing import image

esc_labels=['airplane','breathing','brushing_teeth','can_opening','car_horn','cat','chainsaw','chirping_birds','church_bells',
        'clapping','clock_alarm','clock_tick','coughing','cow','crackling_fire','crickets','crow','crying_baby','dog',
        'door_wood_creaks','door_wood_knock','drinking_sipping','engine','fireworks','footsteps','frog','glass_breaking',
        'hand_saw','helicopter','hen','insects','keyboard_typing','laughing','mouse_click','pig','pouring_water','rain',
        'rooster','sea_waves','sheep','siren','sneezing','snoring','thunderstorm','toilet_flush','train','vacuum_cleaner',
        'washing_machine','water_drops','wind']

def top_5_accuracy(y_true, y_pred):
    return metrics.top_k_categorical_accuracy(y_true, y_pred, k=5)

def save_melspectrogram(file_name, file_path, sampling_rate=44100):
    """ Will save spectogram into current directory"""
    
    data, sr = librosa.load(file_path, sr=sampling_rate, mono=True)
    data = scale(data)

    melspec = librosa.feature.melspectrogram(y=data, sr=sr, n_mels=128)
    # Convert to log scale (dB) using the peak power (max) as reference
        # per suggestion from Librbosa: https://librosa.github.io/librosa/generated/librosa.feature.melspectrogram.html
    log_melspec = librosa.power_to_db(melspec, ref=np.max)  
    librosa.display.specshow(log_melspec, sr=sr)
    
    # create saving directory
    directory = './melspectrograms'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    plt.savefig(directory + '/' + file_name.strip('.wav') + '.png')
    
def predict_engine_label():
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)* 1./255
    preds = model_engine.predict(x)[0]
    
    max_index = np.argmax(np.array(preds))
    result = ""
    if(max_index==0):
        result = "broken"
    elif(max_index==1):
        result = "good"
    else:
        result = "heavyload"
    return result

def predict_esc_label():
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)* 1./255
    preds = model_esc.predict(x)[0]
    
    max_index = np.argmax(np.array(preds))
    result = esc_labels[max_index]
    return result

## 图片展示函数
def display():
    global img_path
    img_open = Image.open(img_path)
    img_open = img_open.resize((600, 400), Image.Resampling.LANCZOS)
    global img_png
    img_png = ImageTk.PhotoImage(img_open)
    label_img = ttk.Label(lf2, image = img_png)
    label_img.pack()

## 通用识别函数
def button_common():
    time_now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) # 获取时间并格式化
    
    # 变量全局化
    global path
    global img_path
    
    # 获取音频路径
    path = askopenfilename()
    
    # 获取文件名
    file_name = path.split('/')[-1]
    if not path:
        return
    
    text.insert('insert',time_now + '\n') # 打印时间
    text.insert('insert','通用音频上传中...\n')
    text.insert('insert','音频预处理中...\n')
    
    # 频谱图转换
    save_melspectrogram(file_name, path)
    text.insert('insert','可视化处理中...\n')
    
    # 音频地址转频谱地址
    img_path=path.replace('test_data','melspectrograms')
    img_path=img_path.replace('wav','png')
    
    # 可视化函数调用
    display() 
    text.insert('insert','结果输出中...\n')
    
    # 模型预测
    res = predict_esc_label()
    
    # 预测值显示
    result_common.insert('insert', res)
    result_common.insert('insert', '\n')
    result_common.see(ttk.END)
    
    # 结束一轮
    text.insert('insert','\n')
    text.see(ttk.END) # 光标跟随着插入的内容移动

## 机房识别函数
def button_IDC():
    time_now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) # 获取时间并格式化
    
    # 变量全局化
    global path
    global img_path
    
    # 获取音频路径
    path = askopenfilename()
    
    # 获取文件名
    file_name = path.split('/')[-1]
    if not path:
        return
    
    text.insert('insert',time_now + '\n') # 打印时间
    text.insert('insert','机房音频上传中...\n')
    text.insert('insert','音频预处理中...\n')
    
    # 频谱图转换
    save_melspectrogram(file_name, path)
    text.insert('insert','可视化处理中...\n')
    
    # 音频地址转频谱地址
    img_path=path.replace('test_data','melspectrograms')
    img_path=img_path.replace('wav','png')
    
    # 可视化函数调用
    display() 
    text.insert('insert','结果输出中...\n')
    
    # 模型预测
    res = predict_engine_label()
    
    # 预测值显示
    result_IDC.insert('insert', res, res)
    result_IDC.insert('insert', '\n')
    result_IDC.see(ttk.END) 
    
    # 结束一轮
    text.insert('insert','\n')
    text.see(ttk.END) #光标跟随着插入的内容移动
## 设置全局变量
img_png = ""
path = ""
img_path = ""

## 设置主窗口
root = ttk.Window(
    title="基于音频信号的机房设备状态分析系统",
    size=(1024,768),
    resizable=None,
    )

## 加载模型
model_esc = load_model('./model/ESC50_94.h5', custom_objects={'top_5_accuracy': top_5_accuracy} )
model_engine = load_model('./model/ENGINE_99.h5', custom_objects={'top_5_accuracy': top_5_accuracy} )

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

## 事件响应刷新
root.mainloop()