import numpy as np
from multiprocessing import cpu_count
# Description: Constants used in the program
MAX_WORKERS = cpu_count()
SETPOS_RECTANGLE_COLOR = (0, 0, 255)
COORDSELECTOR_RESIZE_SCALE = 0.8
SIMPLIFYCONSTANT = 1/47
OFFSETTIMESVALUE = 0.16

def douglasPeucker(points, tolerance):
    def perpendicularDistance(point, line_start, line_end):
        line_length = np.linalg.norm(line_end - line_start)
        if line_length == 0:
            return np.linalg.norm(point - line_start)
        return np.abs(np.cross(line_end - line_start, point - line_start)) / line_length

    def horizontalDistance(point, line_start, line_end):
        x1, y1 = line_start
        x2, y2 = line_end
        x, y = point

        numerator = np.abs((x2 - x1) * (y1 - y) - (x1 - x) * (y2 - y1))
        denominator = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        return numerator / denominator

    stack = [(0, len(points) - 1)]
    simplified_points = []

    while stack:
        start, end = stack.pop()

        max_distance = 0
        farthest_point_index = 0

        for i in range(start + 1, end):
            distance = perpendicularDistance(points[i], points[start], points[end]) + horizontalDistance(points[i], points[start], points[end])

            if distance > max_distance:
                max_distance = distance
                farthest_point_index = i

        if max_distance > tolerance:
            stack.append((start, farthest_point_index))
            stack.append((farthest_point_index, end))
        else:
            if start == 0 and end == len(points) - 1:
                simplified_points.append(points[0])
            simplified_points.append(points[start])

    return simplified_points

def calculateOffset(edge):
    farthest_point = max(edge, key=lambda point: np.linalg.norm(point - edge[0]))
    main_vector = farthest_point - edge[0]
    offset_distances = [np.linalg.norm((point - edge[0]) - np.dot((point - edge[0]), main_vector) / np.dot(main_vector, main_vector) * main_vector) for point in edge[1:]]

    return sum(offset_distances) / len(offset_distances)

# # 測試
# edge = np.array([[0, 0], [1, 1], [2, 0], [3, 1]])
# calculateOffset(edge)
    