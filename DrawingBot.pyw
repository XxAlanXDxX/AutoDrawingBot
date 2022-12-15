#Auto-Drawing-bot by XxAlanXDxX
import numpy as np
import cv2 as cv
import tkinter as tk
import tkinter.ttk as ttk
import pyautogui as pg
import pyperclip as pc

import sys
print('\n'.join(sys.path))

#start
def draw():
    quick = checkStartVar.get()
    scale = 11 - int(accVar.get())

    if quick:
        time.sleep(3)
        
        startx, starty = pg.position()

        startxVar.set(str(startx))
        startyVar.set(str(starty))
        endxVar.set(str(2000))
        endyVar.set(str(2000))
        
        endx, endy = 2000, 2000
        
    else:
        startx = int(startxEntry.get())
        starty = int(startyEntry.get())
        endx = int(endxEntry.get())
        endy = int(endyEntry.get())

    src = cv.imread("./pic.png")

    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    gaussian = cv.GaussianBlur(gray, (3, 3), 0)

    edges = cv.Canny(gaussian, 70, 210)
    contours, hierarchy = cv.findContours(
        edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    pg.PAUSE = 0.00001
    
    for i in range(0, len(contours)):
        if startx + contours[i][0][0][0] < endx and starty + contours[i][0][0][1] < endy:
            pg.moveTo(startx + contours[i][0][0][0], starty + contours[i][0][0][1])
            pg.mouseDown()

        else:
            continue
         
        for j in range(len(contours[i]) - 1, -1, -1 * scale):
            if startx + contours[i][j][0][0] < endx and starty + contours[i][j][0][1] < endy:
                 pg.moveTo(startx + contours[i][j][0][0], starty + contours[i][j][0][1], duration = 0.05)

            else:
                 pg.mouseUp()
                 break
        
        pg.mouseUp()        
       
    hint.config(text = "Done!")

#flieModes
hintON = False
        
def fileMode():
    global hintON

    if hintON:
        win.geometry('350x210')
        btnHint.config(text = "↓") 
        hintON = False

    else:
        win.geometry('350x240')
        btnHint.config(text = "↑") 
        hintON = True

#contours
def contours():
    cv.destroyAllWindows()
    src = cv.imread("./pic.png")

    sp = src.shape

    img = np.zeros((sp[0], sp[1]), dtype = np.uint8)
    img.fill(255)

    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    gaussian = cv.GaussianBlur(gray, (3, 3), 0)

    edges = cv.Canny(gaussian, 70, 210)
    
    # 尋找輪廓
    contours, hierarchy = cv.findContours(
        edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # 繪製輪廓
    cv.drawContours(img, contours, -1, (50, 50, 50), 2)
    cv.imshow('Preview', img)

    scale = 11 - int(accVar.get())
    
    count = 0

    for i in range(len(contours)):
        count += len(contours[i])

    usedTimes = (count * 0.02) / scale

    hint.config(text = str(len(contours)) + " 個輪廓 預估用時 : " +str(int(usedTimes)) + " 秒")

#color
def show_rgb(event,x,y,flags,userdata):
    if event == 1:
        src = cv.imread("./pic.png")
        color = src[y, x]

        colorhex = "#" + str(hex(int(color[2])))[2:4] + str(hex(int(color[1])))[2:4] + str(hex(int(color[0])))[2:4]
        pc.copy(colorhex)
        
        hint.config(text = "R " + str(int(color[2])) + "  G " + str(int(color[1])) + " B " + str(int(color[0])))
    
def color():
    cv.destroyAllWindows()
    src = cv.imread("./pic.png")
    cv.imshow('image', src)

    cv.setMouseCallback('image', show_rgb)

#setting 
def show_xy(event,x,y,flags,userdata):
    
    if event == 1:
        startxVar.set(str(x))
        startyVar.set(str(y))

    elif event == 2:
        endxVar.set(str(x))
        endyVar.set(str(y))
    
def setting():
    pg.screenshot('./screenshot.png')
    
    img = cv.imread('./screenshot.png')
    cv.imshow('img', img)

    cv.setMouseCallback('img', show_xy)

#pillow 
from PIL import Image, ImageGrab

def clipBoard(): #load from ClipBoard
    im = ImageGrab.grabclipboard()
    if isinstance(im, Image.Image):
        im.save('./pic.png')

        img = cv.imread('pic.png')
        height, width, _ = img.shape

        hint.config(text = "載入成功! (圖片大小 " + str(width) + "*" + str(height) + ")")

    else:
        hint.config(text = "錯誤!")

#win
win = tk.Tk() 
win.geometry('350x210')
win.title("AutoDrawingBot")
win.iconbitmap('.\icons\drawingbot.ico')
win.config(bg="#eeeeee", padx = 5, pady = 5)

#frames
Hintframe = tk.Frame(win)
Hintframe.pack(padx = 5, pady = 5) 
frame = tk.Frame(win)
frame.pack(padx = 5, pady = 5)
frame1 = tk.Frame(win)
frame1.pack(padx = 5, pady = 0)
frame2 = tk.Frame(win)
frame2.pack(padx = 5, pady = 5)

frame3 = tk.Frame(win)
frame3.pack(padx = 5, pady = 7)

#hint
btnHint = ttk.Button(Hintframe, text = "↓", command = fileMode)
btnHint.config(width = 2) 
btnHint.grid(row = 0, column = 1)

hint = tk.Label(Hintframe, bg="#dddddd", font = "System 15", text = "AutoDrawingBot")
hint.config(width = 28) 
hint.grid(row = 0, column = 0)

#startCoordinates
startxVar = tk.StringVar()
startxEntry = tk.Entry(frame, bg="#ffffff", textvariable = startxVar, font = "System 12", borderwidth = 1)
startxEntry.config(width = 5) 
startxEntry.insert(0, "0")
startxEntry.grid(row = 1, column = 1, padx = 1)

startyVar = tk.StringVar()
startyEntry = tk.Entry(frame, bg="#ffffff", textvariable = startyVar, font = "System 12", borderwidth = 1)
startyEntry.config(width = 5) 
startyEntry.insert(0, "0")
startyEntry.grid(row = 1, column = 2, padx = 1)

start = tk.Label(frame, bg="#eeeeee", font = "System 12", text = "開始座標 [x, y]")
start.config(width = 15) 
start.grid(row = 1, column = 0)

#endCoordinates
endxVar = tk.StringVar()
endxEntry = tk.Entry(frame, bg="#ffffff", textvariable = endxVar, font = "System 12", borderwidth = 1)
endxEntry.config(width = 5) 
endxEntry.insert(0, "0")
endxEntry.grid(row = 2, column = 1, padx = 1)

endyVar = tk.StringVar()
endyEntry = tk.Entry(frame, bg="#ffffff", textvariable = endyVar, font = "System 12", borderwidth = 1)
endyEntry.config(width = 5) 
endyEntry.insert(0, "0")
endyEntry.grid(row = 2, column = 2, padx = 1)

end = tk.Label(frame, bg="#eeeeee", font = "System 12", text = "邊界座標 [x, y]")
end.config(width = 15) 
end.grid(row = 2, column = 0)

#accuracy
accVar = tk.StringVar()
accSpinbox = tk.Spinbox(frame1, from_=1, to=10, textvariable=accVar, wrap = True)
accSpinbox.config(width = 10)
accSpinbox.grid(row = 0, column = 1)
accVar.set("7")

acc = tk.Label(frame1, bg="#eeeeee", font = "System 12", text = "精準度")
acc.config(width = 15) 
acc.grid(row = 0, column = 0)

#buttons
btnLoad = ttk.Button(frame2, text = "剪貼簿", command = clipBoard)
btnLoad.grid(row = 0, column = 0)
btnSet = ttk.Button(frame2, text = "調整座標", command = setting)
btnSet.grid(row = 0, column = 1)
btnStart = ttk.Button(frame2, text = "開始", command = draw)
btnStart.grid(row = 0, column = 2)

btnStart = ttk.Button(frame2, text = "顯示圖片", command = color)
btnStart.grid(row = 1, column = 0)
btnContours = ttk.Button(frame2, text = "預覽", command = contours)
btnContours.grid(row = 1, column = 1)

#checkBtn
checkStartVar = tk.BooleanVar()
checkStart = ttk.Checkbutton(frame2, text='快速開始', var = checkStartVar)
checkStart.grid(row = 1, column = 2)

#XxAlanXDxX
XxAlanXDxX = tk.Label(frame3, bg="#eeeeee",fg = "#cccccc",  font = "System 10", text = "新北市南山高中 普一和 22 吳晉綸 製作")
XxAlanXDxX.config(width = 35) 
XxAlanXDxX.grid(row = 10, column = 0)


#repeat
win.mainloop()
