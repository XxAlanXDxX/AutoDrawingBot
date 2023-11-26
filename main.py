import numpy as np
import cv2 as cv
import tkinter as tk
from tkinter import ttk, filedialog
import pyautogui as pg
from PIL import Image, ImageGrab
from ImageLoader import ImageLoader
from Constants import *

import json

from libs.LogTextbox import LogTextbox
with open('./setting.json', 'r', encoding="utf8") as jfile:
  SETTING = json.load(jfile)

pg.FAILSAFE = False
pg.PAUSE = PGPAUSE

class AutoDrawerGUI:
    def __init__(self, master):
        self.master = master
        self.intitialize_ui()
        self.configFuntionBtn(False)

    def intitialize_ui(self):
        self.master.geometry('670x265')
        self.master.title("AutoDrawingBot")
        self.master.iconbitmap("assets/icon.ico")
        self.master.config(bg="#eeeeee", padx = 5, pady = 5)

        self.createFrames()
        self.createUserInput()
        self.createFunctionButtons()

    def createFrames(self):
        self.left_frame = tk.Frame(self.master)
        self.left_frame.grid(row=0, column=0, padx=5, pady=5)

        self.left_bottom_frame = tk.Frame(self.left_frame)
        self.left_bottom_frame.grid(row=2, column=0, padx=5, pady=5)

        self.left_middle_frame = tk.Frame(self.left_frame)
        self.left_middle_frame.grid(row=1, column=0, padx=5, pady=5)

        self.left_top_frame = tk.Frame(self.left_frame)
        self.left_top_frame.grid(row=0, column=0, padx=5, pady=5)

    def createUserInput(self):
        self.start_x = tk.StringVar()
        Entry = tk.Entry(self.left_top_frame, bg="#ffffff", textvariable = self.start_x, font = "System 12", borderwidth = 1)
        Entry.config(width = 5) 
        Entry.insert(0, str(SETTING["DEFAULT_START_COORD"][0]))
        Entry.grid(row = 0, column = 1, padx = 1)

        self.start_y = tk.StringVar()
        Entry = tk.Entry(self.left_top_frame, bg="#ffffff", textvariable = self.start_y, font = "System 12", borderwidth = 1)
        Entry.config(width = 5) 
        Entry.insert(0, str(SETTING["DEFAULT_START_COORD"][1]))
        Entry.grid(row = 0, column = 2, padx = 1)

        Label = tk.Label(self.left_top_frame, bg="#eeeeee", font = "System 12", text = "開始座標 [x, y]")
        Label.config(width = 15) 
        Label.grid(row = 0, column = 0)

        self.end_x = tk.StringVar()
        Entry = tk.Entry(self.left_top_frame, bg="#ffffff", textvariable = self.end_x, font = "System 12", borderwidth = 1)
        Entry.config(width = 5) 
        Entry.insert(0, str(SETTING["DEFAULT_END_COORD"][0]))
        Entry.grid(row = 1, column = 1, padx = 1)

        self.end_y = tk.StringVar()
        Entry = tk.Entry(self.left_top_frame, bg="#ffffff", textvariable = self.end_y, font = "System 12", borderwidth = 1)
        Entry.config(width = 5) 
        Entry.insert(0, str(SETTING["DEFAULT_END_COORD"][1]))
        Entry.grid(row = 1, column = 2, padx = 1)

        Label = tk.Label(self.left_top_frame, bg="#eeeeee", font = "System 12", text = "邊界座標 [x, y]")
        Label.config(width = 15) 
        Label.grid(row = 1, column = 0)

        self.scaling_factor = tk.StringVar()
        Spinbox = tk.Spinbox(self.left_middle_frame, from_=1, to=20, textvariable=self.scaling_factor, wrap = True)
        Spinbox.config(width = 10)
        Spinbox.grid(row = 0, column = 1)
        self.scaling_factor.set(str(SETTING["DEFAULT_SCALINE_FACTOR"]))

        Label = tk.Label(self.left_middle_frame, bg="#eeeeee", font = "System 12", text = "簡化量 (%)")
        Label.config(width = 15) 
        Label.grid(row = 0, column = 0)

        self.scale = tk.StringVar()
        Spinbox = tk.Spinbox(self.left_middle_frame, from_=1, to=300, textvariable=self.scale, wrap = True)
        Spinbox.config(width = 10)
        Spinbox.grid(row = 1, column = 1)
        self.scale.set("100")

        Label = tk.Label(self.left_middle_frame, bg="#eeeeee", font = "System 12", text = "縮放量 (%)")
        Label.config(width = 15) 
        Label.grid(row = 1, column = 0)

    def createFunctionButtons(self):
        Button_width = 8
        self.clipBoard_btn = ttk.Button(self.left_bottom_frame, text = "剪貼簿", width = Button_width, command = self.clipBoard)
        self.clipBoard_btn.grid(row = 0, column = 0)

        self.attachFile_btn = ttk.Button(self.left_bottom_frame, text = "開啟檔案", width = Button_width, command = self.attachFile)
        self.attachFile_btn.grid(row = 0, column = 1)

        self.reloadImage_btn = ttk.Button(self.left_bottom_frame, text = "重載圖片", width = Button_width, command = self.reloadImage)
        self.reloadImage_btn.grid(row = 0, column = 2)


        self.startDraw_btn = ttk.Button(self.left_bottom_frame, text = "開始", width = Button_width, command = self.startDraw)
        self.startDraw_btn.grid(row = 0, column = 3)

        self.resizeImage_btn = ttk.Button(self.left_bottom_frame, text = "調整大小", width = Button_width, command = self.resizeImage)
        self.resizeImage_btn.grid(row = 1, column = 0)

        self.setPositon_btn = ttk.Button(self.left_bottom_frame, text = "調整座標", width = Button_width, command = self.setPositon)
        self.setPositon_btn.grid(row = 1, column = 1)

        # self.openSetting_btn = ttk.Button(self.left_bottom_frame, text = "設定", width = Button_width, command = self.openSetting)
        # self.openSetting_btn.grid(row = 1, column = 2)

        self.showImage_btn = ttk.Button(self.left_bottom_frame, text = "顯示圖片", width = Button_width, command = self.showImage)
        self.showImage_btn.grid(row = 1, column = 3)

        #Right
        self.right_frame = tk.Frame(self.master)
        self.right_frame.grid(row=0, column=1, padx=10, pady=5)

        self.hint = tk.Label(self.right_frame, width=28, bg="#dddddd", font="System 12", text="")
        self.hint.grid(pady=5, columnspan=40)

        self.log = LogTextbox(self.right_frame, width=35,  height=12, font=("System", 10))
        self.log.grid(pady=5, columnspan=40)
        self.log_count = 0

    def updateLog(self, arg: str):
        if self.log_count >= 10:
            self.log.delete("1.0", "end")
            self.log_count = 0

        self.log.insert("end", f"{arg}\n")
        self.log_count += 1

    def updateHint(self, arg: str):
        self.hint.config(text=arg)
        self.master.update()

    def loadImage(self):
        self.image = ImageLoader("./images/image.png", self)

    def attachFile(self):
        file_path = filedialog.askopenfilename(title="Select file", filetypes= [("Image Files","*.png .jpg .jpeg")])

        if file_path:
            img = cv.imread(file_path)
            cv.imwrite('./images/raw_image.png', img) 
            cv.imwrite('./images/image.png', img) 
            self.log.updateLog(f"attachFile: 開啟檔案 {file_path.split('/')[-1]}", LOG_DONE_COLOR)
            self.loadImage()

    def clipBoard(self):
        im = ImageGrab.grabclipboard()
        if isinstance(im, Image.Image):
            im.save('./images/raw_image.png')
            im.save('./images/image.png')

            self.loadImage()

        else:
            self.log.updateLog(f"clipBoard: 錯誤! 未擷取到圖片", LOG_ERROR_COLOR)

    def reloadImage(self):
        self.loadImage()

    def setPositon(self):
            pg.screenshot('./images/screenshot.png')
            self.screenshot = cv.imread('./images/screenshot.png')
            self.positons = []
            cv.imshow('setPos', self.screenshot)
            cv.setMouseCallback('setPos', self.activePos)

    def activePos(self,event,x,y,flags,userdata):
        if event == cv.EVENT_LBUTTONDOWN:
            self.positons.append((x, y))

            if len(self.positons) > 2:
                self.screenshot = cv.imread('./images/screenshot.png')
                self.positons.pop(0)

            if len(self.positons) == 2:
                min_x = min(self.positons[0][0], self.positons[1][0])
                min_y = min(self.positons[0][1], self.positons[1][1])

                max_x = max(self.positons[0][0], self.positons[1][0])
                max_y = max(self.positons[0][1], self.positons[1][1])

                self.start_x.set(str(min_x))
                self.start_y.set(str(min_y))
                self.end_x.set(str(max_x))
                self.end_y.set(str(max_y))

                cv.rectangle(self.screenshot, self.positons[0], self.positons[1], SETTING["SETPOS_RECTANGLE_COLOR"], 2)
                cv.imshow("setPos", self.screenshot)

    def drawContours(self, start_coord: tuple, end_coord: tuple):
        edges = self.image.simplified_edges
        print(self.image.total_coords)

        finished_coords = 0
        for edge in edges:
            for edge_coord in edge:
                self.updateHint(f"Drawing {(finished_coords / self.image.total_coords * 100):.2f} %")
                if type(edge_coord) is np.ndarray:
                    target_coord = (start_coord[0] + edge_coord[0], start_coord[1] + edge_coord[1])
                    
                if not (target_coord[0] > end_coord[0] or target_coord[1] > end_coord[1]):
                    pg.moveTo(target_coord)
                    pg.mouseDown()
                    self.hint.config(fg="#000000")
                    if np.linalg.norm(np.subtract(pg.position(), target_coord)) > 180:
                        pg.mouseUp()
                        return -1
                else:
                    self.hint.config(fg="#ff0000")
                    
                finished_coords += 1

            pg.mouseUp()
            
        self.hint.config(fg="#000000")
        self.updateHint(f"Drawing 100.00 %")
        return 0

    def startDraw(self):
        start_coord = (int(self.start_x.get()), int(self.start_y.get()))
        end_coord = (int(self.end_x.get()), int(self.end_y.get()))
        self.exceptionCatcher(self.drawContours(start_coord, end_coord))

    def exceptionCatcher(self, exception_code):
        if exception_code == 0:
            self.log.updateLog("AutDrawingBot: 完成!", LOG_DONE_COLOR)

        if exception_code == -1:
            self.log.updateLog("AutDrawingBot: 游標移動: -1", LOG_ERROR_COLOR)

    def showImage(self):
        cv.destroyAllWindows()
        cv.imshow('Image', self.image.image)

    def resizeImage(self):
        scale = float(self.scale.get()) / 100
        cv.destroyAllWindows()
        raw_img = cv.imread('./images/raw_image.png')
        height, width, _ = raw_img.shape
        raw_img = cv.resize(raw_img, (int(width * scale), int(height * scale)))
        cv.imwrite('./images/image.png', raw_img)
        self.loadImage()
        cv.imshow('resizedImage', raw_img)

        self.log.updateLog(f"resizeImage: 調整成功! ({str(int(width * scale))} * {str(int(height * scale))})", LOG_DONE_COLOR)

    def configFuntionBtn(self, state: bool):
        state = [tk.DISABLED, tk.NORMAL][state]
        self.showImage_btn.config(state=state)
        self.startDraw_btn.config(state=state)
        self.resizeImage_btn.config(state=state)

    def configLoadBtn(self, state: bool):
        state = [tk.DISABLED, tk.NORMAL][state]
        self.clipBoard_btn.config(state=state)
        self.attachFile_btn.config(state=state)
        self.reloadImage_btn.config(state=state)


  
if __name__ == "__main__":
    root = tk.Tk()
    gui = AutoDrawerGUI(root)
    root.mainloop()