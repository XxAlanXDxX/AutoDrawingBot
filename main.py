import math
import time
import numpy as np
import cv2 as cv
import tkinter as tk
from tkinter import ttk, filedialog
import pyautogui as pg
from PIL import Image, ImageGrab

import json
with open('./setting.json', 'r', encoding="utf8") as jfile:
  SETTING = json.load(jfile)

pg.FAILSAFE = False
pg.PAUSE = SETTING['PG.PAUSE']

class AutoDrawerGUI:
    def __init__(self, master):
        self.master = master
        self.intitialize_ui()
        self.configFuntionBtn(False)

    def intitialize_ui(self):
        self.master.geometry('670x265')
        self.master.title("AutoDrawingBot")
        self.master.iconbitmap("icon.ico")
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

        self.log = tk.Text(self.right_frame, width=35,  height=12, font=("System", 10))
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
        self.image = m_image("./images/image.png", self)

    def attachFile(self):
        file_path = filedialog.askopenfilename(title="Select file", filetypes= [("Image Files","*.png .jpg .jpeg")])

        if file_path:
            img = cv.imread(file_path)
            cv.imwrite('./images/raw_image.png', img) 
            cv.imwrite('./images/image.png', img) 
            self.updateLog(f"attachFile: 開啟檔案 {file_path.split('/')[-1]}")
            self.loadImage()

    def clipBoard(self):
        im = ImageGrab.grabclipboard()
        if isinstance(im, Image.Image):
            im.save('./images/raw_image.png')
            im.save('./images/image.png')

            self.loadImage()

        else:
            self.updateLog(f"clipBoard: 錯誤! 未擷取到圖片")

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
        #print(self.image.total_coords)

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
            self.updateLog("AutDrawingBot: 完成!")

        if exception_code == -1:
            self.updateLog("AutDrawingBot: 游標移動: -1")

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

        self.updateLog(f"resizeImage: 調整成功! ({str(int(width * scale))} * {str(int(height * scale))})")

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

class m_image:
    def __init__(self, img_path, auto_drawer_GUI):
        self.auto_drawer_GUI = auto_drawer_GUI

        self.auto_drawer_GUI.updateLog("m_image: 加載圖片中..")
        self.auto_drawer_GUI.configFuntionBtn(False)
        self.auto_drawer_GUI.configLoadBtn(False)

        self.image = cv.imread(img_path)
        self.auto_drawer_GUI.updateLog(f"m_image: 原始大小 {self.image.shape[:-1]}")
        scale = self.caculateResizeScale()
        if SETTING["AUTO_FIT_AREA"]:
            height, width, _ = self.image.shape
            self.image = cv.resize(self.image, (int(width * scale), int(height * scale)))
            self.auto_drawer_GUI.updateLog(f"m_image:調整大小 {self.image.shape[:-1]}")

        grayscale_img = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        gaussian = cv.GaussianBlur(grayscale_img, SETTING["KERNEL_SIZE"], 0)
        edges = cv.Canny(gaussian, SETTING["LOW_cTHRESHOLD"], SETTING["HIGH_cTHRESHOLD"])
        contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        self.edges = self.fixEdges([np.squeeze(contour) for contour in contours])
        scaling_factor = int(self.auto_drawer_GUI.scaling_factor.get()) / 100
        self.simplified_edges = self.simplifyEdges(self.edges, scaling_factor)

        self.total_coords = sum([len(edge) for edge in self.simplified_edges])

        self.auto_drawer_GUI.updateLog("m_image: 完成!")
        self.auto_drawer_GUI.configFuntionBtn(True)
        self.auto_drawer_GUI.configLoadBtn(True)

    def caculateResizeScale(self):
        img = cv.imread('./images/image.png')
        height, width, _ = img.shape
        image_shape = np.array([width, height])

        start_coord = np.array([int(self.auto_drawer_GUI.start_x.get()), int(self.auto_drawer_GUI.start_y.get())])
        end_coord = np.array([int(self.auto_drawer_GUI.end_x.get()), int(self.auto_drawer_GUI.end_y.get())])
        drawing_area = end_coord - start_coord
        resize_scale = min(drawing_area / image_shape)
        resize_scale = resize_scale if resize_scale != 0 else 1
        self.auto_drawer_GUI.scale.set(f"{(resize_scale * 100):.2f}")
        return resize_scale
        
    def fixEdges(self, edges):
        fixed_edges = [edge for edge in edges if any(isinstance(coord, np.ndarray) for coord in edge)]
        return fixed_edges

    def simplifyEdges(self, edges, scaling_factor):
        simplified_edges = []
        total_edges = len(edges)

        for i, edge in enumerate(edges):
            self.auto_drawer_GUI.updateHint(f"Optimizing {(i / total_edges * 100):.2f} %")

            curvature = self.calculateCurvature(edge)
            min_curvature = min(curvature) if len(curvature) > 0 else 1
            min_curvature = min_curvature if min_curvature != 0 else 1
            if min_curvature == math.inf:
                simplified_edges.append([edge[0], edge[-1]])

            else:
                tolerance = np.log(len(edge)) * scaling_factor * np.log(1/min_curvature)
                simplified_edge = self.douglasPeucker(np.array(edge), tolerance=tolerance)
                simplified_edges.append(simplified_edge)

        self.auto_drawer_GUI.updateHint(f"Optimizing 100.00 %")

        return simplified_edges
    
    def calculateCurvature(self, points):
        curvatures = []

        for i in range(1, len(points) - 1):
            p1 = points[i - 1]
            p2 = points[i]
            p3 = points[i + 1]

            vector1 = np.array([p1[0] - p2[0], p1[1] - p2[1]])
            vector2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])

            dot_product = np.dot(vector1, vector2)
            magnitude1 = np.linalg.norm(vector1)
            magnitude2 = np.linalg.norm(vector2)

            # Calculate angle between vectors using dot product
            angle = np.arccos(dot_product / (magnitude1 * magnitude2))

            # Calculate curvature (inverse of angle)
            curvature = 1 / angle if angle != 0 else float('inf')
            curvatures.append(curvature)

        return curvatures

    def douglasPeucker(self, points, tolerance):
        # print(len(points), tolerance)
        if len(points) <= SETTING["MIN_EDGE_LENGTH"]:
            return [points[0], points[-1]]

        stack = [(0, len(points) - 1)]
        simplified_points = []

        while stack:
            start, end = stack.pop()
            max_dist = 0
            max_index = 0

            line_start = points[start]
            line_end = points[end]

            for i in range(start + 1, end):
                self.auto_drawer_GUI.master.update()
                point = points[i]
                dist = self.perpendicularDistance(point, line_start, line_end)

                if dist > max_dist:
                    max_dist = dist
                    max_index = i

            if max_dist > tolerance:
                stack.append((start, max_index))
                stack.append((max_index, end))
            else:
                if start == 0 and end == len(points) - 1:
                    simplified_points.append(points[0])
                simplified_points.append(points[start])

        return simplified_points

    def perpendicularDistance(self, point, line_start, line_end):
        line_length = np.linalg.norm(line_end - line_start)
        if line_length == 0:
            return np.linalg.norm(point - line_start)
        return np.abs(np.cross(line_end - line_start, point - line_start)) / line_length
  
if __name__ == "__main__":
    root = tk.Tk()
    gui = AutoDrawerGUI(root)
    root.mainloop()