AutoDrawingBot
======

![license MIT](https://img.shields.io/badge/license-MIT-blue)
![python 3.10.6](https://img.shields.io/badge/python-3.10.6-blue)

> 2023 &copy; alanwu-9852
> 
> Language: English / [繁體中文](./README.zh-TW.md)

Project Overview
---
This is an automatic drawing program developed using PyQt5 and OpenCV. It allows users to load images, perform edge detection, and simulate the drawing process using mouse movements. The program provides a range of settings, allowing users to adjust various parameters for optimal drawing effects.

Usage Instructions
---

1. Run the Program: After executing the program, you will see the main window, which provides buttons for functions such as loading images, setting parameters, and starting drawing.

2. Set Parameters: Click the "Settings" button to adjust various parameters, including scaling factor, edge detection parameters, etc.

3. Load Images: Use the "Load Image" button or load an image from the clipboard. The program will process the image and display it in the main window.

4. Start Drawing: After adjusting the parameters, click the "Start Drawing" button to simulate the drawing process. The program will simulate the drawing process based on the results of edge detection, using mouse movements.


Explanation of setting.json:

* `DEFAULT_SCALINE_FACTOR` (Default Simplification Factor): This value represents the degree of simplification of images, expressed as a percentage.
* `MIN_EDGE_LENGTH` (Minimum Edge Length): This value represents the minimum length of edges to be retained during simplification.
* `KERNEL_SIZE` (Kernel Size): This is the size of a convolution kernel, typically used for image processing operations. It is represented as an array, [width, height].
* `LOW_cTHRESHOLD` (Low Canny Threshold): This is the low threshold used in Canny edge detection to determine edge strength.
* `HIGH_cTHRESHOLD` (High Canny Threshold): This is the high threshold used in Canny edge detection to determine edge strength.
* `DEFAULT_START_COORD` (Default Start Coordinates): These are the starting coordinates for drawing operations, represented as [x, y].
* `DEFAULT_END_COORD` (Default End Coordinates): These are the ending coordinates for drawing operations, represented as [x, y].
* `SETPOS_RECTANGLE_COLOR` (Set Position Rectangle Color): This is the color used to draw rectangles when marking coordinates adjustments, represented as an RGB color code.
* `AUTO_FIT_AREA` (Auto Fit Area): A boolean value that determines whether the image is automatically resized to fit the drawing area.
* `PG.PAUSE` (PyAutoGUI Pause): This is the pause time between operations in PyAutoGUI, measured in seconds.

Version Updates
---
* v1.0.0-beta (2022/12/15): Initial beta release.
* v1.0.1-beta (2023/1/17):
    1. Added contour mode using `cv.Canny` from `opencv-python` to detect image contours.
    2. Introduced resizing functionality for proportional image scaling.
    3. Added the ability to specify the drawing area.
* v1.0.0 (2023-09-10):
    1. Removed pixel intensity-based drawing mode.
    2. Simplified drawing time using the [Douglas-Peucker algorithm](https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm).
    3. Added setting.json configuration file for adjusting program parameters as needed.
* v1.2.0 (2024-01-18):
    1. Changed tkinter to PyQt.
    2. Added temporary data storage functionality.
    3. Used linear transformation to scale images.

To-Do List
---
Here are some upcoming features and improvements:

- [x] Add embedding preview functionality

If you have any suggestions or questions, please feel free to contact the author.
