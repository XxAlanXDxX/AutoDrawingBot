import cv2 as cv
import numpy as np
import pyautogui as pg
from PyQt5.QtCore import QObject, pyqtSignal, QThread

from Constants import *

class WorkerSignals(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(tuple)

class CoordSelector(QThread):
    def __init__(self, parent=None):
        super(CoordSelector, self).__init__(parent)
        self.progress_signal = WorkerSignals()
        self.selection = None
        self.drag_start = None
        self.track_window = None
        self.screenshot = None

    def run(self):
        pg.screenshot('./images/screenshot.png')
        image = cv.imread('./images/screenshot.png')
        width, height, _ = image.shape
        self.screenshot = cv.resize(image, (int(height * COORDSELECTOR_RESIZE_SCALE), int(width * COORDSELECTOR_RESIZE_SCALE)))
        self.selection = None
        self.drag_start = None
        self.track_window = None

        cv.imshow('setCoord', self.screenshot)
        cv.setMouseCallback('setCoord', self.onMouse)

        while True:
            frame_copy = self.screenshot.copy()
            selection = self.selection

            # 畫出選取的矩形
            if selection:
                cv.rectangle(frame_copy, (selection[0], selection[1]), (selection[0] + selection[2], selection[1] + selection[3]), SETPOS_RECTANGLE_COLOR, 2)

            # 顯示處理後的影像
            cv.imshow("setCoord", frame_copy)
            key = cv.waitKey(1) & 0xFF
            if key == 27:
                self.progress_signal.finished.emit()
                break

    def onMouse(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            self.drag_start = (x, y)
            self.track_window = None

        elif event == cv.EVENT_LBUTTONUP:
            self.drag_start = None
            self.track_window = (min(x, self.selection[0]), min(y, self.selection[1]),
                                abs(x - self.selection[0]), abs(y - self.selection[1]))
            if self.track_window[2] > 0 and self.track_window[3] > 0:
                start_coord = np.array([self.track_window[1], self.track_window[0]])
                end_coord = np.array([self.track_window[1] + self.track_window[3], self.track_window[0] + self.track_window[2]])

                roi = self.screenshot[start_coord[0]:end_coord[0], start_coord[1]:end_coord[1]]
                cv.imshow("Selected Region", roi)

                self.progress_signal.progress.emit((start_coord // COORDSELECTOR_RESIZE_SCALE, end_coord // COORDSELECTOR_RESIZE_SCALE))


        elif self.drag_start:
            min_x = min(x, self.drag_start[0])
            min_y = min(y, self.drag_start[1])
            width = abs(x - self.drag_start[0])
            height = abs(y - self.drag_start[1])
            self.selection = (min_x, min_y, width, height)