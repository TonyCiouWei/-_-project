import matplotlib.pyplot as plt
import numpy as np
import time
import time, random
import math
import serial
from collections import deque
from scipy import signal
from scipy.signal import firwin
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

def draw_response_zeroandpole(coefficient,a):
    gain = []
    for i in range(0,50):
        t = np.arange(0, 1, 0.01)
        x = np.cos(2*np.pi*i*t)
        y = signal.lfilter(coefficient, a, x)
        gain.append(max(y))
    ft = range(0,50)
    b = Figure(figsize=(4, 6), dpi=100)
    response = b.add_subplot(211)
    response.set_title("Filter's Frequency Response")
    response.set_xlabel("Frequency")
    response.set_ylabel("Gain")
    response.plot(ft,gain)
    #######Filter zero & pole#######
    result = np.roots(coefficient)
    angle = np.linspace(-np.pi,np.pi,50)
    cirx = np.sin(angle)
    ciry = np.cos(angle)
    c = b.add_subplot(212)
    c.plot(cirx,ciry,"k-")
    c.plot(0,0,"x",markersize = 12)
    c.plot(np.real(result),np.imag(result),"o",markersize = 12)
    c.grid()
    # 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
    canvas = FigureCanvasTkAgg(b, master=response_ZeroAndPole_frame)
    canvas.draw()  # 注意show方法已经过时了,这里改用draw
    canvas.get_tk_widget().place(x = 100,y = 0)
#bandpass_firwin
def bandpass_firwin(ntaps, lowcut, highcut, fs, window='hamming'):
    nyq = 0.5 * fs
    taps = firwin(ntaps, [lowcut, highcut], nyq=nyq, pass_zero=False,
                  window=window, scale=False)
    return taps
def set_butter_filter(fs,order,low_cut,high_cut):
    # calculate the Nyquist frequency
    nyq = 0.5 * fs
    # design filter
    low = low_cut / nyq
    high = high_cut / nyq
    coefficient, a = signal.butter(order, [low, high], btype='band')
    return coefficient, a
def _quit():
    root.quit() 
    root.destroy() 
def get_bpm(PData_x_axis,PData_y_axis,t1,t2):
    ys = [i for i in range(100)]
    for i in range(100):
        ys[i] = PData_y_axis[i]
    t2 = PData.axis_x[np.argmax(ys)]
    if abs(t2 - t1) != 0:
        bpm = (1 / (abs(t2 - t1)) ) * 60
    t1 = t2
    return bpm
#Display loading 
class PlotData:
    def __init__(self, max_entries=30):
        self.axis_x = deque(maxlen=max_entries)
        self.axis_y = deque(maxlen=max_entries)
        self.axis_y1 = deque(maxlen=max_entries)
    def add(self, x, y, y1):
        self.axis_x.append(x)
        self.axis_y.append(y)
        self.axis_y1.append(y1)


#########定義視窗##########
root = tk.Tk()  # 創建tkinter的主窗口
root.title("訊號與系統期末專題")
root.geometry("1280x800")
##########################

#########Frame#########
filter_choice_frame = tk.LabelFrame(root,text = "Choose filter",height = 200,width = 600)
filter_choice_frame.place(x = 0,y = 0) 
response_ZeroAndPole_frame = tk.LabelFrame(root,text = "Response & Zero & Pole",height = 600,width = 600)
response_ZeroAndPole_frame.place(x = 0,y = 200)
pulse_realtime_frame = tk.LabelFrame(root,text = "Pulse in real time",height = 700,width = 680)
pulse_realtime_frame.place(x = 600,y = 0)
bpm_frame = tk.Frame(root,height = 100,width = 680)
bpm_frame.place(x = 600,y = 700)
#######################

