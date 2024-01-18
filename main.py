import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PIL import Image, ImageGrab
import cv2 as cv
import numpy as np

from DataManager import DataManager
from DrawSubsystem import DrawSubsystem
from ImageLoader import ImageLoader
from CoordSelector import CoordSelector
from Constants import *

import time

Ui_MainWindow, QtBaseClass = uic.loadUiType("mainGUI.ui")

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setupUi(self)

        self.saved_image_edges = []
        self.current_image_edges = None
        self.setWindowIcon(QIcon('assets\icon.ico'))

        self.loadData()
        self.connectFunctionBtn()

    def loadData(self):
        self.data_manager = DataManager()

        self.DEFAULT_SCALINE_FACTOR.setValue(self.data_manager.jsetting["DEFAULT_SCALINE_FACTOR"])
        self.MIN_EDGE_LENGTH.setValue(self.data_manager.jsetting["MIN_EDGE_LENGTH"])
        self.KERNEL_SIZEx.setValue(self.data_manager.jsetting["KERNEL_SIZE"][0])
        self.KERNEL_SIZEy.setValue(self.data_manager.jsetting["KERNEL_SIZE"][1])
        self.LOW_cTHRESHOLD.setValue(self.data_manager.jsetting["LOW_cTHRESHOLD"])
        self.HIGH_cTHRESHOLD.setValue(self.data_manager.jsetting["HIGH_cTHRESHOLD"])
        self.DEFAULT_START_COORDx.setValue(self.data_manager.jsetting["DEFAULT_START_COORD"][0])
        self.DEFAULT_START_COORDy.setValue(self.data_manager.jsetting["DEFAULT_START_COORD"][1])
        self.DEFAULT_END_COORDx.setValue(self.data_manager.jsetting["DEFAULT_END_COORD"][0])
        self.DEFAULT_END_COORDy.setValue(self.data_manager.jsetting["DEFAULT_END_COORD"][1])
        self.AUTO_FIT_AREA.setChecked(self.data_manager.jsetting["AUTO_FIT_AREA"])
        self.PGPAUSE.setValue(self.data_manager.jsetting["PGPAUSE"])
        self.USE_SPEEDMODE.setChecked(self.data_manager.jsetting["USE_SPEEDMODE"])

        self.SCALINE_FACTOR.setValue(self.data_manager.jsetting["DEFAULT_SCALINE_FACTOR"])
        self.START_COORDx.setValue(self.data_manager.jsetting["DEFAULT_START_COORD"][0])
        self.START_COORDy.setValue(self.data_manager.jsetting["DEFAULT_START_COORD"][1])
        self.END_COORDx.setValue(self.data_manager.jsetting["DEFAULT_END_COORD"][0])
        self.END_COORDy.setValue(self.data_manager.jsetting["DEFAULT_END_COORD"][1])

    def connectFunctionBtn(self):
        self.apply_btn.clicked.connect(self.applySetting)
        self.clipboard_btn.clicked.connect(self.loadfromClipboard)
        self.openfile_btn.clicked.connect(self.openFile)
        self.setcoord_btn.clicked.connect(self.setCoord)
        self.start_btn.clicked.connect(self.startDrawing)
        self.resizeEdges_btn.clicked.connect(self.resizeEdges)
        self.reload_btn.clicked.connect(self.reloadImage)

        self.edges_select.itemClicked.connect(self.edgeSelected)

        self.reload_btn.setEnabled(False)
        self.start_btn.setEnabled(False)
        self.resizeEdges_btn.setEnabled(False)

    def toggleBtn(self, state):
        self.start_btn.setEnabled(state)
        self.apply_btn.setEnabled(state)
        self.clipboard_btn.setEnabled(state)
        self.setcoord_btn.setEnabled(state)
        self.openfile_btn.setEnabled(state)
        self.reload_btn.setEnabled(state)
        self.resizeEdges_btn.setEnabled(state)

    def applySetting(self):
        self.data_manager.saveSetting({
            "DEFAULT_SCALINE_FACTOR": self.DEFAULT_SCALINE_FACTOR.value(),
            "MIN_EDGE_LENGTH": self.MIN_EDGE_LENGTH.value(),
            "KERNEL_SIZE": [self.KERNEL_SIZEx.value(), self.KERNEL_SIZEy.value()],
            "LOW_cTHRESHOLD": self.LOW_cTHRESHOLD.value(),
            "HIGH_cTHRESHOLD": self.HIGH_cTHRESHOLD.value(),
            "DEFAULT_START_COORD": [self.DEFAULT_START_COORDx.value(), self.DEFAULT_START_COORDy.value()],
            "DEFAULT_END_COORD": [self.DEFAULT_END_COORDx.value(), self.DEFAULT_END_COORDy.value()],
            "AUTO_FIT_AREA": self.AUTO_FIT_AREA.isChecked(),
            "PGPAUSE": self.PGPAUSE.value(),
            "USE_SPEEDMODE": self.USE_SPEEDMODE.isChecked()
        })

        self.statusbar.showMessage(f"儲存設定! ", 2000)

    def getsetting(self):
        setting = {
            "SCALINE_FACTOR": self.SCALINE_FACTOR.value(),
            "MIN_EDGE_LENGTH": self.MIN_EDGE_LENGTH.value(),
            "KERNEL_SIZE": [self.KERNEL_SIZEx.value(), self.KERNEL_SIZEy.value()],
            "LOW_cTHRESHOLD": self.LOW_cTHRESHOLD.value(),
            "HIGH_cTHRESHOLD": self.HIGH_cTHRESHOLD.value(),
            "START_COORD": [self.START_COORDx.value(), self.START_COORDy.value()],
            "END_COORD": [self.END_COORDx.value(), self.END_COORDy.value()],
            "AUTO_FIT_AREA": self.AUTO_FIT_AREA.isChecked(),
            "PGPAUSE": self.PGPAUSE.value(),
            "USE_SPEEDMODE": self.USE_SPEEDMODE.isChecked()
        }

        return setting

    def setCoord(self):
        coord_selector = CoordSelector(self)
        coord_selector.progress_signal.progress.connect(self.setCoordCallback)
        coord_selector.progress_signal.finished.connect(self.setCoordFinished)
        coord_selector.start()

    def setCoordCallback(self, coords):
        self.START_COORDx.setValue(int(coords[0][1]))
        self.START_COORDy.setValue(int(coords[0][0]))
        self.END_COORDx.setValue(int(coords[1][1]))
        self.END_COORDy.setValue(int(coords[1][0]))

    def setCoordFinished(self):
        cv.destroyAllWindows()

    def loadfromClipboard(self):
        im = ImageGrab.grabclipboard()
        if isinstance(im, Image.Image):
            im.save('./images/raw_image.png')
            im.save('./images/image.png')

            self.loadImage("./images/raw_image.png")

        else:
            self.statusbar.showMessage(f"未擷取到圖片! ", 2000)

    def openFile(self):
        path, _ = QFileDialog.getOpenFileName(self, "選擇圖片", "", "Image Files (*.png *.jpg *.bmp)")
        self.loadImage(path) if path else None

    def reloadImage(self):
        selected_item = self.edges_select.currentItem()
        draw_image_edges = self.saved_image_edges[self.edges_select.row(selected_item)] if selected_item else self.current_image_edges

        self.loadImage(draw_image_edges.path)

    def loadImage(self, path):
        self.start_time = time.time()
        self.toggleBtn(False)

        if self.data_manager.jsetting["USE_SPEEDMODE"]:
            self.statusbar.showMessage(f"加載圖片中... (快速模式)")
            self.progressing_data.setText("圖片處理: ")

        imageLoader = ImageLoader(
            path=path, 
            setting=self.getsetting(), 
            parent=self
        )

        imageLoader.progress_signal.progress.connect(self.imageLoaderCallback)
        imageLoader.progress_signal.finished.connect(self.imageLoaderFinished)
        imageLoader.start()

    def imageLoaderCallback(self, progress):
        self.progressBar.setValue(int(progress))
        self.statusbar.showMessage(f"加載圖片中...")
        self.progressing_data.setText("圖片處理: ")

    def imageLoaderFinished(self, result):
        self.toggleBtn(True)
        self.statusbar.showMessage(f"完成! 用時 {time.time() - self.start_time:.2f} 秒", 2000)
        self.progressing_data.setText("")
        self.progressBar.setValue(0)

        self.current_image_edges = result
        self.saved_image_edges.append(result)
        self.edges_select.addItem(result.timestemp)
        self.edges_select.setCurrentRow(self.edges_select.count() - 1)

        self.setDisplayImage(result.path)
        self.RESIZE_SCALE.setValue(result.scale * 100)

    def edgeSelected(self):
        selected_item = self.edges_select.currentItem()
        draw_image_edges = self.saved_image_edges[self.edges_select.row(selected_item)] if selected_item else self.current_image_edges

        self.setDisplayImage(draw_image_edges.path)

    def setDisplayImage(self, image_path):
        image = QImage(image_path)
        original_width = image.width()
        original_height = image.height()
        scaled_width = self.image_display.width()
        scaled_height = self.image_display.height()
        scaled_image = image.scaledToWidth(scaled_width) if original_width > original_height else image.scaledToHeight(scaled_height)
        pixmap = QPixmap(scaled_image)
        self.image_display.setPixmap(pixmap)
        
    def startDrawing(self):
        selected_item = self.edges_select.currentItem()
        draw_image_edges = self.saved_image_edges[self.edges_select.row(selected_item)] if selected_item else self.current_image_edges

        self.toggleBtn(False)
        self.progressBar.setValue(0)

        self.drawSubsystem = DrawSubsystem(
            image_edges=draw_image_edges, 
            setting=self.getsetting(), 
            parent=self
        )

        self.drawSubsystem.progress_signal.progress.connect(self.drawSubsystemCallback)
        self.drawSubsystem.progress_signal.finished.connect(self.drawSubsystemFinished)
        self.drawSubsystem.start()

    def drawSubsystemCallback(self, progress):
        self.progressBar.setValue(int(progress[1]))
        self.statusbar.showMessage(f"繪製中...")
        self.progressing_data.setText("繪製: ")

    def drawSubsystemFinished(self, feedback):
        self.toggleBtn(True)
        self.progressBar.setValue(0)
        self.statusbar.showMessage(f'{["完成!", "游標移動!"][feedback]}', 2000)
        self.progressing_data.setText("")

    def resizeEdges(self):
        scale_value = self.RESIZE_SCALE.value() / 100
        for i, edge in enumerate(self.current_image_edges.edges):
            self.current_image_edges.edges[i] = np.array(edge) * np.array([scale_value, scale_value])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
