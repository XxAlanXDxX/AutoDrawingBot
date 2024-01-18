import numpy as np
import pyautogui as pg
from PyQt5.QtCore import QObject, pyqtSignal, QThread

from ImageLoader import ImageEdges
from Constants import *

class WorkerSignals(QObject):
    finished = pyqtSignal(int)
    progress = pyqtSignal(tuple)

class DrawSubsystem(QThread):
    def __init__(self, image_edges:ImageEdges, setting, parent=None):
        pg.PAUSE = setting["PGPAUSE"]
        super(DrawSubsystem, self).__init__(parent)
        self.progress_signal = WorkerSignals()
        self.image_edges = image_edges
        self.setting = setting

    def run(self):
        isBreak = False
        finished_coords = 0
        total_coords = self.image_edges.total_coords
        edges = self.image_edges.edges

        start_coord = np.array(list(map(int, self.setting["START_COORD"])))
        end_coord = np.array(list(map(int, self.setting["END_COORD"])))
        
        for edge in edges:
            if isBreak:
                break

            for edge_coord in edge:
                self.progress_signal.progress.emit((False, (finished_coords / total_coords) * 100))
                if type(edge_coord) is np.ndarray:
                    target_coord = (start_coord[0] + edge_coord[0], start_coord[1] + edge_coord[1])
                    
                if not (target_coord[0] > end_coord[0] or target_coord[1] > end_coord[1]):
                    pg.moveTo(target_coord)
                    pg.mouseDown()
                    if np.linalg.norm(np.subtract(pg.position(), target_coord)) > 180:
                        pg.mouseUp()
                        isBreak = True
                        self.progress_signal.finished.emit(1)
                        break

                else:
                    self.progress_signal.progress.emit((True, (finished_coords / total_coords) * 100))
                    
                finished_coords += 1

            pg.mouseUp()

        if not isBreak:
            self.progress_signal.finished.emit(0)