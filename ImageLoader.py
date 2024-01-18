import concurrent.futures
import math
import multiprocessing
import numpy as np
import cv2 as cv
import datetime

from PyQt5.QtCore import QObject, pyqtSignal, QThread, QMetaObject, Qt, Q_ARG
from Constants import *

def simplify_edge(args):
    edge, tolerance, progress_callback = args
    offset = calculateOffset(edge)
    # print(f'--{offset:.2f}--')
    if offset == 0:
        return [edge[0], edge[-1]]
    
    tolerance /= math.log(1 + OFFSETTIMESVALUE * offset)

    try:
        
        simplified_edge = douglasPeucker(np.array(edge), tolerance=tolerance)
        progress_callback() if progress_callback is not None else None
        return simplified_edge
    
    except Exception as e:
        print(f"Error processing edge: {e}")
        return None

class ImageEdges:
    def __init__(self, path, edges, scale):
        self.path = path
        self.edges = edges
        self.scale = scale
        self.total_coords = sum([len(edge) for edge in self.edges])
        self.timestemp = datetime.datetime.now().strftime("%H:%M:%S")

class WorkerSignals(QObject):
    finished = pyqtSignal(object)
    progress = pyqtSignal(float)

class ImageLoader(QThread):
    def __init__(self, path, setting, area=None, parent=None):
        super(ImageLoader, self).__init__(parent)
        self.progress_signal = WorkerSignals()

        self.path = path
        self.setting = setting

    def run(self):
        image = cv.imread(self.path)
        width, height, _ = image.shape

        start_coord = np.array(list(map(int, self.setting["START_COORD"])))
        end_coord = np.array(list(map(int, self.setting["END_COORD"])))
        area = [None, end_coord - start_coord][self.setting["AUTO_FIT_AREA"]]
        scale = self.caculateResizeScale(area, [height, width])
        image = cv.resize(image, (int(height * scale), int(width * scale)))

        grayscale_img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        gaussian = cv.GaussianBlur(grayscale_img, self.setting["KERNEL_SIZE"], 0)
        edges = cv.Canny(gaussian, self.setting["LOW_cTHRESHOLD"], self.setting["HIGH_cTHRESHOLD"])
        contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        edges = self.fixEdges([np.squeeze(contour) for contour in contours])
        edges = self.simplifyEdges(edges, self.setting["SCALINE_FACTOR"], self.setting["USE_SPEEDMODE"], MAX_WORKERS)
        self.progress_signal.finished.emit(ImageEdges(self.path, edges, scale))

    def caculateResizeScale(self, area, image_shape):
        if area is None:
            return 1

        image_shape = np.array(image_shape)
        # print(area, image_shape, area / image_shape)
        resize_scale = min(area / image_shape)
        resize_scale = resize_scale if resize_scale != 0 else 1
        return resize_scale
    
    def fixEdges(self, edges):
        fixed_edges = [edge for edge in edges if any(isinstance(coord, np.ndarray) for coord in edge)]
        return fixed_edges
    
    def simplifyEdges(self, edges, scaling_factor, use_speedMode=False, max_workers=cpu_count()):
        simplified_edges = []
        total_edges = len(edges)
        tolerance_values = [np.log(len(edge)) * (scaling_factor * SIMPLIFYCONSTANT) for edge in edges]
        simplified_edges_count = multiprocessing.Value('i', 0)

        def simplifyEdgesProgressCallback():
            nonlocal simplified_edges_count
            with simplified_edges_count.get_lock():
                simplified_edges_count.value += 1

            QMetaObject.invokeMethod(self.progress_signal, 'progress', Qt.QueuedConnection, Q_ARG(float, (simplified_edges_count.value / total_edges) * 100))

        if use_speedMode:
            with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
                args_list = [(edge, tolerance, None) for edge, tolerance in zip(edges, tolerance_values)]
                results = list(executor.map(simplify_edge, args_list, chunksize=max_workers))
        
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                args_list = [(edge, tolerance, simplifyEdgesProgressCallback) for edge, tolerance in zip(edges, tolerance_values)]
                results = list(executor.map(simplify_edge, args_list))

        simplified_edges.extend(filter(None, results))
        return simplified_edges

        