##filter_choice_frame##
choose_lable = tk.Label(master = filter_choice_frame,text = "Choose the filter : ",height = 1,width = 20,bg = "yellow")
choose_lable.place(x = 25,y = 30)
# fs_lable = tk.Label(master = filter_choice_frame,text = "Sampling frequency : ",height = 1,width = 20,bg = "yellow")
# fs_lable.place(x = 25,y = 60)
# fs_entry = tk.Entry(master = filter_choice_frame,width = 31)
# fs_entry.place(x = 175,y = 60)
low_cut_lable = tk.Label(master = filter_choice_frame,text = "Low cut : ",height = 1,width = 20,bg = "yellow")
low_cut_lable.place(x = 25,y = 75)
# low_cut_entry = tk.Entry(master = filter_choice_frame,width = 31)
# low_cut_entry.place(x = 175,y = 90)
low_cut_scale = tk.Scale(master = filter_choice_frame, from_=0.5, to=1, orient='horizontal', resolution=0.1, showvalue=True)
low_cut_scale.place(x = 175,y = 55)
high_cut_lable = tk.Label(master = filter_choice_frame,text = "High cut : ",height = 1,width = 20,bg = "yellow")
high_cut_lable.place(x = 25,y = 120)
# high_cut_entry = tk.Entry(master = filter_choice_frame,width = 31)
# high_cut_entry.place(x = 175,y = 120)
high_cut_scale = tk.Scale(master = filter_choice_frame, from_=5, to=10, orient='horizontal', resolution=1, showvalue=True)
high_cut_scale.place(x = 175,y = 100)
filter_option = tk.StringVar(filter_choice_frame)
filter_option.set("三點平均濾波器(Default)")
filter_choise = tk.OptionMenu(filter_choice_frame,filter_option,"三點平均濾波器(Default)","bandpass_firwin","butter")
filter_choise.config(height = 1,width = 25)
filter_choise.place(x = 175,y = 25)
quit_button = tk.Button(master = filter_choice_frame , text="Quit", command=_quit)
quit_button.place(x = 200,y = 150)
#######################

#######bpm_frame#######
bpm_lable = tk.Label(master = bpm_frame,text = " 即時心律 : ",height = 1,width = 20,bg = "yellow")
bpm_lable.place(x = 20, y = 50)
#######################

######初始值設定########
fig, (ax,ax2,ax3) = plt.subplots(3,1)

line,  = ax.plot(np.random.randn(100))
line2, = ax2.plot(np.random.randn(100))
line3, = ax3.plot(np.random.randn(100))
# plt.show(block = False)
plt.setp(line2,color = 'r')
plt.setp(line3,color = "k")
PData= PlotData(500)
ax.set_ylim(200, 600)
ax2.set_ylim(-200,400)
ax3.set_ylim(0,1000)
# plot parameters
print('plotting data...')
# open serial port
strPort='com4'
ser = serial.Serial(strPort, 115200)
ser.flush()
start = time.time()
x = [i for i in range(100)]
y = [i for i in range(100)]
y1 = [i for i in range(100)]
f = np.arange(0, 100, 1)
t1 = 0
t2 = 0
########################
#########顯示視窗##########
while(True):
    for ii in range(100):
        try:
            data = float(ser.readline())
            x[ii] = time.time() - start
            y[ii] = data.real
            y1[ii] = data.real
        except:
            pass
    ##response_ZeroAndPole_frame##
    #######頻率響應#######
    if(filter_option.get() == "三點平均濾波器(Default)"):
        ax2.set_ylim(-20,20)
        draw_response_zeroandpole([1/3,1/3,1/3],1)
        y = np.fft.fft(y)
        y[0] = 0
        y = np.fft.ifft(y)
        y = signal.lfilter([1/3,1/3,1/3], 1, y)
        #print(np.argmax(abs(np.fft.fft(y))))
        for ii in range(100):
            PData.add(x[ii], y[ii], y1[ii])
        ax.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
        ax2.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
        line.set_xdata(PData.axis_x)
        line.set_ydata(PData.axis_y1)
        line2.set_xdata(PData.axis_x)
        line2.set_ydata(PData.axis_y)
        line3.set_xdata(f)
        line3.set_ydata(abs(np.fft.fft(y)))
        canvas1 = FigureCanvasTkAgg(fig, master=pulse_realtime_frame)
        canvas1.draw()  
        canvas1.get_tk_widget().place(x = 20, y = 100)
        ##BPM##
        ys = [i for i in range(100)]
        for i in range(100):
            ys[i] = PData.axis_y[i]
        t2 = PData.axis_x[np.argmax(ys)]
        if abs(t2 - t1) != 0:
            bpm = (1 / (abs(t2 - t1)) ) * 60
        t1 = t2
        bpm_show_lable = tk.Label(master = bpm_frame , text = str(bpm),height = 1,width = 20,bg = "yellow")
        bpm_show_lable.place(x = 150, y = 50)

    elif(filter_option.get() == "bandpass_firwin"):
        ax2.set_ylim(-200,400)
        coefficient = bandpass_firwin(100, low_cut_scale.get(), high_cut_scale.get(), fs=100)
        draw_response_zeroandpole(coefficient,1)
        y = signal.lfilter(coefficient, 1, y)
        for ii in range(100):
            PData.add(x[ii], y[ii], y1[ii])
        ax.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
        ax2.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
        line.set_xdata(PData.axis_x)
        line.set_ydata(PData.axis_y1)
        line2.set_xdata(PData.axis_x)
        line2.set_ydata(PData.axis_y)
        line3.set_xdata(f)
        line3.set_ydata(abs(np.fft.fft(y)))
        canvas2 = FigureCanvasTkAgg(fig, master=pulse_realtime_frame)
        canvas2.draw()
        canvas2.get_tk_widget().place(x = 20, y = 100)
        ##BPM##
        ys = [i for i in range(100)]
        for i in range(100):
            ys[i] = PData.axis_y[i]
        t2 = PData.axis_x[np.argmax(ys)]
        if abs(t2 - t1) != 0:
            bpm = (1 / (abs(t2 - t1)) ) * 60
        t1 = t2
        bpm_show_lable = tk.Label(master = bpm_frame , text = str(bpm),height = 1,width = 20,bg = "yellow")
        bpm_show_lable.place(x = 150, y = 50)
    elif(filter_option.get() == "butter"):
        ax2.set_ylim(-200,400)
        coefficient, a = set_butter_filter(100,8,low_cut_scale.get(),high_cut_scale.get())
        draw_response_zeroandpole(coefficient,a)
        y = signal.lfilter(coefficient, a, y)
        for ii in range(100):
            PData.add(x[ii], y[ii], y1[ii])
        ax.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
        ax2.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
        line.set_xdata(PData.axis_x)
        line.set_ydata(PData.axis_y1)
        line2.set_xdata(PData.axis_x)
        line2.set_ydata(PData.axis_y)
        line3.set_xdata(f)
        line3.set_ydata(abs(np.fft.fft(y)))
        canvas3 = FigureCanvasTkAgg(fig, master=pulse_realtime_frame)
        canvas3.draw()
        canvas3.get_tk_widget().place(x = 20, y = 100)
        ##BPM##
        ys = [i for i in range(100)]
        for i in range(100):
            ys[i] = PData.axis_y[i]
        t2 = PData.axis_x[np.argmax(ys)]
        if abs(t2 - t1) != 0:
            bpm = (1 / (abs(t2 - t1)) ) * 60
        t1 = t2
        bpm_show_lable = tk.Label(master = bpm_frame , text = str(bpm),height = 1,width = 20,bg = "yellow")
        bpm_show_lable.place(x = 150, y = 50)
    ##########################
    root.update() 
