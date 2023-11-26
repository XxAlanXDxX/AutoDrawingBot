import math
import time
import numpy as np
import cv2 as cv
from Constants import *

import json
with open('./setting.json', 'r', encoding="utf8") as jfile:
  SETTING = json.load(jfile)

class ImageLoader:
    def __init__(self, img_path, auto_drawer_GUI):
        self.auto_drawer_GUI = auto_drawer_GUI

        self.auto_drawer_GUI.log.updateLog("m_image: 加載圖片中..", LOG_PROCESS_COLOR)
        self.auto_drawer_GUI.configFuntionBtn(False)
        self.auto_drawer_GUI.configLoadBtn(False)

        self.image = cv.imread(img_path)
        self.auto_drawer_GUI.log.updateLog(f"m_image: 原始大小 {self.image.shape[:-1]}")
        scale = self.caculateResizeScale()
        if SETTING["AUTO_FIT_AREA"]:
            height, width, _ = self.image.shape
            self.image = cv.resize(self.image, (int(width * scale), int(height * scale)))
            self.auto_drawer_GUI.log.updateLog(f"m_image:調整大小 {self.image.shape[:-1]}")

        grayscale_img = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        gaussian = cv.GaussianBlur(grayscale_img, SETTING["KERNEL_SIZE"], 0)
        edges = cv.Canny(gaussian, SETTING["LOW_cTHRESHOLD"], SETTING["HIGH_cTHRESHOLD"])
        contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        self.edges = self.fixEdges([np.squeeze(contour) for contour in contours])
        scaling_factor = int(self.auto_drawer_GUI.scaling_factor.get()) / 100
        self.simplified_edges = self.simplifyEdges(self.edges, scaling_factor)

        self.total_coords = sum([len(edge) for edge in self.simplified_edges])

        self.auto_drawer_GUI.log.updateLog("m_image: 完成!", LOG_DONE_COLOR)
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