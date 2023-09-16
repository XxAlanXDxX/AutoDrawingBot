AutoDrawingBot
======

![license MIT](https://img.shields.io/badge/license-MIT-blue)
![python 3.10.6](https://img.shields.io/badge/python-3.10.6-blue)

> 2023 &copy; alanwu-9852
> 
> Language: English / [繁體中文](./README.zh-TW.md)

Project Introduction
---
This project is an automatic drawing robot application called "AutoDrawingBot." It can automatically draw within a specified area based on the contour information of the loaded image.

Usage Instructions
---

Getting Started:
- Load an image
- Set the starting coordinates and ending coordinates
- Set the simplification factor and scaling factor
- Clipboard: Copy an image from the clipboard into the program
- Start drawing
- Display the image
- Resize the image
- Reload the image: Reload the image from the file

Usage Example:

1. Launch the program.
2. Click the "Clipboard" button to load an image from the clipboard.
3. Set the starting coordinates and ending coordinates to specify the drawing area (click with the left mouse button).
4. Set the simplification factor and scaling factor as needed.
5. Click the "Start" button, and the program will automatically draw the contours of the image.
6. You can use other buttons to display the image, resize the image, and perform other operations.

setting.json Description:

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

To-Do List
---
Here are some upcoming features and improvements:

- [ ] Enhance drawing algorithm for faster execution
- [ ] Add export contours and import functionality
- [ ] Add embedding preview functionality

If you have any suggestions or questions, please feel free to contact the author.