##########################


 




























'''
 

fig, (ax,ax2,ax3) = plt.subplots(3,1)
line,  = ax.plot(np.random.randn(100))
line2, = ax2.plot(np.random.randn(100))
line3, = ax3.plot(np.random.randn(100))

PData= PlotData(500)
ax.set_ylim(300, 400)
ax2.set_ylim(-10,10)
ax3.set_ylim(0,200)



# plot parameters
print('plotting data...')
# open serial port
strPort='com4'
ser = serial.Serial(strPort, 115200)
ser.flush()

start = time.time()

x = [i for i in range(100)]
y = [i for i in range(100)]
y1 = [i for i in range(100)]
y2 = [i for i in range(100)]

while True:
    for ii in range(100):
        try:
            data = float(ser.readline())
            x[ii] = time.time() - start
            y[ii] = data.real
            y1[ii] = data.real
            y2[ii] = int(ser.readline())
        except:
            pass

    f = np.arange(0, 100, 1)
    xf = np.fft.fft(y)
    xf[0] = 0
    y = np.fft.ifft(xf)
    y = signal.lfilter(z, 1, y)
    yf = np.fft.fft(y)
    for i in range(10,100):
        yf[i] = 0
    y = np.fft.ifft(yf)
    print(np.argmax(abs(np.fft.fft(y))))
    for ii in range(100):
        PData.add(x[ii], y[ii], y1[ii])
    ax.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    ax2.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    line.set_xdata(PData.axis_x)
    line.set_ydata(PData.axis_y1)
    line2.set_xdata(PData.axis_x)
    line2.set_ydata(PData.axis_y)
    line3.set_xdata(f)
    line3.set_ydata(abs(np.fft.fft(y)))
    # 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
    canvas1 = FigureCanvasTkAgg(fig, master=root)
    canvas1.draw()  
    canvas1.get_tk_widget().grid(row = 0,column = 1)
    root.update()
'''